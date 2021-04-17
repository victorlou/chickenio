#! /usr/bin/python2

import sys
import time
from datetime import datetime
import requests
import json

EMULATE_HX711=False

rfid_sensitivity = 3
measures = 3
reference_unit = 1
min_weight = 100
max_feed = 999999
min_feed = 10
zero_tolerance = 1
db_failcount = 0
db_tolerance = 10
db_reqretries = 10
default_feed = 100
end_time = 5

url = 'https://chickenio-api.herokuapp.com'
#url = 'http://192.168.0.119:3000'
#address = "endereco ip do banco de dados"
#login = "login no banco de dados"
#password = "senha no banco de dados"

from mfrc522 import SimpleMFRC522
from rpi_ws281x import Adafruit_NeoPixel, Color
if not EMULATE_HX711:
    import RPi.GPIO as GPIO
    from hx711 import HX711
else:
    from emulated_hx711 import HX711
print("Inicializando sistema")

#preparar balancas
hx = HX711(23, 24)
hx.set_reading_format("MSB", "MSB")

# HOW TO CALCULATE THE REFFERENCE UNIT
# To set the reference unit to 1. Put 1kg on your sensor or anything you have and know exactly how much it weights.
# In this case, 92 is 1 gram because, with 1 as a reference unit I got numbers near 0 without any weight
# and I got numbers around 184000 when I added 2kg. So, according to the rule of thirds:
# If 2000 grams is 184000 then 1000 grams is 184000 / 2000 = 92.
hx.set_reference_unit_B(116.189)
hx.set_reference_unit_A(29.601)
#hx.set_reference_unit(reference_unit)
print("Preparando balancas")

hx.reset()
hx.tare_A()
hx.tare_B()

print("Tara das balancas configuradas!")

print("Pesando Primeiro...")
weight = hx.get_weight_B(5)
hx.power_down()
hx.power_up()
time.sleep(0.1)
print("Peso: %s" % weight)

reader = SimpleMFRC522()

strip = Adafruit_NeoPixel(12, 12, 800000, 10, False, 255)
strip.begin()

#preparar rele
GPIO.setup(13, GPIO.OUT)

#balanca A = galinha/poleiro
#balanca B = racao/comedouro

def mytime():
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

#funcao que detectara rfids e os retornara
def rfidDetect():
    succs = 0
    rfid = 0
    while succs < rfid_sensitivity:
        print("RFID: Reading RFIDs...")
        read = reader.read_id()
        if read == rfid:
            print("RFID: The %s RFID was read, it is the same as the previous reading %s. Successes: %s." % (read, rfid, succs+1))
            succs += 1
        else:
            print("RFID: The %s RFID was read, it is different from the previous reading %s. Successes were reset." % (read, rfid)) 
            rfid = read
            succs = 0
    print("RFID: The %s RFID was definitively detected, proceeding." % rfid)
    return rfid

#funcao que conectara ao banco de dados
def dbConnect(url):#(address, login, password):
    try:
        print(requests.get(url+'/').text)
        return True
    except:
        return False

#funcao que verificara se a galinha especifica pode ser alimentada
def dbCanFeed(rfid):
    for i in range(db_reqretries):
        try:
            pkg = requests.get(url+'/chickens/can-eat/%s' % rfid)
            print(pkg.text)
            return json.loads(pkg.text)["nextMealNumber"]
        except:
            print("Feed GET fail #%s" % i)
    return 0

#funcao que lera todos os dados relevantes para o calculo da quantidade da racao da galinha
def dbGetStats(rfid):
    for i in range(db_reqretries):
        try:
            pkg = requests.get(url+'/chickens/%s' % rfid)
            print(pkg.text)
            return json.loads(pkg.text)
        except:
            print("Stats GET fail #%s" % i)
    return None

#funcao que atualizara o peso da galinha
def dbUpdateWeight(rfid, weight):
    json = {'timestamp':mytime(), 'tag_code':'%s' % rfid,'weight':'%.2f' % weight}
    print(json)
    for i in range(db_reqretries):
        try:
            pkg = requests.post(url+'/chicken-weight-log/store', data = json)
            print(pkg.text)
            return True
        except:
            print("Weight POST fail #%s" % i)
    return False

#funcao que atualizara o peso da ultima refeicao da galinha
def dbUpdateFeed(rfid, feed, leftover, meals, mealn):
    json = {
        'tag_code':'%s' % rfid,
        'food_amount':'%.2f' % feed,
        'food_amount_at_end':'%.2f' % leftover,
        'ate_food':'%s' % (leftover < min_feed),
        'meals_per_day':'%s' % meals,
        'daily_meal_number':'%s' % mealn,
        'timestamp':mytime()}
    print(json)
    for i in range(db_reqretries):
        try:
            pkg = requests.post(url+'/feeder-weight-log/store', data = json)
            print(pkg.text)
            return True
        except:
            print("Feed POST fail #%s" % i)
    return False

#funcao que encerrara a conexao com o banco de dados
def dbDisconnect():
    return

#funcao para calcular quanta comida deve ser dada a galinha, baseado em uma serie de fatores
def calculateFeed(stats):
    return stats["food_quantity"]

#funcao que controla os LEDs
#color = 0 : desligado
#color = 1 : amarelo  - galinha pode ser alimentada, e esta sendo pesada
#color = 2 : azul     - pesagem da galinha concluida, racao sera dispensada
#color = 3 : verde    - dispensao de racao concluida
#color = 4 : laranja  - peso da galinha inconsistente
#color = 5 : vermelho - galinha nao pode ser alimentada
#color = 6 : roxo     - operacao concluida com sucesso, galinha pode se retirar
#color = 7 : cian     - racao foi inteiramente comida
#color = 9 : branco   - conexao com o banco de dados perdida, racao padrao sera dispensada
def lightLED(color):
    switcher = {
        0: Color(  0,   0,   0),
        1: Color(255, 255,   0),
        2: Color(  0,   0, 255),
        3: Color(  0, 255,   0),
        4: Color(255, 127,   0),
        5: Color(255,   0,   0),
        6: Color(127,   0, 255),
        7: Color(  0, 127, 255),
        9: Color(255, 255, 255)
    }
    #switcher = {
    #    0: Color(  0,   0,   0),
    #    1: Color(255,   0,   0),
    #    2: Color(255, 127,   0),
    #    3: Color(255,   0, 127),
    #    4: Color(255, 127, 127),
    #    5: Color(  0, 127, 255),
    #    6: Color(  0,   0, 255),
    #    7: Color(127,   0, 255),
    #    9: Color(255, 255, 255)
    #}
    for i in range(0, strip.numPixels(), 1):
        strip.setPixelColor(i, Color(0, 0, 0))
    for i in range(0, strip.numPixels(), 1):
        strip.setPixelColor(i, switcher.get(color, Color(0, 0, 0)))
    strip.show()
    return

def getChickenWeight():
    print("Pesando...")
    weight = hx.get_weight_A(5)
    hx.power_down()
    hx.power_up()
    time.sleep(0.1)
    print("Peso: %s" % weight)
    return weight

def getFeedWeight():
    weight = hx.get_weight_B(5)
    hx.power_down()
    hx.power_up()
    time.sleep(0.1)
    return weight

#funcao que liberara a racao especificada
def dispenseFood(tofeed):
    GPIO.output(13, 1)
    for i in range(max_feed):
        if getFeedWeight() >= tofeed:
            break
    GPIO.output(13, 0)
    return

def rfidWait(rfid):
    fails = 0
    while fails < rfid_sensitivity:
        print("RFID: Checking for the RFID...")
        read = reader.read_id_no_block()
        if read != rfid:
            print("RFID: The %s RFID was read, it is different from the chicken's %s RFID. Failures: %s." % (read, rfid, fails+1))
            fails += 1
        else:
            print("RFID: The %s RFID was read, it is the chicken's %s RFID. Failures were reset." % (read, rfid)) 
            fails = 0
        if (getFeedWeight() <= min_feed):
            lightLED(7)
        time.sleep(3)
    print("RFID: The %s RFID was definitively NOT detected, proceeding." % rfid)
    return

try:
    while True:
        rfid = rfidDetect()
        if rfid != 0:
            print("FEEDER: Read the RFID %s." % rfid)
            if dbConnect(url):#(address, login, password):
                print("FEEDER: Successfully connected to the database.")
                db_failcount = 0
                mealn = dbCanFeed(rfid)
                if mealn > 0:
                    print("FEEDER: The RFID %s chicken can be fed, measuring" % rfid)
                    lightLED(1)
                    #colhe varias medicoes do peso, quanto a memoria do Raspberry aguentar
                    zero_counter = 0
                    weights = []
                    print("Pesando NaHora...")
                    hx.power_down()
                    hx.power_up()
                    time.sleep(0.1)
                    weight = hx.get_weight_B(5)
                    hx.power_down()
                    hx.power_up()
                    time.sleep(0.1)
                    print("Peso: %s" % weight)
                    for i in range(measures):
                        weights.append(getChickenWeight())
                        #detector de quantas vezes a balanca nao mediu um peso significativo
                        if weights[i] < min_weight:
                            zero_counter += 1
                            if zero_counter > zero_tolerance:
                                break
                            else:
                                i -= 1
                        time.sleep(0.1)
                    #a racao so sera liberada se nao houver muitas medidas zero na balanca
                    print(weights)
                    if zero_counter <= zero_tolerance:
                        print("FEEDER: The chicken's weight is sufficiently consistent.")
                        lightLED(2)
                        medium_weight = 0
                        for i in range(measures):
                            medium_weight += weights[i]
                        medium_weight = medium_weight/measures
                        #salva e le dados no banco de dados para calcular quanta e qual racao deve ser dispersa
                        print("FEEDER: The chicken's %s weight will be uploaded to the database." % medium_weight)
                        dbUpdateWeight(rfid, medium_weight)
                        print("FEEDER: The chicken's feed will be determined by the data in the database.")
                        stats = dbGetStats(rfid)
                        feed = calculateFeed(stats)
                        #dispersao da racao ate os valores estipulados
                        print("FEEDER: Dispensing feed.")
                        dispenseFood(feed)
                        print("FEEDER: Feed dispensed, waiting for the chicken to eat and leave.")
                        lightLED(3)
                        rfidWait(rfid)
                        leftover = getFeedWeight()
                        print("FEEDER: The chicken has left, the %s feed and %s leftover weight will be uploaded to the database." % (feed, leftover))
                        dbUpdateFeed(rfid, feed, leftover, stats["meals_per_day"], mealn)
                        print("FEEDER: Operation complete.")
                        lightLED(6)
                    else :
                        print("FEEDER: The chicken's weight is not sufficiently consistent (it has probably left).")
                        lightLED(4)
                else:
                    print("FEEDER: The RFID %s chicken cannot be fed." % rfid)
                    lightLED(5)
                dbDisconnect()
                time.sleep(end_time)
                lightLED(0)
            else:
                print("FEEDER: Failed to connect to database. Fail Count: %s" % db_failcount)
                db_failcount += 1
                if db_failcount > db_tolerance:
                    db_failcount = 0
                    print("FEEDER: Too many database connection fails, engaging default program.")
                    lightLED(9)
                    dispenseFood(default_feed)
                    print("FEEDER: The default amount of feed was dispensed.")
                    time.sleep(end_time)
                    lightLED(0)
except (KeyboardInterrupt, SystemExit):
    print(" -> Feeder program shutdown...")
    print("Cleaning...")
    if not EMULATE_HX711:
        GPIO.cleanup()
    print("Bye!")
    sys.exit()
        
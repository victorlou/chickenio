#! /usr/bin/python2

import sys
import time
from datetime import datetime
import random

EMULATE_HX711=False

rfid_sensitivity = 10
measures = 100
referenceUnit = 1
min_weight = 100
max_feed = 10000
zero_tolerance = 50
dbfailcount = 0
dbtolerance = 3
default_feed = 100
end_time = 10

url = 'http://192.168.0.119:3000/'
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

hx = HX711(5, 6)
hx.set_reading_format("MSB", "MSB")

# HOW TO CALCULATE THE REFFERENCE UNIT
# To set the reference unit to 1. Put 1kg on your sensor or anything you have and know exactly how much it weights.
# In this case, 92 is 1 gram because, with 1 as a reference unit I got numbers near 0 without any weight
# and I got numbers around 184000 when I added 2kg. So, according to the rule of thirds:
# If 2000 grams is 184000 then 1000 grams is 184000 / 2000 = 92.
#hx.set_reference_unit(113)
#hx.set_reference_unit(referenceUnit)

hx.reset()
hx.tare_A()
hx.tare_B()

reader = SimpleMFRC522()

strip = Adafruit_NeoPixel(12, 12, 800000, 10, False, 255)
strip.begin()

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
    print("RFID: The %s RFID was definitively NOT detected, proceeding." % rfid)
    return

#funcao placeholder que conectara ao banco de dados
def dbConnect(url):#(address, login, password):
    try:
        #pkg = requests.get(url)
        #return 1
        return random.randint(0, 1)
    except:
        return 0

#funcao placeholder que detectara o rfid e o retornara
def dbCanFeed(rfid):
    json = {'timestamp':mytime(),'request':"can-feed",'rfid':'%s' % rfid}
    print(json)
    try:
        #pkg = requests.post(url, data = json)
        #print(pkg.text)
        if random.randint(0, 1) == 0:#pkg.text == "Yes":
            return True
        else:
            return False
    except:
        return False

#funcao placeholder que lera todos os dados relevantes para o calculo da quantidade da racao da galinha
def dbGetStats(rfid):
    json = {'timestamp':mytime(),'request':"get-weight",'rfid':'%s' % rfid}
    print(json)
    stats = []
    try:
        #pkg = requests.get(url, data = json)
        #print(pkg.text)
        stats.append(10000.0)#stats.append(float(pkg.text))
    except:
        stats.append(10000.0)
    return stats

#funcao placeholder que atualizara o peso da galinha
def dbUpdateWeight(rfid, weight):
    json = {'timestamp':mytime(),'request':"update-weight",'rfid':'%s' % rfid,'weight':'%.2f' % weight}
    print(json)
    try:
        #pkg = requests.post(url, data = json)
        #print(pkg.text)
        return True
    except:
        return False

#funcao placeholder que atualizara o peso da ultima refeicao da galinha
def dbUpdateFeed(rfid, feed):
    json = {'timestamp':mytime(),'request':"update-feed",'rfid':'%s' % rfid,'feed':'%.2f' % feed}
    print(json)
    try:
        #pkg = requests.post(url, data = json)
        #print(pkg.text)
        return True
    except:
        return False

#funcao placeholder que atualizara o peso do resto da ultima refeicao da galinha
def dbUpdateLeftover(rfid, leftover):
    json = {'timestamp':mytime(),'request':"update-leftover",'rfid':'%s' % rfid,'leftover':'%.2f' % leftover}
    print(json)
    try:
        #pkg = requests.post(url, data = json)
        #print(pkg.text)
        return True
    except:
        return False

#funcao placeholder que encerrara a conexao com o banco de dados
def dbDisconnect():
    return

#funcao para calcular quanta comida deve ser dada a galinha, baseado em uma serie de fatores
def calculateFeed(stats):
    return stats[0]/10 #por enquanto apenas retorna o peso da galinha dividido por 10

#funcao que controla os LEDs
#color = 0 : desligado
#color = 1 : amarelo  - galinha pode ser alimentada, e esta sendo pesada
#color = 2 : azul     - pesagem da galinha concluida, racao sera dispensada
#color = 3 : verde    - dispensao de racao concluida
#color = 4 : laranja  - peso da galinha inconsistente
#color = 5 : vermelho - galinha nao pode ser alimentada
#color = 6 : roxo     - operacao concluida com scuesso, galinha pode se retirar
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
        9: Color(255, 255, 255)
    }
    for i in range(0, strip.numPixels(), 1):
        strip.setPixelColor(i, Color(0, 0, 0))
    for i in range(0, strip.numPixels(), 1):
        strip.setPixelColor(i, switcher.get(color, Color(0, 0, 0)))
    strip.show()
    return

#funcao que liberara uma "unidade" do tipo de racao especificado
def dispenseFood():
    #codigo para girar o rele aqui
    return

def getChickenWeight():
    #weight = hx.get_weight_A(5)
    #hx.power_down()
    #hx.power_up()
    return random.uniform(0, 2000)#weight

def getFeedWeight():
    #weight = hx.get_weight_B(5)
    #hx.power_down()
    #hx.power_up()
    return random.uniform(0, 200)#weight

#funcao para encerrar o programa
def cleanAndExit():
    print("Cleaning...")
    if not EMULATE_HX711:
        GPIO.cleanup()
    print("Bye!")
    sys.exit()

try:
    while True:
        rfid = rfidDetect()
        if rfid != 0:
            print("FEEDER: Read the RFID %s." % rfid)
            if dbConnect(url):#(address, login, password):
                print("FEEDER: Successfully connected to the database.")
                dbfailcount = 0
                if dbCanFeed(rfid):
                    print("FEEDER: The RFID %s chicken can be fed, measuring" % rfid)
                    lightLED(1)
                    #colhe varias medicoes do peso, quanto a memoria do Raspberry aguentar
                    zero_counter = 0
                    weights = []
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
                        feed = calculateFeed(dbGetStats(rfid))
                        print("FEEDER: The chicken's %s feed weight will be uploaded to the database." % feed)
                        dbUpdateFeed(rfid, feed)
                        #dispersao da racao ate os valores estipulados
                        print("FEEDER: Dispensing feed.")
                        for i in range(max_feed):
                            dispenseFood()
                            if getFeedWeight() > feed:
                                break
                        print("FEEDER: Feed dispensed, waiting for the chicken to eat and leave.")
                        lightLED(3)
                        rfidWait(rfid)
                        feed = getFeedWeight()
                        print("FEEDER: The chicken has left, the %s leftover feed weight will be uploaded to the database." % feed)
                        dbUpdateLeftover(rfid, feed)
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
                print("FEEDER: Failed to connect to database. Fail Count: %s" % dbfailcount)
                dbfailcount += 1
                if dbfailcount > dbtolerance:
                    dbfailcount = 0
                    print("FEEDER: Too many database connection fails, engaging default program.")
                    lightLED(9)
                    for i in range(max_feed):
                        dispenseFood()
                        if getFeedWeight() > default_feed:
                            print("FEEDER: The default amount of feed was dispensed.")
                            break
                    time.sleep(end_time)
                    lightLED(0)
except (KeyboardInterrupt, SystemExit):
    print("FEEDER: Read the RFID %s." % rfid)
    cleanAndExit()
        
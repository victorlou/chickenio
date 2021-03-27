#! /usr/bin/python2

import time
import sys

EMULATE_HX711=False

measures = 255
referenceUnit = 1
min_weight = 1000
max_feed = 100000
zero_tolerance = 127

address = "endereco ip do banco de dados"
login = "login no banco de dados"
password = "senha no banco de dados"

if not EMULATE_HX711:
    import RPi.GPIO as GPIO
    from hx711 import HX711
else:
    from emulated_hx711 import HX711

#funcao placeholder que detectara o rfid e o retornara
def rfidDetect():
    return 1

#funcao placeholder que conectara ao banco de dados
def dbConnect(address, login, password):
    return 1

#funcao placeholder que detectara o rfid e o retornara
def dbCanFeed(rfid):
    return 1

#funcao placeholder que lera todos os dados relevantes para o calculo da quantidade da racao da galinha
def dbGetStats(rfid):
    stats[0] = 10000
    return stats

#funcao placeholder que lera qual o tipo de racao que deve ser dado a galinha
def dbGetFeedType(rfid):
    return 1

#funcao placeholder que atualizara o peso da galinha
def dbUpdateWeight(rfid, weight):
    return 1

#funcao placeholder que atualizara o peso da ultima refeicao da galinha
def dbUpdateFeed(rfid, feed):
    return 1

#funcao placeholder que encerrara a conexao com o banco de dados
def dbDisconnect():
    return 1

#funcao para calcular quanta comida deve ser dada a galinha, baseado em uma serie de fatores
def calculateFeed(stats):
    return stats[0]/10 #por enquanto apenas retorna o peso da galinha dividido por 10

#funcao que liga os LEDs em uma cor por ate 30 seg
#color = 0 : amarelo
#color = 1 : azul
#color = 2 : verde
#color = 3 : laranja
#color = 4 : vermelho
def lightLED(color):
    return 1

#funcao que liberara uma "unidade" do tipo de racao especificado
def dispenseFood(feed_type):
    return True

#funcao para encerrar o programa
def cleanAndExit():
    print("Cleaning...")
    if not EMULATE_HX711:
        GPIO.cleanup()
    print("Bye!")
    sys.exit()

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

#balanca A = galinha/poleiro
#balanca B = racao/comedouro

while True:
    rfid = rfidDetect()
    if rfid != 0:
        try:
            dbConnect(address, login, password)
            if dbCanFeed(rfid):
                lightLED(0)
                #colhe varias medicoes do peso, quanto a memoria do Raspberry aguentar
                zero_counter = 0
                for i in range(measures):
                    weights[i] = hx.get_weight_A(5)
                    hx.power_down()
                    hx.power_up()
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
                    lightLED(1)
                    medium_weight = 0
                    for i in range(measures):
                        medium_weight += weights[i]
                    medium_weight = medium_weight/(measures+1)
                    #salva e le dados no banco de dados para calcular quanta e qual racao deve ser dispersa
                    dbUpdateWeight(rfid, medium_weight)
                    feed_type = dbGetFeedType(rfid)
                    feed = calculateFeed(dbGetStats(rfid))
                    dbUpdateFeed(rfid, feed)
                    #dispersao da racao ate os valores estipulados
                    for i in range(maxfeed):
                        dispenseFood(feed_type)
                        if hx.get_weight_B(5) > feed:
                            break
                    lightLED(2)
                else :
                    lightLED(3)
            else:
                lightLED(4)
            dbDisconnect()
        except (KeyboardInterrupt, SystemExit):
            cleanAndExit()
        
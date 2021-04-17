#! /usr/bin/python2

import sys
import time
from datetime import datetime
import requests
import json

EMULATE_HX711=False

rfid_sensitivity = 3
measures = 3
min_weight = 10
db_reqretries = 3
end_time = 5

url = 'https://chickenio-api.herokuapp.com'
#url = 'http://192.168.0.119:3000'
#address = "endereco ip do banco de dados"
#login = "login no banco de dados"
#password = "senha no banco de dados"

from mfrc522 import SimpleMFRC522
if not EMULATE_HX711:
    import RPi.GPIO as GPIO
    from hx711 import HX711
else:
    from emulated_hx711 import HX711
print("Inicializando sistema")

#preparar balanca
hx = HX711(1, 7)
hx.set_reading_format("MSB", "MSB")

# HOW TO CALCULATE THE REFFERENCE UNIT
# To set the reference unit to 1. Put 1kg on your sensor or anything you have and know exactly how much it weights.
# In this case, 92 is 1 gram because, with 1 as a reference unit I got numbers near 0 without any weight
# and I got numbers around 184000 when I added 2kg. So, according to the rule of thirds:
# If 2000 grams is 184000 then 1000 grams is 184000 / 2000 = 92.
#hx.set_reference_unit_B(116.189)
#hx.set_reference_unit_A(29.601)
hx.set_reference_unit(423.5)
print("Preparando balancas")

hx.reset()
hx.tare()

print("Tara da balanca configurada!")

print("Pesando Primeiro...")
weight = hx.get_weight(5)
hx.power_down()
hx.power_up()
time.sleep(0.1)
print("Peso: %s" % weight)

reader = SimpleMFRC522()

#preparar rele
#GPIO.setup(13, GPIO.OUT)

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

def dbUpdateEggs(rfid, weight, laid):
    json = {'timestamp':mytime(), 'tag_code':'%s' % rfid,'egg_weight':'%.2f' % weight, 'laid_egg':'%s' % laid}
    print(json)
    for i in range(db_reqretries):
        try:
            pkg = requests.post(url+'/nest-weight-log/store', data = json)
            print(pkg.text)
            return True
        except:
            print("Eggs POST fail #%s" % i)
    return False

#funcao que encerrara a conexao com o banco de dados
def dbDisconnect():
    return

def getEggsWeight():
    weight = hx.get_weight(5)
    hx.power_down()
    hx.power_up()
    time.sleep(0.1)
    return weight

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
        time.sleep(3)
    print("RFID: The %s RFID was definitively NOT detected, proceeding." % rfid)
    return

try:
    while True:
        rfid = rfidDetect()
        if rfid != 0:
            print("NEST: Read the RFID %s." % rfid)
            if dbConnect(url):#(address, login, password):
                print("NEST: Successfully connected to the database. Waiting for the chicken to leave...")
                rfidWait(rfid)
                print("NEST: The chicken has left, the eggs' weight will be measured...")
                eggs = getEggsWeight()
                if eggs < min_weight:
                    print("NEST: Measurement done. The %s eggs weight is too small to be uploaded to the database." % eggs)
                    dbUpdateEggs(rfid, eggs, False)
                else:
                    print("NEST: Measurement done. The %s eggs weight will be uploaded to the database." % eggs)
                    dbUpdateEggs(rfid, eggs, True)
                print("NEST: Operation complete.")
                dbDisconnect()
                time.sleep(end_time)
            else:
                print("NEST: Failed to connect to database.")
except (KeyboardInterrupt, SystemExit):
    print(" -> NEST program shutdown...")
    print("Cleaning...")
    if not EMULATE_HX711:
        GPIO.cleanup()
    print("Bye!")
    sys.exit()
        
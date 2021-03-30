#!/usr/bin/python2
# vim: expandtab ts=4 sw=4
# Inspired by http://www.raspberrypi-spy.co.uk/2015/03/bh1750fvi-i2c-digital-light-intensity-sensor/

import smbus
import time
import BH1750
import Adafruit_DHT
import requests

url = 'http://192.168.0.119:3000/environmental-log/store'
#bus = smbus.SMBus(0) # Rev 1 Pi uses 0
bus = smbus.SMBus(1)  # Rev 2 Pi uses 1
DLsensor = BH1750(bus)
DHTsensor = Adafruit_DHT.DHT22
# Example using a Raspberry Pi with DHT sensor
# connected to GPIO23.
DHTpin = 4

delay = 3600

#funcao que atualizara as informacoes do ambiente na hora atual
def dbUpdate(sens, lr, hr, hr2, temp, humi):
    json = {'time':localtime(),'sensitivity':sens,'lowres':lr,'highres':hr,'highresb':hr2,'temperature':temp,'humidity':humi}
    print(json)
    pkg = requests.post(url, data = json)
    return pkg.text

while True:
    sens = DLsensor.mtreg
    lr = DLsensor.measure_low_res()
    hr = DLsensor.measure_high_res()
    hr2 = DLsensor.measure_high_res2()
    DLsensor.set_sensitivity((DLsensor.mtreg + 10) % 255)

    # Try to grab a sensor reading.  Use the read_retry method which will retry up
    # to 15 times to get a sensor reading (waiting 2 seconds between each retry).
    humi, temp = Adafruit_DHT.read_retry(DHTsensor, DHTpin)
    
    print(dbUpdate(sens, lr, hr, hr2, temp, humi))
    time.sleep(delay)
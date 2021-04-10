#!/usr/bin/python2
# vim: expandtab ts=4 sw=4
# Inspired by http://www.raspberrypi-spy.co.uk/2015/03/bh1750fvi-i2c-digital-light-intensity-sensor/

import sys
import smbus
import time
import Adafruit_DHT
import requests
import os
import shutil
from threading import Thread
from datetime import datetime
from google.cloud import storage
from firebase_admin import credentials, initialize_app, storage

class BH1750():
    """ Implement BH1750 communication. """
    # Define some constants from the datasheet
    POWER_DOWN = 0x00 # No active state
    POWER_ON   = 0x01 # Power on
    RESET      = 0x07 # Reset data register value
    # Start measurement at 4lx resolution. Time typically 16ms.
    CONTINUOUS_LOW_RES_MODE = 0x13
    # Start measurement at 1lx resolution. Time typically 120ms
    CONTINUOUS_HIGH_RES_MODE_1 = 0x10
    # Start measurement at 0.5lx resolution. Time typically 120ms
    CONTINUOUS_HIGH_RES_MODE_2 = 0x11
    # Start measurement at 1lx resolution. Time typically 120ms
    # Device is automatically set to Power Down after measurement.
    ONE_TIME_HIGH_RES_MODE_1 = 0x20
    # Start measurement at 0.5lx resolution. Time typically 120ms
    # Device is automatically set to Power Down after measurement.
    ONE_TIME_HIGH_RES_MODE_2 = 0x21
    # Start measurement at 1lx resolution. Time typically 120ms
    # Device is automatically set to Power Down after measurement.
    ONE_TIME_LOW_RES_MODE = 0x23

    def __init__(self, bus, addr=0x23):
        self.bus = bus
        self.addr = addr
        self.power_down()
        self.set_sensitivity()

    def _set_mode(self, mode):
        self.mode = mode
        self.bus.write_byte(self.addr, self.mode)

    def power_down(self):
        self._set_mode(self.POWER_DOWN)

    def power_on(self):
        self._set_mode(self.POWER_ON)

    def reset(self):
        self.power_on() #It has to be powered on before resetting
        self._set_mode(self.RESET)

    def cont_low_res(self):
        self._set_mode(self.CONTINUOUS_LOW_RES_MODE)

    def cont_high_res(self):
        self._set_mode(self.CONTINUOUS_HIGH_RES_MODE_1)

    def cont_high_res2(self):
        self._set_mode(self.CONTINUOUS_HIGH_RES_MODE_2)

    def oneshot_low_res(self):
        self._set_mode(self.ONE_TIME_LOW_RES_MODE)

    def oneshot_high_res(self):
        self._set_mode(self.ONE_TIME_HIGH_RES_MODE_1)

    def oneshot_high_res2(self):
        self._set_mode(self.ONE_TIME_HIGH_RES_MODE_2)

    def set_sensitivity(self, sensitivity=69):
        """ Set the sensor sensitivity.
            Valid values are 31 (lowest) to 254 (highest), default is 69.
        """
        if sensitivity < 31:
            self.mtreg = 31
        elif sensitivity > 254:
            self.mtreg = 254
        else:
            self.mtreg = sensitivity
        self.power_on()
        self._set_mode(0x40 | (self.mtreg >> 5))
        self._set_mode(0x60 | (self.mtreg & 0x1f))
        self.power_down()

    def get_result(self):
        """ Return current measurement result in lx. """   
        data = self.bus.read_word_data(self.addr, self.mode)
        count = data >> 8 | (data&0xff)<<8
        mode2coeff =  2 if (self.mode & 0x03) == 0x01 else 1
        ratio = 1/(1.2 * (self.mtreg/69.0) * mode2coeff)
        return ratio*count

    def wait_for_result(self, additional=0):
        basetime = 0.018 if (self.mode & 0x03) == 0x03 else 0.128
        time.sleep(basetime * (self.mtreg/69.0) + additional)

    def do_measurement(self, mode, additional_delay=0):
        """ 
        Perform complete measurement using command
        specified by parameter mode with additional
        delay specified in parameter additional_delay.
        Return output value in Lx.
        """
        self.reset()
        self._set_mode(mode)
        self.wait_for_result(additional=additional_delay)
        return self.get_result()

    def measure_low_res(self, additional_delay=0):
        return self.do_measurement(self.ONE_TIME_LOW_RES_MODE, additional_delay)

    def measure_high_res(self, additional_delay=0):
        return self.do_measurement(self.ONE_TIME_HIGH_RES_MODE_1, additional_delay)

    def measure_high_res2(self, additional_delay=0):
        return self.do_measurement(self.ONE_TIME_HIGH_RES_MODE_2, additional_delay)

url = 'http://192.168.0.119:3000/environmental-log/store'

#cred = credentials.Certificate('chickenio-309621-27a35130195e.json')
#initialize_app(cred, {'storageBucket': 'chickenio.appspot.com'})
#bucket = storage.bucket()

#bus = smbus.SMBus(0) # Rev 1 Pi uses 0
bus = smbus.SMBus(1)  # Rev 2 Pi uses 1
DLsensor = BH1750(bus)
DHTsensor = Adafruit_DHT.DHT22
# Example using a Raspberry Pi with DHT sensor
# connected to GPIO23.
DHTpin = 4

delay = 5#3600

def single_frame(name='img_'+datetime.now().strftime('%Y-%m-%d_%H:%M:%S')+'.jpg', quality=25):
    arg = 'raspistill -n -q %s -o images/%s' % (quality, name)
    Thread(target=os.system, args=([arg])).start()

#funcao que atualizara as informacoes do ambiente na hora atual
def dbUpdate(now, lumi, temp, humi):
    #print('%s %s %s %s' % (now, lumi, temp, humi))
    json = {'timestamp':now.strftime("%Y-%m-%d %H:%M:%S"),'light':"%.2f" % lumi,'temperature':"%.2f" % temp,'air_humidity':"%.2f" % humi}
    print(json)
    pkg = requests.post(url, data = json)
    return pkg.text

#funcao que atualizara as informacoes do ambiente na hora atual
def imageUp(now, filename):
    #image = bucket.blob(file)
    #image.upload_from_filename(filename='images/'+file)
    #image.make_public()
    #print("your file url", image.public_url)
    #folder = 'images'
    #for filename in os.listdir(folder):
    #    file_path = os.path.join(folder, filename)
    #    try:
    #        if os.path.isfile(file_path) or os.path.islink(file_path):
    #            os.unlink(file_path)
    #        elif os.path.isdir(file_path):
    #            shutil.rmtree(file_path)
    #    except Exception as e:
    #        print('Failed to delete %s. Reason: %s' % (file_path, e))
    return "Imagem Database Disconnected. Filename: %s" % filename

try:
    switch = 1
    while True:
        now = datetime.now()
        if switch:
            #sens = DLsensor.mtreg
            #hr = DLsensor.measure_high_res()
            #hr2 = DLsensor.measure_high_res2()
            lumi = DLsensor.measure_low_res()
            DLsensor.set_sensitivity((DLsensor.mtreg + 10) % 255)

            # Try to grab a sensor reading.  Use the read_retry method which will retry up
            # to 15 times to get a sensor reading (waiting 2 seconds between each retry).
            humi, temp = Adafruit_DHT.read_retry(DHTsensor, DHTpin)
            
            print(dbUpdate(now, lumi, temp, humi))
            switch = 0
        else:
            filename = 'img_'+now.strftime('%Y-%m-%d_%H:%M:%S')+'.jpg'
            single_frame(filename, 10)
            time.sleep(10)

            print(imageUp(now, filename))
            switch = 1
        time.sleep(delay/2)
except (KeyboardInterrupt, SystemExit):
    print(" -> Ambient Control program shutdown...")
    print("Bye!")
    sys.exit()
from __future__ import division

__author__ = 'Vijay Ganesan'
# Kingsin KS-10X Ultrasonic Sensor API for BBB
# See ks_test.py for implementation example
# Default address is 0x74

from drivers.BBB_lib.Adafruit_I2C import Adafruit_I2C
from time import sleep

class Ultrasonic_KS: #TODO: SetAddr
    """Kingsin KS 103B Ultrasonic Sensor Class"""
    def __init__(self, addr=0x74, debug=0): #Initialize using default sensor address
        self.addr = addr
        self.debug = debug
        self.i2c = Adafruit_I2C(self.addr, -1, debug)
    def ping(self): #Send signal, -1 if failed
        return self.i2c.write8(0x2,0xbc) #Write to register 2
    def read(self): #Read result, -1 if failed
        return (self.i2c.reverseByteOrder(self.i2c.readU16(0x2)))/10; #Return in cm


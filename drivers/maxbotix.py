__author__ = 'Vijay Ganesan'
# Maxbotix MB-1202 Ultrasonic Sensor API for BBB
# Maxbotix Sensor Documentation: http://maxbotix.com/documents/I2CXL-MaxSonar-EZ_Datasheet.pdf
# See maxbotix_test.py for implementation example

from drivers.BBB_lib.Adafruit_I2C import Adafruit_I2C
from time import sleep

class Ultrasonic_MB:
    """Maxbotix MB1202 I2C Ultrasonic Sensor Class"""
    def __init__(self, debug=0): #Initialize using default sensor address
        self.addr = 0x70
        self.i2c = Adafruit_I2C(0x70, -1, debug)

    def __init__(self, addr, debug=0): #Initialize using given I2C address
        self.addr = addr
        self.i2c = Adafruit_I2C(addr, -1, debug)

    def setAddr(self): #Modify the sensor address, WARNING: Use very sparingly, addresses are saved over power cycles
        return self.i2c.writeList(self.addr, 0, [0xAA, 0xA5, self.addr])

    def ping(self): #Send signal, -1 if failed
        return self.i2c.write8_noreg(0x51)
    
    def read(self): #Read result, -1 if failed
        return self.i2c.reverseByteOrder(self.i2c.readU16(0x0))

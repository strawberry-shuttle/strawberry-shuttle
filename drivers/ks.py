__author__ = 'Vijay Ganesan'
# Kingsin KS-10X Ultrasonic Sensor API for BBB
# See ks_test.py for implementation example
# Default address is 0x74

from drivers.BBB_lib.Adafruit_I2C import Adafruit_I2C
from time import sleep

class Ultrasonic_KS:
    """Kingsin KS 103B Ultrasonic Sensor Class"""
    def __init__(self, addr=0x74, debug=False):  # Initialize using default sensor address
        self.addr = addr >> 1
        self.debug = debug
        self.i2c = Adafruit_I2C(self.addr, -1, debug)

    def ping(self):  # Send signal, -1 if failed
        return self.i2c.write8(0x2, 0xbc)  # Write to register 2

    def read(self):  # Read result, -1 if failed
        return self.i2c.reverseByteOrder(self.i2c.readU16(0x2))

    def setAddr(self, addr):  # Modify the sensor address
        sleep(.2)
        self.i2c.write8(0x2, 0x9a)
        sleep(.003)
        self.i2c.write8(0x2, 0x92)
        sleep(.003)
        self.i2c.write8(0x2, 0x9e)
        sleep(.003)
        self.i2c.write8(0x2, addr)
        self.addr = addr >> 1
        self.i2c = Adafruit_I2C(self.addr, -1, self.debug)
        sleep(.1)

    def disableClampdownSCL(self):
        return self.i2c.write8(0x2, 0xc3)  # Write to register 2

    def enableClampdownSCL(self):
        return self.i2c.write8(0x2, 0xc2)  # Write to register 2

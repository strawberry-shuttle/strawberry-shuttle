__author__ = 'Vijay Ganesan'
# Kingsin KS-10X Ultrasonic Sensor API for BBB
# See ks_test.py for implementation example
# Default address is 0x74

from drivers.BBB_lib.Adafruit_I2C import Adafruit_I2C
from time import sleep

class Ultrasonic_KS:
    """Kingsin KS 103B Ultrasonic Sensor Driver Class
    
    Handles low level communication with KS Ultrasonic Sensors. This class should only be referenced in the ultrasonic sensors class.
    """
    def __init__(self, addr=0x74, debug=False,busnum=-1):  # Initialize using default sensor address
        """
        
        Input: int(addr = sensor I2C address), bool(debug = enable debug messages from i2c), int(busnum = i2c bus ID)
        Output: N/A
        
        Constructor for KS Ultrasonic sensor class. Each instance can control a different ultrasonic sensor. No guarantees made if two instances control the same address.       
        """
        self.addr = addr >> 1
        self.debug = debug
        self.i2c = Adafruit_I2C(self.addr, busnum, debug)

    def ping(self):  # Send signal, -1 if failed
        """
        
        Input: N/A
        Output: NULL or -1 if fail
        
        Send command to the sensor to ping. Returns success, -1 if fail.
        """
        return self.i2c.write8(0x2, 0xbc)  # Write to register 2

    def read(self):  # Read result, -1 if failed
        """
        
        Input: N/A
        Output: int(result) or -1 if fail
        
        Read result of ping. 
        """
        return self.i2c.reverseByteOrder(self.i2c.readU16(0x2))

    def setAddr(self, addr):  # Modify the sensor address
        """
        
        Input: int(addr)
        Output: N/A
        
        Modify sensor address. Note there are limitations on what addresses you can use, check the BBB documentation or use i2cdetect for more information.
        
        Use very sparingly as erasing flash memory is an expensive operation on the lifespan of the sensor.
        """    
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
        """
        
        Input: N/A
        Output: NULL or -1 if fail
        
        Disable locking the SCL line down during a ping. (Enabled by default). Preserved through power loss, this doesn't need to be run more than once.
        """        
        return self.i2c.write8(0x2, 0xc3)  # Write to register 2

    def enableClampdownSCL(self):
        """
        
        Input: N/A
        Output: NULL or -1 if fail
        
        Enable locking the SCL line down during a ping. (Enabled by default). Preserved through power loss, this doesn't need to be run more than once.
        """          
        return self.i2c.write8(0x2, 0xc2)  # Write to register 2

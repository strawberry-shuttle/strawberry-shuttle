__author__ = 'Vijay Ganesan'
# Maxbotix MB-1202 Ultrasonic Sensor API for BBB
# Maxbotix Sensor Documentation: http://maxbotix.com/documents/I2CXL-MaxSonar-EZ_Datasheet.pdf
# See maxbotix_test.py for implementation example

from drivers.BBB_lib.Adafruit_I2C import Adafruit_I2C
from time import sleep

class Ultrasonic_MB:
    """Maxbotix MB1202 I2C Ultrasonic Sensor Class
    
    Handles low level communication with MaxBotix Ultrasonic Sensors. This class should only be referenced in the ultrasonic sensors class.
    """
    def __init__(self, addr=0x70, debug=False,busnum=-1):  # Initialize using default sensor address
        """
        
        Input: int(addr = sensor I2C address), bool(debug = enable debug messages from i2c), int(busnum = i2c bus ID)
        Output: N/A
        
        Constructor for MaxBotix Ultrasonic sensor class. Each instance can control a different ultrasonic sensor. No guarantees made if two instances control the same address.       
        """    
        self.addr = addr
        self.debug = debug
        self.i2c = Adafruit_I2C(self.addr, busnum, debug)

    def setAddr(self, addr):  # Modify the sensor address, WARNING: Use very sparingly, addresses are saved over power cycles
        """
        
        Input: int(addr)
        Output: N/A
        
        Modify sensor address. Note there are limitations on what addresses you can use, check the BBB documentation or use i2cdetect for more information.
        
        Use very sparingly as erasing flash memory is an expensive operation on the lifespan of the sensor.
        """        
        addr <<= 1
        if self.i2c.writeList(0, [0xAA, 0xA5, addr]) > 0:
            return -1
        else:
            self.addr = addr >> 1
            self.i2c = Adafruit_I2C(addr, -1, 0)
            return 1

    def ping(self):  # Send signal, -1 if failed
        """
        
        Input: N/A
        Output: NULL or -1 if fail
        
        Send command to the sensor to ping. Returns success, -1 if fail.
        """    
        return self.i2c.write8_noreg(0x51)
    
    def read(self):  # Read result, -1 if failed
         """
        
        Input: N/A
        Output: int(result) or -1 if fail
        
        Read result of ping. 
        """   
        return self.i2c.reverseByteOrder(self.i2c.readU16(0x0))

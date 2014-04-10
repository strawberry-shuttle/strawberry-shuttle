from Adafruit_I2C import Adafruit_I2C
import Adafruit_BBIO.GPIO as GPIO
from time import sleep

# Maxbotix Sensor Documentation: http://maxbotix.com/documents/I2CXL-MaxSonar-EZ_Datasheet.pdf

i2c = Adafruit_I2C(0x70)  # Default Sensor address. Can be changed with other I2C commands
GPIO.setup("P8_14",GPIO.IN)

while True:
    i2c.write8_noreg(0x51)
    
    if GPIO.input("P8_14"):
        print("HIGH")
    else:
        print("LOW")

    sleep(0.1) #We really only need to wait 50 us to check

    if GPIO.input("P8_14"):
        print("HIGH")
    else:
        print("LOW")

    print i2c.reverseByteOrder(i2c.readU16(0x0))  # Read latest range reading

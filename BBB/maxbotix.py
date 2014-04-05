from Adafruit_I2C import Adafruit_I2C
from time import sleep

# Maxbotix Sensor Documentation: http://maxbotix.com/documents/I2CXL-MaxSonar-EZ_Datasheet.pdf

i2c = Adafruit_I2C(0x70)  # Default Sensor address. Can be changed with other I2C commands

while True:
    i2c.write8(0, 0x51)  # Take Range Reading

    # Not sure what the correct sleep value should be.
    # With the timing analyzer I was seeing that the status pin was high for around 15ms.
    # Even with this 0.1 value it was still saying the device is inaccessible when it was reading really long distances.
    sleep(0.1)
    print i2c.reverseByteOrder(i2c.readU16(0x0))  # Read latest range reading
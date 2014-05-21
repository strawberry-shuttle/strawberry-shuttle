from drivers.ultrasonic_sensors import UltrasonicSensors as US
from time import sleep

u = US()

while 1:
    u.backRightSensor.ping()
    print "%d\n" % (u.backRightSensor.read()/10.0)
    sleep(.1)

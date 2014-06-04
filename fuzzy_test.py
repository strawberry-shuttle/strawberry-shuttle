#Oliver Chen
#tests fuzzy (i think)

import Adafruit_GPIO.GPIO as GPIO
from drivers.motors import Motors
from drivers.ultrasonic_sensors import UltrasonicSensors as us
from control.fuzzy.fuzzy import fuzzyControl as fuzz
from time import sleep

m = Motors()
u = us()
f = fuzz()

GPIO.setup("P8_9", GPIO.IN)

while 1:
    while GPIO.input("P8_9"):
        pass

    while GPIO.input("P8_9"):
        dist = u.updateDistances()
        ang = u.calculateAngle()
        speed = f.fuzzy((ang[0]+ang[1])/2,[dist[2], dist[3], dist[4], dist[5]])
        m.moveForward(speed[0], speed[1])

    m.moveForward(0,0)



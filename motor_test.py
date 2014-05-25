#!/usr/bin/python

from drivers.motors import Motors
from time import sleep, time
from misc import mechInfo
import Adafruit_BBIO.GPIO as GPIO

distance = 1828.0  # distance to travel in cm, ~20 yards
rps = 0.75  # Velocity

rotations = distance/mechInfo.wheelCircumference
t = rotations/rps

GPIO.setup("P8_9", GPIO.IN)   # Forward Button

m = Motors()

while 1:
    while GPIO.input("P8_9"):
        pass

    m.moveForward(0,0.75)
    m.printEncoderSpeeds()
    
    sleep(2)

    currentTime = time()
    finalTime = currentTime + t
    
    while GPIO.input("P8_9") and finalTime-currentTime > 0:
        currentTime = time()
        m.printEncoderSpeeds()

    m.moveForward(0, 0)
    sleep(3)


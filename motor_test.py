#!/usr/bin/python

from drivers.motors import Motors
from time import sleep, time
import mechInfo
import Adafruit_BBIO.GPIO as GPIO

distance = 1828.0 #distance to travel in cm, ~20 yards
rps = 1.0 #Velocity

rotations = distance/mechInfo.wheelCircumference
t = rotations/rps

GPIO.setup("P8_9", GPIO.IN)   # Forward Button

m = Motors(2200)

while 1:
    while GPIO.input("P8_9"):
        pass

    m.moveForward(rps,rps)
    
    sleep(2)

    currenttime = time()
    finaltime = currenttime + t
    

    while GPIO.input("P8_9") and finaltime-currenttime > 0:
        currenttime = time()

    m.moveForward(0,0)
    sleep(3)


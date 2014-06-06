#!/usr/bin/python

from drivers.motors import Motors
from time import sleep, time
from misc import mechInfo
import Adafruit_BBIO.GPIO as GPIO
import argparse

parser = argparse.ArgumentParser(description='Run motors with specified speed')
parser.add_argument('leftSpeed', type=float, nargs='?', default="0.5", help='Speed for the left wheels in revolutions per second')
parser.add_argument('rightSpeed', type=float, nargs='?', default="0.5", help='Speed for the right wheels in revolutions per second')

args = parser.parse_args()
print args.leftSpeed
print args.rightSpeed

distance = 914.0  # distance to travel in cm, ~10 yards
rps = 0.75  # Velocity

rotations = distance/mechInfo.wheelCircumference
t = rotations/rps

GPIO.setup("P8_9", GPIO.IN)   # Forward Button

m = Motors()

while 1:
    while GPIO.input("P8_9"):
        pass

    m.move(args.leftSpeed, args.rightSpeed)
    m.printEncoderSpeeds()
    
    sleep(2)

    currentTime = time()
    finalTime = currentTime + t
    
    while GPIO.input("P8_9") and finalTime-currentTime > 0:
        currentTime = time()
        m.printEncoderSpeeds()

    m.moveForward(0, 0)
    sleep(3)

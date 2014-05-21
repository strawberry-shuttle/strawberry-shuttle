#motor time response test
from __future__ import division
__author__ = 'Evan Racah'
from drivers.motors import Motors
from time import sleep, time
import misc.mechInfo
import random
import math
import Adafruit_BBIO.GPIO as GPIO
from drivers.ultrasonic_sensors import UltrasonicSensors


def takeReadings(t,rps,t0,us):
		t.append(time() - t0)
		ultrasonic.updateDistances()
		us.append(ultrasonic.calculateAngle())
		rps.append(tuple(motor.readEncoderSpeeds()))
		sleep(delay)
		return t,rps,us

def timeResponse(accel,speed,delay,totalTime):
	
	if(totalTime < 2):
		print "Hey totalTime must be greater than 2!"
		return

	while GPIO.input("P8_9"):
	   pass

	t0 = time()
	t = [0]
	ultrasonic.updateDistances()
	us = [ultrasonic.calculateAngle()]
	rps = [tuple(motor.readEncoderSpeeds())]
	motor.moveForward(speed,speed)
	sleep(delay)

	#takes readings for 2 seconds before responding to button to stop it
	while (t[-1] < 2):
	#take readings has access to variables inside timeResponse?
		t,rps,us = takeReadings(t,rps,t0,us)

	#now does same thing but checks for button to stop
	while GPIO.input("P8_9") and ((t[-1] - t0) < 10):
		t,rps,us = takeReadings(t,rps,t0,us)

	motor.moveForward(0,0)

	sleep(3)

	#unzip rps so we have time response of each motor
	lf,rf,lb,rb = zip(*rps)
	rpsData = [lf,rf,lb,rb]
	
	tFile = open('timedata.txt','w')
	for point in t:
		tFile.write("%s\n" % point)
	tFile.close()

	fileString = "RPS_TimeResponse"
	count = 1
	for data in rpsData:
		f = open(fileString + str(count) + ".txt",'w')
		for point in data:
			f.write("%s\n"%point)
		f.close()
		count += 1

	fileString ="UltrasonicAngleData.txt"
	f = open(fileString, 'w')
	for point in us:
		for angle in point:
			angle = angle * 180 / math.pi
			f.write("%s "%angle)
		f.write("\n")
	f.close()
   
if __name__=="__main__":
	accel = 1
	rps = 1.0
	delay = 0.05
	totalTime = 10
	ultrasonic = UltrasonicSensors()
	motor = Motors(accel)
	GPIO.setup("P8_9", GPIO.IN) 
	timeResponse(accel,rps,delay,totalTime)




#motor time response test
from __future__ import division
__author__ = 'Evan Racah'
from drivers.motors import Motors
from time import sleep, time
import misc.mechInfo
import random
import math
import Adafruit_BBIO.GPIO as GPIO


def takeReadings(t,rps,t0):
		t.append(time() - t0)
		rps.append(tuple(motor.readEncoderSpeeds()))
		sleep(delay)
		return t,rps

def timeResponse(accel,speed,delay,totalTime):
	
	if(totalTime < 2):
		print "Hey totalTime must be greater than 2!"
		return

	while GPIO.input("P8_9"):
	   pass

	t0 = time()
	t = [0]
	rps = [tuple(motor.readEncoderSpeeds())]
	motor.moveForward(speed,speed)
	

	sleep(delay)

	#takes readings for 2 seconds before responding to button to stop it
	while (t[-1] < 2):
	#take readings has access to variables inside timeResponse?
		t,rps = takeReadings(t,rps,t0)

	#now does same thing but checks for button to stop
	while GPIO.input("P8_9") and ((t[-1] - t0) < 10):
		t,rps = takeReadings(t,rps,t0)

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
   
if __name__=="__main__":
	accel = 1
	rps = 1.0
	delay = 0.05
	totalTime = 10
	motor = Motors(accel)
	GPIO.setup("P8_9", GPIO.IN) 
	timeResponse(accel,rps,delay,totalTime)




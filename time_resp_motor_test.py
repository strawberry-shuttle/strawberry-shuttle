#motor time response test
from __future__ import division
__author__ = 'Evan Racah'
from drivers.motors import Motors
from time import sleep, time
import mechInfo
import Adafruit_BBIO.GPIO as GPIO


def takeReadings(t,rps,t0):
		t.append(time() - t0)
		rps.append(tuple(motor.readEncoderSpeed()))
		sleep(delay)
		return t,rps

def timeResponse(accel,rps,delay):
	

	while GPIO.input("P8_9"):
    pass

  t0 = time()
  t = [0]

  rps = [tuple(motor.readEncoderSpeed())]
 	motor.moveForward(rps,rps)
	
	sleep(delay)

	#takes readings for 2 seconds before responding to button to stop it
	while t[-1] < 2:
		#take readings has access to variables inside timeResponse?
		t,rps = takeReadings(t,rps,t0)

	#now does same thing but checks for button to stop
	while GPIO.input("P8_9") and ((t[-1] - t0) < 10):
		t,rps = takeReadings(t,rps)

	m.moveForward(0,0)

  sleep(3)

  #unzip rps so we have time response of each motor
  lf,rf,lb,rb = zip(*rps)

   #TODO save these to a file
   #print(lf," ","\n","left_front_time_response.txt")
   #print(t," ","\n","time_.txt")
   
if __name__=="__main__":
	accel = 2200
	rps = 1.0
	delay = 0.1
	motor = Motors(accel)
	GPIO.setup("P8_9", GPIO.IN) 
	timeResponse(accel,rps,delay)




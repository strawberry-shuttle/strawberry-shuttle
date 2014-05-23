#Sensor Covariance Test
#Evan Racah
#5/12/14
__author__ = 'Evan Racah'
import numpy as np
from drivers.motors import Motors
from drivers.ultrasonic_sensors import UltrasonicSensors
import time 
import Adafruit_BBIO.GPIO as GPIO



def test(numMeas):
	while GPIO.input("P8_9"):
	   pass
	
	ultrasonicSensors = UltrasonicSensors()
	rawData = np.zeros(shape=(4,numMeas))
	ultrasonicSensors.updateDistances()
	# motors.frontAngle = np.mean(ultrasonicSensors.calculateAngle())
	motors.backAngle = np.mean(ultrasonicSensors.calculateAngle())
	motors.moveForward(1,1)
	for i in range(numMeas):
		ultrasonicSensors.updateDistances()
		rawData[0,i],rawData[1,i] = ultrasonicSensors.calculateAngle() #right and left ultrasonic sensor
		junk, rawData[2,i] = motors.getEncoderAngles()
		junkToo, rawData[3,i] = motors.getSpeedDiff()
		time.sleep(0.1)

	

	motors.moveForward(0,0)
		
	return np.cov(rawData)

if __name__=="__main__":
	motors = Motors()
	GPIO.setup("P8_9", GPIO.IN) 
	covMatrix = test(50)
	print covMatrix





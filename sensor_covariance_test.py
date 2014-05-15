#Sensor Covariance Test
#Evan Racah
#5/12/14
__author__ = 'Evan Racah'
import numpy as np
from drivers.motors import Motors
from drivers.ultrasonic_sensors import UltrasonicSensors
from time import delay


def test(numMeas):
	motors = Motors()
	ultrasonicSensors = UltrasonicSensors()

	rawData = np.zeros(6,numMeas)
	for i in range(numMeas)
		ultrasonicSensors.updateDistances()
		rawData[0,i],rawData[1,i] = ultrasonicSensors.calculateAngle() #right and left ultrasonic sensor
		rawData[2,i], rawData[3,i] = motors.getEncoderAngles()
		rawData[4,i], rawData[5,i] = motors.getSpeedDiff()
		time.delay(0.1)
		
	return np.cov(rawData)

if __name__=="__main__":
	covMatrix = test(50)
	print covMatrix





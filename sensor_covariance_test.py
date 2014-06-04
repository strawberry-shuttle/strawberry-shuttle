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
    rawData = np.zeros(shape=(6,numMeas))
    ultrasonicSensors.updateDistances()
    # motors.frontAngle = np.mean(ultrasonicSensors.calculateAngle())
    motors.backAngle = np.mean(ultrasonicSensors.calculateAngle())
    motors.moveForward(.5,.5)
    for i in range(numMeas):
        ultrasonicSensors.updateDistances()
        rawData[0,i], rawData[1,i] = ultrasonicSensors.calculateAngle() #right and left ultrasonic sensor
        rawData[2,i], rawData[3,i] = motors.getEncoderAngles(0) #front angle then back
        rawData[4,i], rawData[5,i] = motors.getSpeedDiff() #front diff, then back
        time.sleep(0.1)



    motors.moveForward(0,0)

    return np.cov(rawData)

if __name__=="__main__":
    motors = Motors()
    GPIO.setup("P8_9", GPIO.IN)
    covMatrix = test(50)
    fid = open("Covariance_Matrix.txt", 'w')
    fid.write("%s"%covMatrix)
    fid.close()




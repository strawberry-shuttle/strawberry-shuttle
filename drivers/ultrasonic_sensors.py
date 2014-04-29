from __future__ import division
__author__ = 'Scotty Waggoner'

from drivers.maxbotix import Ultrasonic_MB
from drivers.ks import Ultrasonic_KS


class UltrasonicSensors:

    def __init__(self):
        self.distanceStartDecelerating = 100  # in cm
        self.distanceStop = 50  # in cm

        self.frontSensor = Ultrasonic_MB(0x70)
        self.backSensor = Ultrasonic_MB(0x71)
        self.frontLeftSensor = Ultrasonic_KS(0xD0)
        self.backLeftSensor = Ultrasonic_KS(0xD2)
        self.frontRightSensor = Ultrasonic_KS(0xD4)
        self.backRightSensor = Ultrasonic_KS(0xD6)

        self.frontSensor.ping()
        self.backSensor.ping()
        self.frontLeftSensor.ping()
        self.backLeftSensor.ping()
        self.frontRightSensor.ping()
        self.backRightSensor.ping()

        self.frontDistance = 0
        self.backDistance = 0
        self.frontLeftDistance = 0
        self.backLeftDistance = 0
        self.frontRightDistance = 0
        self.backRightDistance = 0

    def readFront(self):
        newDistance = self.frontSensor.read()
        if newDistance != -1:
            self.frontDistance = newDistance
        self.frontSensor.ping()
        return self.frontDistance

    def readBack(self):
        newDistance = self.backSensor.read()
        if newDistance != -1:
            self.backDistance = newDistance
        self.backSensor.ping()
        return self.backDistance

    def readFrontLeft(self):
        newDistance = self.frontLeftSensor.read()
        if newDistance != -1:
            self.frontLeftDistance = newDistance
        self.frontLeftSensor.ping()
        return self.frontLeftDistance

    def readBackLeft(self):
        newDistance = self.backLeftSensor.read()
        if newDistance != -1:
            self.backLeftDistance = newDistance
        self.backLeftSensor.ping()
        return self.backLeftDistance

    def readFrontRight(self):
        newDistance = self.frontRightSensor.read()
        if newDistance != -1:
            self.frontRightDistance = newDistance
        self.frontRightSensor.ping()
        return self.frontRightDistance

    def readBackRight(self):
        newDistance = self.backRightSensor.read()
        if newDistance != -1:
            self.backRightDistance = newDistance
        self.backRightSensor.ping()
        return self.backRightDistance

    def updateDistances(self):
        #Attempted to order so pings don't interfere with each other. Not sure if this actually matters
        self.readFrontLeft()
        self.readBackRight()
        self.readFront()
        self.readBack()
        self.readBackLeft()
        self.readFrontRight()

    def getSpeedScalingFront(self):
        if self.frontDistance <= self.distanceStop:
            return 0
        return (self.frontDistance - self.distanceStop) / (self.distanceStartDecelerating - self.distanceStop)

    def getSpeedScalingBack(self):
        if self.backDistance <= self.distanceStop:
            return 0
        return (self.backDistance - self.distanceStop) / (self.distanceStartDecelerating - self.distanceStop)

    def calculateAngleAndOffset(self, state): #should give a different angle based on if we are moving forward or backward
        self.updateDistances()
        #TODO: implement calculations. Do we need distance from center also? YES
        return 0

    def endOfFurrow(self):
        if self.frontLeftDistance > 50 and self.frontRightDistance > 50 or self.backLeftDistance > 50 and self.backRightDistance > 50:
            return True
        return False
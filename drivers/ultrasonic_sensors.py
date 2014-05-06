from __future__ import division
from misc import mechInfo

__author__ = 'Scotty Waggoner'

from drivers.maxbotix import Ultrasonic_MB
from drivers.ks import Ultrasonic_KS
import math


class UltrasonicSensors:

    def __init__(self):
        self.distanceStartDecelerating = 100  # in cm
        self.distanceStop = 50  # in cm

        self.frontSensor = Ultrasonic_MB(0x70)
        self.backSensor = Ultrasonic_MB(0x71)
        self.frontLeftSensor = Ultrasonic_KS(0x72)
        self.backLeftSensor = Ultrasonic_KS(0x73)
        self.frontRightSensor = Ultrasonic_KS(0x74)
        self.backRightSensor = Ultrasonic_KS(0x75)

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

    def calculateAngle(self, state):  # TODO: should give a different angle based on if we are moving forward or backward
        return [math.asin((self.frontLeftDistance-self.backLeftDistance)/ mechInfo.distBetweenUS),
                math.asin((self.frontRightDistance-self.backRightDistance)/ mechInfo.distBetweenUS)]

    def endOfFurrow(self):
        distEOF = mechInfo.distForNoFurrow  # cm, distances greater than this are assumed to be at the end of the furrow
        if self.frontLeftDistance > distEOF and self.frontRightDistance > distEOF or self.backLeftDistance > distEOF and self.backRightDistance > distEOF:
            return True
        return False

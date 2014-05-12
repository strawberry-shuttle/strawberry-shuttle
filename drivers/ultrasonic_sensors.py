#TODO: Test
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
        self.frontLeftSensor = Ultrasonic_KS(0xD0)
        self.frontRightSensor = Ultrasonic_KS(0xD2)
        self.backLeftSensor = Ultrasonic_KS(0xD4)
        self.backRightSensor = Ultrasonic_KS(0xD6)

        self.__pingAll()

        self.frontDistance = 0
        self.backDistance = 0
        self.frontLeftDistance = 0
        self.backLeftDistance = 0
        self.frontRightDistance = 0
        self.backRightDistance = 0

    def disableAllClampdownSCL(self):
        #Disables the sensors pulling the clock line low during ranging. Allows commands to be sent to other sensors during ranging
        #self.frontSensor.disableClampdownSCL()
        #self.backSensor.disableClampdownSCL()
        self.frontLeftSensor.disableClampdownSCL()
        self.frontRightSensor.disableClampdownSCL()
        self.backLeftSensor.disableClampdownSCL()
        self.backRightSensor.disableClampdownSCL()

    def __pingAll(self):
        #Attempted to order so pings don't interfere with each other. Not sure if this actually matters
        self.frontLeftSensor.ping()
        self.backRightSensor.ping()
        self.frontSensor.ping()
        self.backSensor.ping()
        self.backLeftSensor.ping()
        self.frontRightSensor.ping()

    def __readFront(self):
        newDistance = self.frontSensor.read()
        if newDistance != -1:
            self.frontDistance = newDistance / 10  # Convert mm to cm
        return self.frontDistance

    def __readBack(self):
        newDistance = self.backSensor.read()
        if newDistance != -1:
            self.backDistance = newDistance / 10  # Convert mm to cm
        return self.backDistance

    def __readFrontLeft(self):
        newDistance = self.frontLeftSensor.read()
        if newDistance != -1:
            self.frontLeftDistance = newDistance / 10  # Convert mm to cm
        return self.frontLeftDistance

    def __readFrontRight(self):
        newDistance = self.frontRightSensor.read()
        if newDistance != -1:
            self.frontRightDistance = newDistance / 10  # Convert mm to cm
        return self.frontRightDistance

    def __readBackLeft(self):
        newDistance = self.backLeftSensor.read()
        if newDistance != -1:
            self.backLeftDistance = newDistance / 10  # Convert mm to cm
        return self.backLeftDistance

    def __readBackRight(self):
        newDistance = self.backRightSensor.read()
        if newDistance != -1:
            self.backRightDistance = newDistance / 10  # Convert mm to cm
        return self.backRightDistance

    def updateDistances(self):
        self.__readFrontLeft()
        self.__readBackRight()
        self.__readFront()
        self.__readBack()
        self.__readBackLeft()
        self.__readFrontRight()

        self.__pingAll()

        return self.frontDistance, self.backDistance, self.frontLeftDistance, self.frontRightDistance, self.backLeftDistance, self.backRightDistance

    def getSpeedScalingFront(self):
        if self.frontDistance <= self.distanceStop:
            return 0
        return (self.frontDistance - self.distanceStop) / (self.distanceStartDecelerating - self.distanceStop)

    def getSpeedScalingBack(self):
        if self.backDistance <= self.distanceStop:
            return 0
        return (self.backDistance - self.distanceStop) / (self.distanceStartDecelerating - self.distanceStop)

    def calculateAngle(self):  # TODO: should give a different angle based on if we are moving forward or backward
        return [math.asin((self.frontLeftDistance - self.backLeftDistance) / mechInfo.distBetweenUS),
                math.asin((self.frontRightDistance - self.backRightDistance) / mechInfo.distBetweenUS)]

    def endOfFurrow(self):
        distEOF = mechInfo.distForNoFurrow  # cm, distances greater than this are assumed to be at the end of the furrow
        if self.frontLeftDistance > distEOF and self.frontRightDistance > distEOF or self.backLeftDistance > distEOF and self.backRightDistance > distEOF:
            return True
        return False

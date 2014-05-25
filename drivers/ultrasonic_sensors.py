from __future__ import division
from misc import mechInfo

__author__ = 'Scotty Waggoner'

from drivers.maxbotix import Ultrasonic_MB
from drivers.ks import Ultrasonic_KS
from misc.log import Log
from misc.median_buffer import MedianBuffer as MB
from time import sleep
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
        #TODO: Change front and back distance to median buffer
        self.frontDistance = self.distanceStartDecelerating + 10  # For testing when front US isn't hooked up. Forces speed scaling value to 1
        self.backDistance = self.distanceStartDecelerating + 10  # For testing when rear US isn't hooked up. Forces speed scaling value to 1
        self.frontLeftDistance = MB()
        self.backLeftDistance = MB()
        self.frontRightDistance = MB()
        self.backRightDistance = MB()

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
            self.frontLeftDistance.insert(newDistance / 10)  # Convert mm to cm
        return self.frontLeftDistance.median

    def __readFrontRight(self):
        newDistance = self.frontRightSensor.read()
        if newDistance != -1:
            self.frontRightDistance.insert(newDistance / 10)  # Convert mm to cm
        return self.frontRightDistance.median

    def __readBackLeft(self):
        newDistance = self.backLeftSensor.read()
        if newDistance != -1:
            self.backLeftDistance.insert(newDistance / 10)  # Convert mm to cm
        return self.backLeftDistance.median

    def __readBackRight(self):
        newDistance = self.backRightSensor.read()
        if newDistance != -1:
            self.backRightDistance.insert(newDistance / 10)  # Convert mm to cm
        return self.backRightDistance.median

    def updateDistances(self):

        self.__readFrontLeft()
        self.__readBackRight()
        #self.__readFront()
        #self.__readBack()
        self.__readBackLeft()
        self.__readFrontRight()

        self.__pingAll()
        sleep(.1)

        return self.frontDistance, self.backDistance, self.frontLeftDistance.median, self.frontRightDistance.median, self.backLeftDistance.median, self.backRightDistance.median

    def getSpeedScalingFront(self):  # TODO: Test
        if self.frontDistance <= self.distanceStop:
            return 0
        elif self.frontDistance >= self.distanceStartDecelerating:
            return 1
        else:
            return (self.frontDistance - self.distanceStop) / (self.distanceStartDecelerating - self.distanceStop)

    def getSpeedScalingBack(self):  # TODO: Test
        if self.backDistance <= self.distanceStop:
            return 0
        elif self.backDistance >= self.distanceStartDecelerating:
            return 1
        return (self.backDistance - self.distanceStop) / (self.distanceStartDecelerating - self.distanceStop)

    def calculateAngle(self):  # TODO: should give a different angle based on if we are moving forward or backward
        return [math.atan((self.frontLeftDistance.median - self.backLeftDistance.median) / mechInfo.distBetweenUS),
                -1*math.atan((self.frontRightDistance.median - self.backRightDistance.median) / mechInfo.distBetweenUS)]

    def endOfFurrow(self):  # TODO: Test
        distEOF = mechInfo.distForNoFurrow  # cm, distances greater than this are assumed to be at the end of the furrow
#        l = Log()
#        l.ShowDebug("Distances: %u %u %u %u" % (self.frontLeftDistance.median,self.frontRightDistance.median,self.backLeftDistance.median,self.backRightDistance.median))
        if self.frontLeftDistance.median > distEOF and self.frontRightDistance.median > distEOF or self.backLeftDistance.median > distEOF and self.backRightDistance.median > distEOF:
            retur
        return False

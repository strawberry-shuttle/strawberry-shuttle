from __future__ import division
__author__ = 'Scotty Waggoner'

from drivers.maxbotix import Ultrasonic_MB


class UltrasonicSensors:

    def __init__(self):
        self.distanceStartDecelerating = 100  # in cm
        self.distanceStop = 50  # in cm

        self.frontSensor = Ultrasonic_MB(0x70)
        self.backSensor = Ultrasonic_MB(0x71)
        #self.frontLeftSensor = Ultrasonic_KS103(0xD0)
        #self.backLeftSensor = Ultrasonic_KS103(0xD2)
        #self.frontRightSensor = Ultrasonic_KS103(0xD4)
        #self.backRightSensor = Ultrasonic_KS103(0xD6)

        self.frontSensor.ping()
        self.backSensor.ping()
        #self.frontLeftSensor.ping()
        #self.backLeftSensor.ping()
        #self.frontRightSensor.ping()
        #self.backRightSensor.ping()

        self.frontDistance = 0
        self.backDistance = 0
        self.frontLeftDistance = 0
        self.backLeftDistance = 0
        self.frontRightDistance = 0
        self.backRightDistance = 0

    def readFront(self):
        self.frontDistance = self.frontSensor.read()
        self.frontSensor.ping()
        return self.frontDistance

    def getSpeedScalingFront(self):
        if self.frontDistance <= self.distanceStop:
            return 0
        return (self.frontDistance - self.distanceStop) / (self.distanceStartDecelerating - self.distanceStop)

    def getSpeedScalingBack(self):
        if self.backDistance <= self.distanceStop:
            return 0
        return (self.backDistance - self.distanceStop) / (self.distanceStartDecelerating - self.distanceStop)

    def readBack(self):
        self.backDistance = self.backSensor.read()
        self.backSensor.ping()
        return self.backDistance

    def updateDistances(self):
        self.readFront()
        self.readBack()

    def calculateAngle(self):
        self.updateDistances()
        #TODO: implement calculations. Do we need distance from center also?
        return 0

    def endOfFurrow(self):
        if self.frontLeftDistance > 50 and self.frontRightDistance > 50 or self.backLeftDistance > 50 and self.backRightDistance > 50:
            return True
        return False
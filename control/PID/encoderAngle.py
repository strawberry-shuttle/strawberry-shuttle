#Evan Racah
#class that keeps track of angle of robot
#from encoders
from __future__ import division
import time
from drivers.motors import Motors
import mechInfo

class EncoderProtractor:
    def __init__(self):
        self.angle = 0  # initial angle
        self.encLeftPrev = 0
        self.encRightPrev = 0
        self.encLeftDiff = 0
        self.encRightDiff = 0

    def getAngle(self, enc):
        encLeft = enc[0]
        encRight = enc[1]

        self.encLeftDiff = encLeft - self.encLeftPrev
        self.encRightDiff = encRight - self.encRightPrev
        d1 = self.encLeftDiff * mechInfo.wheelCircumference
        d2 = self.encRightDiff * mechInfo.wheelCircumference
        self.angle += ((d1 - d2) / mechInfo.robotDiameter)
        self.encLeftPrev = encLeft
        self.encRightPrev = encRight
        return self.angle

if __name__== "__main__":
    encAngle = EncoderProtractor(0, 12.5, 10)
    motors = Motors()
    motors.moveForward(3, 4)
    while True:
        encc = motors.readEncoderSpeeds()
        motors.printEncoders()
        encoderAngle = encAngle.getAngle(encc)
        print "Angle from encoders ", encoderAngle
        time.sleep(0.25)  # To see debug info

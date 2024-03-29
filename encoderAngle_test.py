#Evan Racah
#class that keeps track of angle of robot
#from encoders
from __future__ import division
import time
from drivers.motors import Motors

class EncoderProtractor:
    def __init__(self, initialAngle, wheelCircumference, robotDiameter):
        self.angle = initialAngle
        self.robotDiameter = robotDiameter
        self.wheelCircum = wheelCircumference
        self.encLeftPrev = 0
        self.encRightPrev = 0
        self.encLeftDiff = 0
        self.encRightDiff = 0

    def getAngle(self, enc):
        encLeft = enc[0]
        encRight = enc[1]

        self.encLeftDiff = encLeft - self.encLeftPrev
        self.encRightDiff = encRight - self.encRightPrev
        d1 = self.encLeftDiff * self.wheelCircum
        d2 = self.encRightDiff * self.wheelCircum
        self.angle = ((d1 - d2) / self.robotDiameter) + self.angle
        self.encLeftPrev = encLeft
        self.encRightPrev = encRight
        return self.angle

if __name__== "__main__":
	encAngle = EncoderProtractor(0, 12.5, 10);
	motor = Motors()
	motor.moveForward(3,3)
	while(1):
		encc = motor.readEncoderSpeeds()
		motor.printEncoders()
		encoderAngle = encAngle.getAngle(encc)
		print "Angle from encoders ", encoderAngle
		time.sleep(0.25)  # To see debug info





     

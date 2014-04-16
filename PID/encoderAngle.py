#Evan Racah
#class that keeps track of angle of robot
#from encoders
from __future__ import division
import time
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
	encc = [10, 10]
	while(1):
		print encAngle.getAngle(encc)
		encc[0]+= 5
		encc[1]+= 10
		time.sleep(1)

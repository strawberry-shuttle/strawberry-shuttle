#Evan Racah
#class that keeps track of angle of robot
#from encoders
from BBB.roboclaw import Roboclaw

class EncoderProtractor(object):
	def __init__(self, initialAngle, wheelCircumfrence, robotDiameter, encoderResolution): #these should be doubles
		self.angle = initialAngle
		self.shuttleDiam = robotDiameter
		self.wheelCircum = wheelCircumfrence
		self.encResolution = encoderResolution #how many encoder counts in 1 rev
		self.enc1Prev = 0
		self.enc2Prev = 0
		robo = Roboclaw(0x80, "/dev/ttyO1")

	def getEncoderCounts(): #sets enc1 and enc2 does not return them
		if (test1 = robo.read_m1_encoder())[0] != -1: #make sure successfully reads encoders
			self.enc1 = test1[0]
		if (test2 = robo.read_m2_encoder())[0] != -1:
			self.enc2 = test2[0]
		#if encoder reading unsuccessful enc1 and enc2 will remain their previous values

	def getAngle(self):
		self.enc1Diff = self.enc1 - self.enc1Prev
		self.enc2Diff = self.enc2 - self.enc2Prev
		d1 = self.enc1Diff * self.wheelCircum / self.encResolution
		d2 = self.enc2Diff * self.weelCircum / self.encResolution
		self.angle = ((d1 - d2) / self.shuttleDiam) + self.angle
		self.enc1Prev = self.enc1
		self.enc2Prev = self.enc2
		return self.angle


#Evan Racah
#tests PID on whole system

from PID import PIDControl
from BBB.roboclaw import Roboclaw
from cv2 import KalmanFilter
#import vijay/oliver's ultrasonic function


pidCoefficients = [1, 0, 0] #still need to figure these out
maxSpeed = 100 #we need to test what the max rotational velocity of the wheels on the robot are
pid = PIDControl(0,[1,0,0],maxSpeed)
#encProt = EncoderProtractor(0, wheelCircum, robotDiam, encoderResolution)

"""INITIALIZE KALMAN FILTER"""
#we might need to use numpy based matrices for kalman implementation
kalman = KalmanFilter(nstateValues, nMeasurementValues, nControlInputs)
#kalman.transition_matrix = ....
#kalman.measurement_matrix = ....
#kalman.control_matrix = ....
"""#################"""


#########initiate ultrasonic object here#######

claw = Roboclaw(0x80, "/dev/ttyO1")

curM1 = 50 
curM2 = 50
claw.m1_forward(curM1) #I dont know what a good speed is yet
claw.m2_forward(curM2)

#kalman.predict(0)

while(1):
	#read ultrasonic values
	#encAngle = encProt.getAngle()
	#measurement = [encAngle, ultrasonic] or using numpy
	#kalman.correct(measurement)
	#filteredAngle = kalman.state_post
	"""Angle Convention: postive filtered angle means robot is tilted
	so motor 1 is ahead of motor 2""""
	speedDiff = pid.update(filteredAngle)
	"""Current speedDiff Convention: positive speedDiff means M2 
	turns faster than M1"""
	
	curM1 -= speedDiff / 2
	curM2 += speedDiff / 2 
	claw.m1_forward(curM1)
	claw.m2_forward(curM2)
	#kalman.predict(speedDiff)
	



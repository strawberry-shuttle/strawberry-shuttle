#Oliver Chen
#simple fuzzy logic implementation

from BBB.roboclaw import Roboclaw

frontclaw = Roboclaw(add, port) #the roboclaw controlling the front motors
backclaw = Roboclaw(add, port) #the roboclaw controlling the back motors
avgspeed = 50; #average forward speed of the robot

def setmotors(turnrate): #sets the speed of the motors based on the required turnrate
	frontclaw.m1_forward(avgspeed*turnrate)		#.5 means straight (50% power to both motors)
	backclaw.m1_forward(avgspeed*turnrate)		#>.5 turns to the right (>50% power to the right motor, <50% to the left motor)
	frontclaw.m2_forward(avgspeed*(1-turnrate))	#<.5 turns to the left (<50% power to the left motor, >50% to the right motor)
	backclaw.m2_forward(avgspeed*(1-turnrate))

def fuzzy(angle, distance): #reads in the angle (0 means straight, >0 means right, <0 means left)
	a = -.01 * angle		#and the distance from the walls (.5 means centered, .75 means halfway to the right wall, etc)
	if distance > .6:	#a is how much the turnrate is affected by the current angle
		d = .6 - d		#d is how much the turnrate should be affected by the current distance from he walls
	if distance < .4:	#may need to multiply a and d by constants if the robot reacts too quickly or too slowly to either variable
		d = .4 - d
	setmotors(.5 + a + d)
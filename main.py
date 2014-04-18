__author__ = 'Scotty Waggoner, Vijay Ganesan'
import time
from enum import Enum
from drivers.motors import Motors
from drivers.ultrasonic_sensors import UltrasonicSensors
from PID.encoderAngle import EncoderProtractor
from PID.PID import PIDControl
#from kalman.kalman import Kalman


class State(Enum):
    estop = 1
    canceled = 2 #This is 'murica
    stopped = 3 #Either estop or canceled
    moveForward = 4
    moveBackward = 8
    moving = 12 #Either moving forward or backwards

    #not sure if we need new states for move away 10ft or if we can just set a timer to move to the canceled state or set a flag to check encoder counts
    #moveForwardDistance = 5
    #moveBackwardDistance = 6


class Button(Enum):
    noBtn = 0
    redBtn = 1
    forwardBtn = 2 #Send in back and Follow in front
    backBtn = 4 #Send in front and Follow in back
    frontBumper = 8
    backBumper = 16


class Control:
    def __init__(self):
        self.motors = Motors()
        self.ultrasonicSensors = UltrasonicSensors()
        self.currentState = State.moveForward  # Should start out as State.canceled once robot is stand-alone
        self.encoderProtractor = EncoderProtractor(0, 12.5, 10)  # What units should these be in?
        self.PID = PIDControl(0, [1, 0, 0], 100)  # update these values

    def changeState(self, newState):
        if newState == State.canceled:
            #stop with deceleration
            self.motors.stop()
        elif newState == State.estop:
            #stop instantly (no deceleration) - used for bumper or really close ultrasonic measurements
            self.motors.estop()
            time.sleep(2)
            self.changeState(State.canceled)
        elif newState == State.moveForward:
            #self.motors.moveForward()
            pass
        elif newState == State.moveBackward:
            #self.motors.moveBackward()
            pass
            #elif newState == State.moveForwardDistance:
            #self.motors.moveForward()
            #elif newState == State.moveBackwardDistance:
            #self.motors.moveBackward()
        self.currentState = newState

    def detectButtonState(self):
        return Button.noBtn

    def updateState(self):
            buttonState = self.detectButtonState() #Detect buttons and bumpers from GPIO
            end_of_furrow = self.ultrasonicSensors.endOfFurrow()  # Information from side ultrasonics

            state = self.currentState
            moving = state & State.moving
            stopped = state & State.stopped

            #Emergency Stop if red button, or bumpers hit in moving state
            if ( (buttonState & Button.redBtn) or ( (buttonState & (Button.backBumper | Button.frontBumper) ) and moving ) ):
                self.currentState = State.estop
            elif end_of_furrow: #Slow down and stop if end of furrow
                self.currenState = State.canceled
            #Move Forward if back bumper and not moving, or the front button is hit
            elif ( (buttonState & Button.frontBtn) or ((buttonState & Button.backBumper) and stopped) ):
                self.currentState = State.moveForward
            #Move Backwards if front bumper and not moving, or the back button is hit
            elif ( (buttonState & Button.backBtn) or ((buttonState & Button.frontBumper) and stopped) ):
                self.currentState = State.moveBackward

    def moveInFurrow(self):
        #Request most recent values from side ultrasonic

        #Request most recent values from camera

        #Request most recent values from encoders
        encoderAngle = self.encoderProtractor.getAngle(self.motors.readEncoders())

        #Call angle calculation for ultrasonic

        #Call Kalman filter with most recent values

        #Run PID with those values
        angle = self.PID.update(0)

        #TODO: update speed from angle, Kalman, and PID
        leftSpeed = 4
        rightSpeed = 4

        #Update motor speeds
        if self.currentState == State.moveForward:
            #Slow down if obstacle
            leftSpeed *= self.ultrasonicSensors.getSpeedScalingFront()
            rightSpeed *= self.ultrasonicSensors.getSpeedScalingFront()

            self.motors.moveForward(leftSpeed, rightSpeed)
        elif self.currentState == State.moveBackward:
            #Slow down if obstacle
            leftSpeed *= self.ultrasonicSensors.getSpeedScalingBack()
            rightSpeed *= self.ultrasonicSensors.getSpeedScalingBack()

            self.motors.moveBackward(leftSpeed, rightSpeed)

        #Print debug info
        self.motors.printCurrents()
        self.motors.printEncoders()
        print "Angle from encoders ", encoderAngle
        time.sleep(0.25)  # To see debug info

    def run(self):  # Main function
        while True:
            self.ultrasonicSensors.updateDistances()  # Used to get data for end of furrow detection, obstacle detection, and distances for navigation

            #Update btn and bumper states
            self.updateState()
            if self.currentState > State.cancelled:  # Robot not stopped
                self.moveInFurrow()  # Handles all the navigation, speeds, etc...

robot = Control()
robot.run()

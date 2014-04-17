__author__ = 'Scotty Waggoner'
import time
from enum import Enum
from drivers.motors import Motors
from PID.encoderAngle import EncoderProtractor
from PID.PID import PIDControl
#from kalman.kalman import Kalman

class State(Enum):
    estop = 1
    canceled = 2
    moveForward = 3
    moveBackward = 4
    #not sure if we need new states for move away 10ft or if we can just set a timer to move to the canceled state or set a flag to check encoder counts
    #moveForwardDistance = 5
    #moveBackwardDistance = 6


class Control:

    def __init__(self):
        self.motors = Motors()
        self.currentState = State.moveForward  # Should start out as State.canceled once robot is stand-alone

        # init to false until buttons and bumpers are implemented
        self.redBtn = False
        self.frontYellowBtn = False
        self.backYellowBtn = False
        self.frontGreenBtn = False
        self.backGreenBtn = False
        self.frontBumper = False
        self.backBumper = False

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

    def detectObstacles(self):
        if self.currentState == State.moveForward:
            #Request reading from front ultrasonic
            pass
        elif self.currentState == State.moveBackward:
            #Request reading from back ultrasonic
            pass

    def detectEndOfFurrow(self):
        if self.currentState == State.moveForward:
            #Request reading from the 2 side front ultrasonics
            pass
        elif self.currentState == State.moveBackward:
            #Request reading from the 2 side back ultrasonics
            pass

    def updateState(self):
        if self.redBtn or (self.currentState == State.moveForward and self.frontBumper) or (self.currentState == State.moveBackward and self.backBumper):
            self.changeState(State.estop)
        elif self.frontYellowBtn or self.backGreenBtn:
            self.changeState(State.moveForward)
        elif self.frontGreenBtn or self.backYellowBtn:
            self.changeState(State.moveBackward)
            #or front/back ultrasonic detects close object: then slow down and eventually stop
            #or end of furrow detected: then change state to canceled

    def moveInFurrow(self):
        #Request most recent values from side ultrasonic

        #Request most recent values from camera

        #Request most recent values from encoders
        encoderAngle = self.encoderProtractor.getAngle(self.motors.readEncoders())

        #Call angle calculation for ultrasonic

        #Call Kalman filter with most recent values

        #Run PID with those values
        angle = self.PID.update(0)

        #Update motor speeds
        if self.currentState == State.moveForward:
            self.motors.moveForward(4, 4)
        elif self.currentState == State.moveBackward:
            self.motors.moveBackward(4, 4)

        #Print debug info
        self.motors.printCurrents()
        self.motors.printEncoders()
        print "Angle from encoders ", encoderAngle
        time.sleep(0.25)  # To see debug info

    def run(self):
        while True:
            self.detectObstacles()
            self.detectEndOfFurrow()

            #Update btn and bumper states
            self.updateState()

            if self.currentState > State.canceled:  # Robot not stopped
                self.moveInFurrow()

    robot = Control()
    robot.run()
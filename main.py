__author__ = 'Scotty Waggoner, Vijay Ganesan, Evan Racah'
import time
from enum import Enum
from control.state import StateManager
from control.state import State #Enum class
from control.state import Button #Enum class
from drivers.motors import Motors
from drivers.ultrasonic_sensors import UltrasonicSensors
from control.PID.encoderAngle import EncoderProtractor, getRPSDiff
from control.PID.PID import PIDControl
from kalman.kalman import KalmanFilterLinear, setUpMatrices
import mechInfo
import numpy as np

#POSITIVEW RPS DIFF MEANS LEFT WHEEL MOVING FASTER THAN RIGHT
#POsitive angle means turned to right -> we could change this
'''
class Button(Enum):
    noBtn = 0
    redBtn = 1
    forwardBtn = 2 #Send in back and Follow in front
    backBtn = 4 #Send in front and Follow in back
    frontBumper = 8
    backBumper = 16
    
class State(Enum):
    estop = 1
    canceled = 2 #This is 'murica
    stopped = 3 #Either estop or canceled
    moveForward = 4
    moveBackward = 8
    moving = 12 #Either moving forward or backwards
'''

class Control:
    def __init__(self):
        self.motors = Motors()
        self.ultrasonicSensors = UltrasonicSensors()
        self.stateManager = StateManager()
        self.encoderProtractor = EncoderProtractor(0, 12.5, 10)  # What units should these be in?
        self.PID = PIDControl(0, [1, 0, 0], 100)  # update these values
        self.kalman = KalmanFilterLinear(setUpMatrices(dt))
        self.commandedRPSDiff = 0
        self.robotRPS = mechInfo.desiredSpeed

    def changeState(self, newState):
        self.stateManager.changeState(self,newState)
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
            buttonState = self.detectButtonState()  # Detect buttons and bumpers from GPIO
            end_of_furrow = self.ultrasonicSensors.endOfFurrow()  # Information from side ultrasonics
            self.stateManager.updateState()

    def getMeasurements(self):
        ultrasonicAngle = self.ultrasonicSensors.calculateAngle()
        #cameraAngle =
        RPSDiff = getRPSDiff(self.motors.readEncoders())
        return np.matrix([[ultrasonicAngle], [RPSDiff]]) #camera angle eventually

    def move(self,speed,RPSDiff):
        RPSIncrement = RPSDiff / 2
        if self.currentState == State.moveForward:
            self.motors.moveForward(speed + RPSIncrement, speed - RPSIncrement)
        elif self.currentState == State.moveBackward:
            self.motors.moveBackward(speed + RPSIncrement, speed - RPSIncrement)

    def obstacleCheck():
        if self.currentState == State.moveForward:
            self.robotRPS = self.ultrasonicSensors.getSpeedScalingFront()
        elif self.currentState == State.moveBackward:
            self.robotRPS = self.ultrasonicSensors.getSpeedScalingBack()

    def determineSpeedInput():
        self.measVector = self.getMeasurements()
        self.controlVector = np.matrix([[self.commandedRPSDiff]])
        self.kalman.Step(self.controlVector,self.measVector)
        self.curAngle = kalman.GetCurrentState()
        return self.PID.update(self.curAngle)

    def moveInFurrow(self, speed):
        self.robotRPS = speed #set robotrps to initial speed desired
        self.obstacleCheck() #slow robotrps if obstacle detected
        self.commandedRPSDiff = self.determineSpeedInput() #get speedinput from meas/kalman/pid
        self.move(self.robotRPS,self.commandedRPSDiff) #move forward or backward


    def run(self):  # Main function
        while True:
             #Update btn and bumper states
            self.updateState()
            if self.currentState > State.canceled:  # Robot not stopped but wait nobtn is 0??
                self.moveInFurrow(speed)  # Handles all the navigation, speeds, etc...
            else:
                if self.currentState == State.canceled:
                    self.motors.stop()
                else:
                    self.motors.estop()
                self.currentState = State.stopped
          
                

if __name__ == "__main__":
    robot = Control()
    robot.run()

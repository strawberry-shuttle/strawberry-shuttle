__author__ = 'Scotty Waggoner, Vijay Ganesan, Evan Racah'
from control.state.state import StateManager
from control.state.state import State  # Enum class
from drivers.motors import Motors
from drivers.ultrasonic_sensors import UltrasonicSensors
from drivers.buttons import Buttons
from control.PID.encoderAngle import EncoderProtractor
from control.PID.PID import PIDControl
from kalman.kalman import KalmanFilterLinear, setUpMatrices
import mechInfo #constants
# TODO: Update constants in mechInfo
import numpy as np

#POSITIVEW RPS DIFF MEANS LEFT WHEEL MOVING FASTER THAN RIGHT
#POsitive angle means turned to right -> we could change this
#Speed unit is Revolutions per Second (RPS)

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
        self.buttons = Buttons()
        self.encoderProtractor = EncoderProtractor()
        self.PID = PIDControl(0, [1, 0, 0], 100)  # update these values
        self.kalman = KalmanFilterLinear(setUpMatrices())
        self.commandedRPSDiff = 0
        self.desiredSpeed = self.motors.maxSpeed() * 0.9  # scaled by a (currently arbitrary) percent of max speed

    def obstacleSpeedScaling(self):
        if self.stateManager.currentState == State.moveForward:
            return self.ultrasonicSensors.getSpeedScalingFront()
        elif self.stateManager.currentState == State.moveBackward:
            return self.ultrasonicSensors.getSpeedScalingBack()

    def getMeasurements(self):
        self.ultrasonicSensors.updateDistances()
        leftUltrasonicAngle,rightUltrasonicAngle = self.ultrasonicSensors.calculateAngle()
        backEncoderAngle, frontEncoderAngle = self.motors.getEncoderAngles()
        #cameraAngle =
        speedDiffFront, speedDiffBack = self.motors.getSpeedDiff()
        #TODO: add speedDiffBack to matrix also and camera angle
        return np.matrix([[leftUltrasonicAngle],[rightUltrasonicAngle],[backEncoderAngle], [frontEncoderAngle], [speedDiffFront], [speedDiffBack]]) #camera angle eventually

    def determineSpeedInput(self):
        self.measVector = self.getMeasurements()
        self.controlVector = np.matrix([[self.commandedRPSDiff]])
        self.kalman.Step(self.controlVector, self.measVector)
        self.curAngle = self.kalman.GetCurrentState()
        return self.PID.update(self.curAngle)

    def moveInFurrow(self):
        scaledSpeed = self.desiredSpeed * self.obstacleSpeedScaling()  # slow robot if obstacle detected
        self.commandedRPSDiff = self.determineSpeedInput()  # get differential steering data from meas/kalman/pid
        speedIncrement = self.commandedRPSDiff / 2
        if self.stateManager.currentState == State.moveForward:
            self.motors.moveForward(scaledSpeed + speedIncrement, scaledSpeed - speedIncrement)
        elif self.stateManager.currentState == State.moveBackward:
            self.motors.moveBackward(scaledSpeed + speedIncrement, scaledSpeed - speedIncrement)

    def run(self):  # Main function
        while True:
            #TODO: Get information from cameras
            self.buttons.updateButtonStates() #TODO: Testing button states
            self.stateManager.updateState(self.buttons.buttonState, self.ultrasonicSensors.endOfFurrow())
            if ~(self.stateManager.currentState & State.stopped):  # Robot not stopped but wait nobtn is 0??
                self.moveInFurrow()  # Handles all the navigation, speeds, etc...
            else: #TODO: Don't stop motors repeatedly, doing this repeatedly might send too many serial packets to the Roboclaw
                if self.stateManager.currentState & State.canceled:
                    self.motors.stop()
                elif self.stateManager.currentState & State.estop:
                    self.motors.estop()

if __name__ == "__main__":
    robot = Control()
    robot.run()

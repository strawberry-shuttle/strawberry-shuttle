__author__ = 'Scotty Waggoner, Vijay Ganesan, Evan Racah'
from control.state.state import StateManager
from control.state.state import State  # States
from drivers.motors import Motors
from drivers.ultrasonic_sensors import UltrasonicSensors
from drivers.buttons import Buttons
from control.PID.PID import PIDControl
from control.kalman.kalman import KalmanFilter
# TODO: Update constants in mechInfo
from misc import mechInfo
from misc.log import Log
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
        self.PID = PIDControl(0, (1, 0, 0))  # update these values
        self.kalman = KalmanFilter()
        self.commandedRPSDiff = 0
        self.desiredSpeed = mechInfo.desiredSpeed

    def obstacleSpeedScaling(self):
        if self.stateManager.currentState == State.moveForward:
            return self.ultrasonicSensors.getSpeedScalingFront()
        elif self.stateManager.currentState == State.moveBackward:
            return self.ultrasonicSensors.getSpeedScalingBack()
        else:
            l = Log()
            l.ShowDebug("Function should not be called in state %d" % self.stateManager.currentState);
            return 0 #Should never happen, will force stop

    def getMeasurements(self):
        self.ultrasonicSensors.updateDistances()
        leftUltrasonicAngle, rightUltrasonicAngle = self.ultrasonicSensors.calculateAngle()
        backEncoderAngle, frontEncoderAngle = self.motors.getEncoderAngles(self.curAngle)
        speedDiffFront, speedDiffBack = self.motors.getSpeedDiff()
        return np.matrix([[leftUltrasonicAngle], [rightUltrasonicAngle], [backEncoderAngle],
                          [frontEncoderAngle], [speedDiffFront], [speedDiffBack]])  # camera angle eventually

    def determineSpeedInput(self):
        measVector = self.getMeasurements()
        controlVector = np.matrix([[self.commandedRPSDiff]])
        self.kalman.Step(controlVector, measVector)
        self.curAngle = self.kalman.getCurrentAngle()
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
            self.buttons.updateButtonStates()  # TODO: Testing button states
            self.stateManager.updateState(self.buttons.buttonState, self.ultrasonicSensors.endOfFurrow())
            if not (self.stateManager.currentState & State.stopped):  # Robot not stopped
                self.moveInFurrow()  # Handles all the navigation, speeds, etc...
            else:  # TODO: Don't stop motors repeatedly, doing this repeatedly might send too many serial packets to the Roboclaw
                if self.stateManager.currentState & State.canceled:
                    self.motors.stop()
                elif self.stateManager.currentState & State.estop:
                    self.motors.estop()

if __name__ == "__main__":
    robot = Control()
    robot.run()

__author__ = 'Vijay Ganesan'
#Main class for state machine

from enum import Enum


class State(Enum):
    estop = 1
    canceled = 2 #  This is 'murica
    stopped = 3 #  Either estop or canceled
    moveForward = 4
    moveBackward = 8
    moving = 12 #  Either moving forward or backwards


class ButtonState(Enum):
    noBtn = 0
    stopBtn = 1
    forwardBtn = 2 #  Send in back and Follow in front
    backBtn = 4 #  Send in front and Follow in back
    frontBumper = 8
    backBumper = 16


class StateManager:
    def __init__(self):
        self.currentState = State.moveForward
        #self.current = State.canceled

    def getCurrentState(self):
        return self.currentState

    def updateState(self, button_state, end_of_furrow):
        state = self.current
        moving = state & State.moving
        stopped = state & State.stopped

        #Emergency Stop if red button, or bumpers hit in moving state
        if ( (button_state & ButtonState.stopBtn) or ( (buttonState & (ButtonState.backBumper | ButtonState.frontBumper) ) and moving ) ):
            self.currentState = State.estop
        elif end_of_furrow: #Slow down and stop if end of furrow
            self.currentState = State.canceled
        #Move Forward if back bumper and not moving, or the front button is hit
        elif ( (button_state & ButtonState.frontBtn) or ((buttonState & ButtonState.backBumper) and stopped) ):
            self.currentState = State.moveForward
        #Move Backwards if front bumper and not moving, or the back button is hit
        elif ( (button_state & ButtonState.backBtn) or ((buttonState & ButtonState.frontBumper) and stopped) ):
            self.currentState = State.moveBackward
        return self.currentState
        
    def changeState(self, newState):
        self.currentState = newState

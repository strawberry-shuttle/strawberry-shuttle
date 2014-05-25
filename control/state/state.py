#TODO: Test
__author__ = 'Vijay Ganesan'
#Main class for state machine

from drivers.buttons import ButtonState
from misc.log import Log

class State:
    estop = 1
    canceled = 2 #  This is 'murica
    stopped = 3 #  Either estop or canceled
    moveForward = 4
    moveBackward = 8
    moving = 12 #  Either moving forward or backwards

class StateManager:
    def __init__(self):
        #self.currentState = State.moveForward
        self.currentState = State.canceled

    def updateState(self, button_state, end_of_furrow):
        state = self.currentState
        moving = state & State.moving
        stopped = state & State.stopped

        #Emergency Stop if red button, or bumpers hit in moving state
        if (button_state & ButtonState.stopBtn) or ( (button_state & (ButtonState.backBumper | ButtonState.frontBumper) ) and moving):
            self.currentState = State.canceled #Could be estop
        elif end_of_furrow: #Slow down and stop if end of furrow
            self.currentState = State.canceled
        #Move Forward if back bumper and not moving, or the front button is hit
        elif ( (button_state & ButtonState.forwardBtn) or ((button_state & ButtonState.backBumper) and stopped) ):
            self.currentState = State.moveForward
        #Move Backwards if front bumper and not moving, or the back button is hit
        elif ( (button_state & ButtonState.backBtn) or ((button_state & ButtonState.frontBumper) and stopped) ):
            self.currentState = State.moveBackward
	l = Log()
	# l.ShowDebug("Current State %d" % self.currentState)
        return self.currentState
        
    def changeState(self, newState):
        self.currentState = newState

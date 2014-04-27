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
   
class Button(Enum):
    noBtn = 0
    redBtn = 1
    forwardBtn = 2 #  Send in back and Follow in front
    backBtn = 4 #  Send in front and Follow in back
    frontBumper = 8
    backBumper = 16
	
class StateManager:
    def __init__(self):
        self.currentState = State.moveForward
        #self.current = State.canceled
    def currentState(self):
        return self.currentState

    def updateState(self, button_state, end_of_furrow):
        state = self.current
        moving = state & State.moving
        stopped = state & State.stopped

        #Emergency Stop if red button, or bumpers hit in moving state
        if ( (button_state & Button.redBtn) or ( (buttonState & (Button.backBumper | Button.frontBumper) ) and moving ) ):
            self.currentState = State.estop
        elif end_of_furrow: #Slow down and stop if end of furrow
            self.currenState = State.canceled
        #Move Forward if back bumper and not moving, or the front button is hit
        elif ( (button_state & Button.frontBtn) or ((buttonState & Button.backBumper) and stopped) ):
            self.currentState = State.moveForward
        #Move Backwards if front bumper and not moving, or the back button is hit
        elif ( (button_state & Button.backBtn) or ((buttonState & Button.frontBumper) and stopped) ):
            self.currentState = State.moveBackward
        return self.currentState
        
    def changeState(self, newState):
        self.currentState = newState
        
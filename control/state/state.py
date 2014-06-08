__author__ = 'Vijay Ganesan'

from drivers.buttons import ButtonState
from misc.log import Log

class State:
    """State class
    
    Effectively an enum for readability and convenience when handling states.
    
    Possible states are:
    
    estop
    canceled
    stopped (either estop or canceled)
    moveForward
    moveBackward
    moving (either moveForward or moveBackward)
    """
    estop = 1
    canceled = 2
    stopped = 3 #  Either estop or canceled
    moveForward = 4
    moveBackward = 8
    moving = 12 #  Either moving forward or backwards

class StateManager:
    """State Manager Class
    
    Class that handles state control based on user I/O and sensor information.
    """
    def __init__(self):
        """
        
        Input: N/A
        Output: N/A
        
        Constructor for state manager class. Initial state defaults to canceled to prevent it from moving as soon as the system starts.
        """
        #self.currentState = State.moveForward
        self.currentState = State.canceled

    def updateState(self, button_state, end_of_furrow):
        """
        
        Input: int(button_state), bool(end_of_furrow)
        Output: int(self.currentState)
        
        Changes or maintains the current state based on user input or sensor information, this function needs to be modified based on what new sensors are added.
        """
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
        
        #l = Log()
        #l.ShowDebug("Current State %d" % self.currentState)
        
        return self.currentState
        
    def changeState(self, newState):
        """
        
        Input: int(newState)
        Output: N/A
        
        Changes the state to a new state. Obsolete.
        """    
        self.currentState = newState

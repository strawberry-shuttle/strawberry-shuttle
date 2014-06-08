from __future__ import division
__author__ = 'Scotty Waggoner'

import Adafruit_BBIO.GPIO as GPIO
from misc.log import Log

class ButtonState:
    """ButtonState class
    
    Effectively an enum for readability and convenience when handling buttons.
    
    Possible buttons are:
    
    noBtn
    stopBtn
    forwardBtn
    backBtn
    frontBumper
    backBumper
    """
    noBtn = 0
    stopBtn = 1
    forwardBtn = 2 #  Send in back and Follow in front
    backBtn = 4 #  Send in front and Follow in back
    frontBumper = 8
    backBumper = 16

class Buttons:
    """Button input handling class.
    
    Class that handles configuration and button states.
    """
    def __init__(self):
        """
        
        Input: N/A
        Output: N/A
        
        Constructor for button handler class. Configures pins for I/O. See BBB_Pinouts for BBB wiring configuration.
        """
        GPIO.setup("P8_7", GPIO.IN)   # Front Bumper
        GPIO.setup("P8_8", GPIO.IN)   # Back Bumper
        GPIO.setup("P8_9", GPIO.IN)   # Forward Button
        GPIO.setup("P8_10", GPIO.IN)  # Backward Button
        GPIO.setup("P8_11", GPIO.IN)  # Stop Button

        GPIO.add_event_detect("P8_7", GPIO.FALLING)   # Front Bumper
        GPIO.add_event_detect("P8_8", GPIO.FALLING)   # Back Bumper
        GPIO.add_event_detect("P8_9", GPIO.FALLING)   # Forward Button
        GPIO.add_event_detect("P8_10", GPIO.FALLING)  # Back Button
        GPIO.add_event_detect("P8_11", GPIO.FALLING)  # Stop Button

        self.buttonState = ButtonState.noBtn

    def updateButtonStates(self):
        """
        
        Input: N/A
        Output: int(self.buttonState)
        
        Check input pins for button presses and record them into button state, and then return it.
        
        """    
        self.buttonState = ButtonState.noBtn
        if GPIO.event_detected("P8_7"):
            self.buttonState |= ButtonState.frontBumper
        if GPIO.event_detected("P8_8"):
            self.buttonState |= ButtonState.backBumper
        if GPIO.event_detected("P8_9"):
            self.buttonState |= ButtonState.forwardBtn
        if GPIO.event_detected("P8_10"):
            self.buttonState |= ButtonState.backBtn
        if GPIO.event_detected("P8_11"):
            self.buttonState |= ButtonState.stopBtn
        #l = Log()
        #l.ShowDebug("ButtonState: %d" % self.buttonState)
        return self.buttonState

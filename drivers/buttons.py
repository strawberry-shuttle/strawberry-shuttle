from __future__ import division
__author__ = 'Scotty Waggoner'

import Adafruit_BBIO.GPIO as GPIO
from control.state.state import ButtonState

class Buttons:

    def __init__(self):
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

    def updateButtonStates(self):
        buttonState = 0
        if GPIO.event_detected("P8_7"):
            buttonState |= ButtonState.frontBumper
        if GPIO.event_detected("P8_8"):
            buttonState |= ButtonState.backBumper
        if GPIO.event_detected("P8_9"):
            buttonState |= ButtonState.forwardBtn
        if GPIO.event_detected("P8_10"):
            buttonState |= ButtonState.backBtn
        if GPIO.event_detected("P8_11"):
            buttonState |= ButtonState.stopBtn
        return buttonState
__author__ = 'Scotty Waggoner'

from drivers.roboclaw_lib import Roboclaw
import Adafruit_BBIO.UART as UART


UART.setup("UART1")

frontMotors = Roboclaw(0x80, "/dev/ttyO1")
rearMotors = Roboclaw(0x81, "/dev/ttyO1")
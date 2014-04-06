from roboclaw import Roboclaw
import Adafruit_BBIO.UART as UART

 
UART.setup("UART1")

robo = Roboclaw(0x80, "/dev/ttyO1")

# Usage: from roboclaw_repl import robo
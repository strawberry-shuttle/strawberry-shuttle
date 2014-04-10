__author__ = 'Scotty Waggoner'

from drivers.roboclaw_lib import Roboclaw
import Adafruit_BBIO.UART as UART

# Motor control is currently implemented with Duty Cycle and Acceleration. This needs to be changed to use
# set_mixed_speed_i_accel once encoders are implemented

class Motors:

    def __init__(self):
        UART.setup("UART1")

        self.front_motors = Roboclaw(0x80, "/dev/ttyO1")
        self.back_motors = Roboclaw(0x81, "/dev/ttyO1")

    def stop(self):
        self.front_motors.set_mixed_duty_accel(500, 0, 500, 0)
        #self.back_motors.set_mixed_duty_accel(500, 0, 500, 0)

    def estop(self):
        self.front_motors.set_mixed_duty_accel(65535, 0, 500, 0)
        #self.back_motors.set_mixed_duty_accel(65535, 0, 500, 0)

    def moveForward(self, left, right):
        #speed is 0-1500
        left = abs(left)
        right = abs(right)
        self.front_motors.set_mixed_duty_accel(1000, left, 1000, right)
        #self.back_motors.set_mixed_duty_accel(1000, left, 1000, right)

    def moveBackward(self, left, right):
        #speed is 0-1500
        left = -abs(left)
        right = -abs(right)
        self.front_motors.set_mixed_duty_accel(1000, left, 1000, right)
        #self.back_motors.set_mixed_duty_accel(1000, left, 1000, right)

    def print_currents(self):
        m1cur, m2cur = self.front_motors.read_currents()
        print "Current M1: ", m1cur/10.0, " M2: ", m2cur/10.0
        #m1cur, m2cur = self.back_motors.read_currents()
        #print "Current M1: ", m1cur/10.0, " M2: ", m2cur/10.0
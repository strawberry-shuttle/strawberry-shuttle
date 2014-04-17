from __future__ import division
__author__ = 'Scotty Waggoner'

from drivers.roboclaw_lib import Roboclaw
import Adafruit_BBIO.UART as UART

# Standalone usage in Python REPL:
# from drivers.motors import Motors
# motors = Motors()

class Motors:

    def __init__(self):
        UART.setup("UART1")

        self.front_motors = Roboclaw(0x80, "/dev/ttyO1")
        self.back_motors = Roboclaw(0x81, "/dev/ttyO1")

        self.encoderResolution = 1024
        self.maxSpeed = 4400  # Units of pulses per second. 100% of power is given at this encoder reading (~4.3 rev/sec)
        self.acceleration = 2200  # pulses per second per second

        self.p = int(1.0 * 65536)
        self.i = int(0.5 * 65536)
        self.d = int(0.25 * 65536)
        self.front_motors.set_m1_pidq(self.p, self.i, self.d, self.maxSpeed)
        self.front_motors.set_m2_pidq(self.p, self.i, self.d, self.maxSpeed)
        #self.back_motors.set_m1_pidq(self.p, self.i, self.d, self.maxSpeed)
        #self.back_motors.set_m2_pidq(self.p, self.i, self.d, self.maxSpeed)

    def revToPulses(self, revolutions):  # Convert revolutions per second to pulses per second
        return int(revolutions * self.encoderResolution)

    def pulsesToRev(self, pulses):  # Convert pulses per second to revolutions per second
        return pulses / self.encoderResolution

    def stop(self):  # Stop with deceleration
        self.front_motors.set_m1_speed_accel(self.acceleration, 0)
        self.front_motors.set_m2_speed_accel(self.acceleration, 0)
        #self.back_motors.set_m1_speed_accel(self.acceleration, 0)
        #self.back_motors.set_m2_speed_accel(self.acceleration, 0)

    def estop(self):  # Stop instantly
        self.front_motors.m1_forward(0)
        self.front_motors.m2_forward(0)
        #self.back_motors.m1_forward(0)
        #self.back_motors.m2_forward(0)

    def moveForward(self, left, right):
        left = self.revToPulses(abs(left))
        right = self.revToPulses(abs(right))
        self.front_motors.set_m1_speed_accel(self.acceleration, left)
        self.front_motors.set_m2_speed_accel(self.acceleration, right)
        #self.back_motors.set_m1_speed_accel(self.acceleration, left)
        #self.back_motors.set_m2_speed_accel(self.acceleration, right)

    def moveBackward(self, left, right):
        left = self.revToPulses(-abs(left))
        right = self.revToPulses(-abs(right))
        self.front_motors.set_m1_speed_accel(self.acceleration, left)
        self.front_motors.set_m2_speed_accel(self.acceleration, right)
        #self.back_motors.set_m1_speed_accel(self.acceleration, left)
        #self.back_motors.set_m2_speed_accel(self.acceleration, right)

    def readEncoders(self):
        #Average
        left = self.front_motors.read_m1_speed()[0]
        #left += self.back_motors.read_m1_speed()[0]
        #left /= 2
        right = self.front_motors.read_m2_speed()[0]
        #right += self.back_motors.read_m2_speed()[0]
        #right /= 2

        #Convert pulses per second to revolutions per second
        left = self.pulsesToRev(left)
        right = self.pulsesToRev(right)
        return left, right  # Returns values in revolutions per second

    def printCurrents(self):
        m1cur, m2cur = self.front_motors.read_currents()
        print "Current Left: ", m1cur/100.0, "A Right: ", m2cur/100.0, "A"
        #m1cur, m2cur = self.back_motors.read_currents()
        #print "Current M1: ", m1cur/100.0, "A M2: ", m2cur/100.0, "A"

    def printEncoders(self):
        left, right = self.readEncoders()
        print "Speed Left: ", left, " rev/sec Right: ", right/100.0, " rev/sec"
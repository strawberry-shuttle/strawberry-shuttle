from __future__ import division
__author__ = 'Scotty Waggoner'

from drivers.roboclaw_lib import Roboclaw
import Adafruit_BBIO.UART as UART
import mechInfo #constants

# Standalone usage in Python REPL:
# from drivers.motors import Motors
# motors = Motors()


class Motors:

    def __init__(self):
        UART.setup("UART1")

        self.front_motors = Roboclaw(0x80, "/dev/ttyO1")
        self.back_motors = Roboclaw(0x81, "/dev/ttyO1")

        self.encoderResolution = 1024
        self.maxPulsesPerSecond = mechInfo.maxPPS  # Units of pulses per second. 100% of power is given at this encoder reading
        self.acceleration = 2200  # pulses per second per second

        self.p = int(1.0 * 65536)
        self.i = int(0.5 * 65536)
        self.d = int(0.25 * 65536)
        self.front_motors.set_m1_pidq(self.p, self.i, self.d, self.maxPulsesPerSecond)
        self.front_motors.set_m2_pidq(self.p, self.i, self.d, self.maxPulsesPerSecond)
        #self.back_motors.set_m1_pidq(self.p, self.i, self.d, self.maxSpeed)
        #self.back_motors.set_m2_pidq(self.p, self.i, self.d, self.maxSpeed)

        self.encoderRevLeftFront = 0
        self.encoderRevRightFront = 0
        self.encoderRevLeftBack = 0
        self.encoderRevRightBack = 0

    def revToPulses(self, revolutions):  # Convert revolutions per second to pulses per second
        return int(revolutions * self.encoderResolution)

    def pulsesToRev(self, pulses):  # Convert pulses per second to revolutions per second
        return pulses / self.encoderResolution

    def maxSpeed(self):
        return self.pulsesToRev(self.maxPulsesPerSecond)

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

    def readEncoderSpeeds(self):
        #Read speeds in pulses per 125th of a second
        leftFront = self.front_motors.read_m1_inst_speed()[0]
        rightFront = self.front_motors.read_m2_inst_speed()[0]
        leftBack = self.back_motors.read_m1_inst_speed()[0]
        rightBack = self.back_motors.read_m2_inst_speed()[0]

        #Convert pulses per 125th of a second to revolutions per second
        leftFront = self.pulsesToRev(leftFront * 125)
        rightFront = self.pulsesToRev(rightFront * 125)
        leftBack = self.pulsesToRev(leftBack * 125)
        rightBack = self.pulsesToRev(rightBack * 125)
        return leftFront, rightFront, leftBack, rightBack  # Returns values in revolutions per second

    def readEncoderDistanceTraveled(self):
        underflowConst = 0b00000001
        overflowConst = 0b00000100
        maxCount = 4294967295

        #Read register values containing pulses count
        leftFront, leftFrontStatus = self.front_motors.read_m1_encoder()
        rightFront, rightFrontStatus = self.front_motors.read_m1_encoder()
        leftBack, leftBackStatus = self.back_motors.read_m1_encoder()
        rightBack, rightBackStatus = self.back_motors.read_m1_encoder()

        #Adjust for underflow and overflow
        if leftFrontStatus & underflowConst:
            self.encoderRevLeftFront += maxCount
        elif leftFrontStatus & overflowConst:
            self.encoderRevLeftFront -= maxCount

        if rightFrontStatus & underflowConst:
            self.encoderRevRightFront += maxCount
        elif rightFrontStatus & overflowConst:
            self.encoderRevRightFront -= maxCount

        if leftBackStatus & underflowConst:
            self.encoderRevLeftBack += maxCount
        elif leftBackStatus & overflowConst:
            self.encoderRevLeftBack -= maxCount

        if rightBackStatus & underflowConst:
            self.encoderRevRightBack += maxCount
        elif rightBackStatus & overflowConst:
            self.encoderRevRightBack -= maxCount

        #Convert pulses to revolutions
        leftFront = self.pulsesToRev(leftFront)
        rightFront = self.pulsesToRev(rightFront)
        leftBack = self.pulsesToRev(leftBack)
        rightBack = self.pulsesToRev(rightBack)

        #Find difference in revolutions since last time function was called
        leftFrontDiff = leftFront - self.encoderRevLeftFront
        rightFrontDiff = rightFront - self.encoderRevRightFront
        leftBackDiff = leftBack - self.encoderRevLeftBack
        rightBackDiff = rightBack - self.encoderRevRightBack

        #Save current revolutions
        self.encoderRevLeftFront = leftFront
        self.encoderRevRightFront = rightFront
        self.encoderRevLeftBack = leftBack
        self.encoderRevRightBack = rightBack

        return leftFrontDiff, rightFrontDiff, leftBackDiff, rightBackDiff  # Returns values in revolutions

    def getSpeedDiff(self):
        leftFront, rightFront, leftBack, rightBack = self.readEncoderSpeeds()
        return leftFront - rightFront, leftBack - rightBack

    def printCurrents(self):
        m1cur, m2cur = self.front_motors.read_currents()
        print "Current Left: ", m1cur/100.0, "A Right: ", m2cur/100.0, "A"
        #m1cur, m2cur = self.back_motors.read_currents()
        #print "Current M1: ", m1cur/100.0, "A M2: ", m2cur/100.0, "A"

    def printEncoders(self):
        left, right = self.readEncoderSpeeds()
        print "Speed Left: ", left, " rev/sec Right: ", right/100.0, " rev/sec"
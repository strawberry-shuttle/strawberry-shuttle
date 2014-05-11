#TODO: Test readEncoderDistanceTraveled overflow and underflow
#TODO: Test Angle calculation and speed diff
from __future__ import division
from misc import mechInfo

__author__ = 'Scotty Waggoner'

from drivers.roboclaw_lib import Roboclaw
import Adafruit_BBIO.UART as UART
import time

# Standalone usage in Python REPL:
# from drivers.motors import Motors; m = Motors()


class Motors:

    def __init__(self, acceleration=1):
        UART.setup("UART1")
        UART.setup("UART2")
        self.backAngle = 0
        self.frontAngle = 0
        self.front_motors = Roboclaw(0x80, "/dev/ttyO1")
        self.back_motors = Roboclaw(0x81, "/dev/ttyO2")

        self.encoderResolution = 1024
        self.maxPulsesPerSecond = mechInfo.maxPPS  # Units of pulses per second. 100% of power is given at this encoder reading
        self.acceleration = self.revToPulses(acceleration)  # Units of revolutions per second, default = 1

        self.p = int(1.0 * 65536)
        self.i = int(0.5 * 65536)
        self.d = int(0.25 * 65536)
        self.front_motors.set_m1_pidq(self.p, self.i, self.d, self.maxPulsesPerSecond)
        self.front_motors.set_m2_pidq(self.p, self.i, self.d, self.maxPulsesPerSecond)
        self.back_motors.set_m1_pidq(self.p, self.i, self.d, self.maxPulsesPerSecond)
        self.back_motors.set_m2_pidq(self.p, self.i, self.d, self.maxPulsesPerSecond)

        self.encoderRevFrontLeft = 0
        self.encoderRevFrontRight = 0
        self.encoderRevBackLeft = 0
        self.encoderRevBackRight = 0

        self.readEncoderDistanceTraveled()  # Clears junk output from this function

    def revToPulses(self, revolutions):  # Convert revolutions per second to pulses per second
        return int(revolutions * self.encoderResolution)

    def pulsesToRev(self, pulses):  # Convert pulses per second to revolutions per second
        return pulses / self.encoderResolution

    def maxSpeed(self):
        return self.pulsesToRev(self.maxPulsesPerSecond)

    def stop(self):  # Stop with deceleration
        self.front_motors.set_m1_speed_accel(self.acceleration, 0)
        self.front_motors.set_m2_speed_accel(self.acceleration, 0)
        self.back_motors.set_m1_speed_accel(self.acceleration, 0)
        self.back_motors.set_m2_speed_accel(self.acceleration, 0)

    def estop(self):  # Stop instantly
        self.front_motors.m1_forward(0)
        self.front_motors.m2_forward(0)
        self.back_motors.m1_forward(0)
        self.back_motors.m2_forward(0)

    def moveForward(self, left, right):
        left = self.revToPulses(abs(left))
        right = self.revToPulses(abs(right))
        self.front_motors.set_m1_speed_accel(self.acceleration, left)
        self.front_motors.set_m2_speed_accel(self.acceleration, right)
        self.back_motors.set_m1_speed_accel(self.acceleration, left)
        self.back_motors.set_m2_speed_accel(self.acceleration, right)

    def moveBackward(self, left, right):
        left = self.revToPulses(-abs(left))
        right = self.revToPulses(-abs(right))
        self.front_motors.set_m1_speed_accel(self.acceleration, left)
        self.front_motors.set_m2_speed_accel(self.acceleration, right)
        self.back_motors.set_m1_speed_accel(self.acceleration, left)
        self.back_motors.set_m2_speed_accel(self.acceleration, right)

    def readEncoderSpeedsPPS(self):
        #Read speeds in pulses per second
        leftFront = self.front_motors.read_m1_speed()[0]
        rightFront = self.front_motors.read_m2_speed()[0]
        leftBack = self.back_motors.read_m1_speed()[0]
        rightBack = self.back_motors.read_m2_speed()[0]

        return leftFront, rightFront, leftBack, rightBack  # Returns values in pulses per second

    def readEncoderSpeeds(self):
        #Read speeds in pulses per second
        return map(self.pulsesToRev, self.readEncoderSpeedsPPS())  # Returns values in revolutions per second

    def readEncoderDistanceTraveled(self):
        underflowConst = 0b00000001
        overflowConst = 0b00000100
        maxCount = 4294967295

        #Read register values containing pulses count
        frontLeft, frontLeftStatus = self.front_motors.read_m1_encoder()
        frontRight, frontRightStatus = self.front_motors.read_m2_encoder()
        backLeft, backLeftStatus = self.back_motors.read_m1_encoder()
        backRight, backRightStatus = self.back_motors.read_m2_encoder()

        #Adjust for underflow and overflow
        if frontLeftStatus & underflowConst:
            self.encoderRevFrontLeft += maxCount
        elif frontLeftStatus & overflowConst:
            self.encoderRevFrontLeft -= maxCount

        if frontRightStatus & underflowConst:
            self.encoderRevFrontRight += maxCount
        elif frontRightStatus & overflowConst:
            self.encoderRevFrontRight -= maxCount

        if backLeftStatus & underflowConst:
            self.encoderRevBackLeft += maxCount
        elif backLeftStatus & overflowConst:
            self.encoderRevBackLeft -= maxCount

        if backRightStatus & underflowConst:
            self.encoderRevBackRight += maxCount
        elif backRightStatus & overflowConst:
            self.encoderRevBackRight -= maxCount

        #Convert pulses to revolutions
        frontLeft = self.pulsesToRev(frontLeft)
        frontRight = self.pulsesToRev(frontRight)
        backLeft = self.pulsesToRev(backLeft)
        backRight = self.pulsesToRev(backRight)

        #Find difference in revolutions since last time function was called
        frontLeftDiff = frontLeft - self.encoderRevFrontLeft
        frontRightDiff = frontRight - self.encoderRevFrontRight
        backLeftDiff = backLeft - self.encoderRevBackLeft
        backRightDiff = backRight - self.encoderRevBackRight

        #Save current revolutions
        self.encoderRevFrontLeft = frontLeft
        self.encoderRevFrontRight = frontRight
        self.encoderRevBackLeft = backLeft
        self.encoderRevBackRight = backRight

        return frontLeftDiff, frontRightDiff, backLeftDiff, backRightDiff  # Returns values in revolutions

    def getDiffAngle(self, encLeftDiff, encRightDiff, angle):
        d1 = encLeftDiff * (mechInfo.wheelCircumference / self.encoderResolution)
        d2 = encRightDiff * (mechInfo.wheelCircumference / self.encoderResolution)
        angle += ((d1 - d2) / mechInfo.robotWidth)
        return angle

    def getEncoderAngles(self):
        leftFrontDiff, rightFrontDiff, leftBackDiff, rightBackDiff = self.readEncoderDistanceTraveled()
        self.backAngle = self.getDiffAngle(leftFrontDiff, rightFrontDiff, self.frontAngle)
        self.frontAngle = self.getDiffAngle(leftBackDiff, rightBackDiff, self.backAngle)
        return [self.backAngle, self.frontAngle]

    def getSpeedDiff(self):
        leftFront, rightFront, leftBack, rightBack = self.readEncoderSpeeds()
        return leftFront - rightFront, leftBack - rightBack

    def printCurrents(self):
        m1cur, m2cur = self.front_motors.read_currents()
        print "Front Currents - Left: ", m1cur/100.0, "A Right: ", m2cur/100.0, "A"
        m1cur, m2cur = self.back_motors.read_currents()
        print "Back  Currents - Left: ", m1cur/100.0, "A Right: ", m2cur/100.0, "A"

    def printEncoderSpeeds(self):
        frontLeft, frontRight, backLeft, backRight = self.readEncoderSpeeds()
        print "Front Speeds - Left: ", frontLeft, " rev/sec Right: ", frontRight, " rev/sec"
        print "Back  Speeds - Left: ", backLeft, " rev/sec Right: ", backRight, " rev/sec"

if __name__ == "__main__":
    m = Motors()
    m.front_motors.m1_forward(50)
    time.sleep(2)
    m.front_motors.m1_forward(0)

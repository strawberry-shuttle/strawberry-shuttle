#TODO: Test Angle calculation - values seemed really small and I'm not sure how changes in directions will be handled. Also when should the angle get reset if ever? Do we NEED the cumulative angle?
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

        self.front_motors = Roboclaw(0x80, "/dev/ttyO1")
        self.back_motors = Roboclaw(0x81, "/dev/ttyO2")

        self.encoderResolution = 1024
        self.maxPulsesPerSecond = mechInfo.maxPPS  # Units of pulses per second. 100% of power is given at this encoder reading
        self.acceleration = self.__revToPulses(acceleration)  # Units of revolutions per second, default = 1

        self.p = int(1.0 * 65536)
        self.i = int(0.5 * 65536)
        self.d = int(0.25 * 65536)
        self.front_motors.set_m1_pidq(self.p, self.i, self.d, self.maxPulsesPerSecond)
        self.front_motors.set_m2_pidq(self.p, self.i, self.d, self.maxPulsesPerSecond)
        self.back_motors.set_m1_pidq(self.p, self.i, self.d, self.maxPulsesPerSecond)
        self.back_motors.set_m2_pidq(self.p, self.i, self.d, self.maxPulsesPerSecond)

        self.encoderPulsesFrontLeft = 0
        self.encoderPulsesFrontRight = 0
        self.encoderPulsesBackLeft = 0
        self.encoderPulsesBackRight = 0

        self.frontAngle = 0
        self.backAngle = 0

        self.readEncoderDistanceTraveled()  # Clears junk output from this function

    def __revToPulses(self, revolutions):  # Convert revolutions per second to pulses per second
        return int(revolutions * self.encoderResolution)

    def __pulsesToRev(self, pulses):  # Convert pulses per second to revolutions per second
        return pulses / self.encoderResolution

    def maxSpeed(self):
        return self.__pulsesToRev(self.maxPulsesPerSecond)

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
        left = self.__revToPulses(abs(left))
        right = self.__revToPulses(abs(right))
        self.front_motors.set_m1_speed_accel(self.acceleration, left)
        self.front_motors.set_m2_speed_accel(self.acceleration, right)
        self.back_motors.set_m1_speed_accel(self.acceleration, left)
        self.back_motors.set_m2_speed_accel(self.acceleration, right)

    def moveBackward(self, left, right):
        left = self.__revToPulses(-abs(left))
        right = self.__revToPulses(-abs(right))
        self.front_motors.set_m1_speed_accel(self.acceleration, left)
        self.front_motors.set_m2_speed_accel(self.acceleration, right)
        self.back_motors.set_m1_speed_accel(self.acceleration, left)
        self.back_motors.set_m2_speed_accel(self.acceleration, right)

    def __readEncoderSpeedsPPS(self):
        #Read speeds in pulses per second
        leftFront = self.front_motors.read_m1_speed()[0]
        rightFront = self.front_motors.read_m2_speed()[0]
        leftBack = self.back_motors.read_m1_speed()[0]
        rightBack = self.back_motors.read_m2_speed()[0]

        return leftFront, rightFront, leftBack, rightBack  # Returns values in pulses per second

    def readEncoderSpeeds(self):
        #Read speeds in pulses per second
        return map(self.__pulsesToRev, self.__readEncoderSpeedsPPS())  # Returns values in revolutions per second

    def __readEncoderDistanceTraveledPulses(self):
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
            self.encoderPulsesFrontLeft += maxCount
        elif frontLeftStatus & overflowConst:
            self.encoderPulsesFrontLeft -= maxCount

        if frontRightStatus & underflowConst:
            self.encoderPulsesFrontRight += maxCount
        elif frontRightStatus & overflowConst:
            self.encoderPulsesFrontRight -= maxCount

        if backLeftStatus & underflowConst:
            self.encoderPulsesBackLeft += maxCount
        elif backLeftStatus & overflowConst:
            self.encoderPulsesBackLeft -= maxCount

        if backRightStatus & underflowConst:
            self.encoderPulsesBackRight += maxCount
        elif backRightStatus & overflowConst:
            self.encoderPulsesBackRight -= maxCount

        #Find difference in revolutions since last time function was called
        frontLeftDiff = abs(frontLeft - self.encoderPulsesFrontLeft)
        frontRightDiff = abs(frontRight - self.encoderPulsesFrontRight)
        backLeftDiff = abs(backLeft - self.encoderPulsesBackLeft)
        backRightDiff = abs(backRight - self.encoderPulsesBackRight)

        #Save current revolutions
        self.encoderPulsesFrontLeft = frontLeft
        self.encoderPulsesFrontRight = frontRight
        self.encoderPulsesBackLeft = backLeft
        self.encoderPulsesBackRight = backRight

        return frontLeftDiff, frontRightDiff, backLeftDiff, backRightDiff  # Returns values in number of pulses

    def readEncoderDistanceTraveled(self):
        return map(self.__pulsesToRev, self.__readEncoderDistanceTraveledPulses())  # Returns values in number of revolutions

    def getDiffAngle(self, encLeftDiff, encRightDiff):
        d1 = encLeftDiff * (mechInfo.wheelCircumference / self.encoderResolution)
        d2 = encRightDiff * (mechInfo.wheelCircumference / self.encoderResolution)
        return (d1 - d2) / mechInfo.robotWidth

    def getEncoderAngles(self):
        leftFrontDiff, rightFrontDiff, leftBackDiff, rightBackDiff = self.readEncoderDistanceTraveled()
        self.frontAngle += self.getDiffAngle(leftFrontDiff, rightFrontDiff)
        self.backAngle += self.getDiffAngle(leftBackDiff, rightBackDiff)
        return [self.frontAngle, self.backAngle]

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

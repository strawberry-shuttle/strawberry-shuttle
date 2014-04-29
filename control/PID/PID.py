'''


@author: Evan Racah
'''

import time


class PIDControl(object):
    def __init__(self, setpoint, coefficients, maxSpeed):  #maxSpeed is in rads/sec i think?
        self.maxDiff = maxSpeed
        self.setpoint = setpoint
        self.lastTime = time.time()
        self.kP, self.kI, self.kD = coefficients
        self.errorTotal = 0.0
        self.previousError = 0.0
        #self.max_error = 180
        #self.min_error = -180

    def update(self, measurement):
        self.now = time.time()
        self.timeInterval = self.now - self.lastTime
        self._calcErrorTerms(measurement)
        input = self._calcInput()
        self.lastTime = self.now
        self.previousError = self.error
        return input

    def set_set_point(self, setpoint):
        self.setpoint = setpoint

    def _calcErrorTerms(self, measurement):
        self.error = self.setpoint - measurement
        self.errorTotal += self.error * self.timeInterval
        self.dError = (self.error - self.previousError) / self.timeInterval

    def _calcInput(self):
        self.P = self.kP * self.error
        self.I = self.kI * self.errorTotal * self.timeInterval
        self.D = self.kD * (self.dError / self.timeInterval)
        return self.P + self.I + self.D

 

__author__ = 'Evan Racah'


import time


class PIDControl(object):
    def __init__(self, setpoint, coefficients): 
        self.setpoint = setpoint
        self.lastTime = time.time()
        self.kP, self.kI, self.kD = coefficients
        self.errorTotal = 0.0
        self.previousError = 0.0
        #self.max_error = 180
        #self.min_error = -180

    def update(self, measurement):
        #update time stuff
        self.now = time.time()
        self.timeInterval = self.now - self.lastTime

        #calculate the three error terms
        self.error = self.setpoint - measurement
        self.errorTotal += self.error * self.timeInterval
        self.dError = (self.error - self.previousError) / self.timeInterval

        #multiply by coefficents
        P = self.kP * self.error
        I = self.kI * self.errorTotal
        D = self.kD * self.dError
        
        #update time and error stuff
        self.lastTime = self.now
        self.previousError = self.error

        return P + I + D

    def set_set_point(self, setpoint):
        self.setpoint = setpoint


 

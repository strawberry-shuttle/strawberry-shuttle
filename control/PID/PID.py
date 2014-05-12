__author__ = 'Evan Racah'


import time


class PIDControl(object):
    def __init__(self, setPoint, coefficients):
        self.setPoint = setPoint
        self.lastTime = time.time()
        self.kP, self.kI, self.kD = coefficients
        self.errorTotal = 0.0
        self.previousError = 0.0
        #self.max_error = 180
        #self.min_error = -180

    def update(self, measurement):
        #update time stuff
        now = time.time()
        timeInterval = now - self.lastTime

        #calculate the three error terms
        error = self.setPoint - measurement
        self.errorTotal += error * timeInterval
        dError = (error - self.previousError) / timeInterval

        #multiply by coefficents
        P = self.kP * error
        I = self.kI * self.errorTotal
        D = self.kD * dError
        
        #update time and error stuff
        self.lastTime = now
        self.previousError = error

        return P + I + D

    def set_set_point(self, setPoint):
        self.setPoint = setPoint


 

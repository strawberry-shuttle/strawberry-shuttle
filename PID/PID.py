'''
Created on Aug 20, 2013

@author: ejracah
'''
import time

class PIDControl(object):
    def __init__(self,setpoint,coefficients):
        self.setpoint = setpoint
        self.lastTime = time.time()
        self.kP, self.kI, self.kD = coefficients
        self.errorTotal = 0.0
        self.previousError = 0.0
        self.max_error = 180
        self.min_error = -180

    def update(self, measurement):

        #get new time interval
        self.now = time.time()
        self.timeInterval = self.now - self.lastTime
        
        #calculate error terms
        self.error = max(min(self.setpoint - measurement, self.max_error),self.min_error)
        self.errorTotal += self.error * self.timeInterval
        self.dError = (self.error - self.previousError) / self.timeInterval
        
        
      
        #calculate the three PID terms
        self.P = self.kP * self.error
        self.I = self.kI * self.errorTotal * self.timeInterval
        self.D = self.kD * (self.dError / self.timeInterval)

        #set new previous termsp
        self.lastTime = self.now
        self.previousError = self.error
        
      
        
        return self.P + self.I + self.D

    def set_set_point(self,setpoint):
        self.setpoint = setpoint

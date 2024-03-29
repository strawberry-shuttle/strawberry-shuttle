from __future__ import division, absolute_import

__author__ = 'Evan Racah, Greg Czerniak'
#Kalman Filter 
#Evan Racah
#This class was written  by Greg Czerniak with some modifications
#and can be found here: http://greg.czerniak.info/guides/kalman1/


#we need numpy here...

#TODO: calculate dt thru timing
import numpy as np
import time
from misc.mechInfo import overallTransferFunction 


# Implements a linear Kalman filter.
class KalmanFilter(object):
    """
     I know, I know, VIJAY: you can turn this into a readme if you want, but nice to have now, while working on it
     A: State transition matrix.
     B: Control matrix.
     H: Observation matrix.
     current_state_estimate: state estimate.
     current_prob_estimate: covariance estimate.
     Q: Estimated error in process.
     R: Estimated error in measurements.
    """
    def __init__(self,ultrasonicAngle):
        self.A, self.B, self.H, self.current_state_estimate, \
            self.current_prob_estimate, self.Q, self.R = self.setUpMatrices(ultrasonicAngle)

        self.lastTime = time.time()

    def GetCurrentState(self):
        return self.current_state_estimate
        
    def getCurrentAngle(self):
        return float(self.current_state_estimate[0])

    def Step(self, control_vector, measurement_vector):
        now = time.time()
        timeStep = now - self.lastTime
        self.A[0, 1] = overallTransferFunction * timeStep  # mechInfo.G * timeStep
        self.lastTime = now
        #---------------------------Prediction step-----------------------------
        
        predicted_state_estimate = self.A * self.current_state_estimate + self.B * control_vector
        predicted_prob_estimate = (self.A * self.current_prob_estimate) * np.transpose(self.A) + self.Q
       
        #--------------------------Observation step-----------------------------
        innovation = measurement_vector - self.H*predicted_state_estimate
        innovation_covariance = self.H*predicted_prob_estimate*np.transpose(self.H) + self.R

        #-----------------------------Update step-------------------------------
        kalman_gain = predicted_prob_estimate * np.transpose(self.H) * np.linalg.inv(innovation_covariance)
        self.current_state_estimate = predicted_state_estimate + kalman_gain * innovation

        # We need the size of the matrix so we can make an identity matrix.
        size = self.current_prob_estimate.shape[0]
        # eye(n) = nxn identity matrix.
        self.current_prob_estimate = (np.eye(size)-kalman_gain*self.H)*predicted_prob_estimate

    @staticmethod
    def setUpMatrices(ultrasonicAngle):
        placeError = 0.01  # human error in placing robot straight in field
        motorSpinError = 0.1
        processNoise = 0.01
        # measNoise = 0.001
        dt = 0  # we don't know this yet but we will correct it before needed
        #G = radius_of_wheel / width of robot

        A = np.matrix([[1, overallTransferFunction*dt], [0, 0]])
        B = np.matrix([[0], [1]])
        # for reference z = np.matrix([[leftUltrasonicAngle],[rightUltrasonicAngle],
        #[backEncoderAngle], [frontEncoderAngle], [speedDiffFront],[speedDiffBack]])
        H = np.matrix([[1, 0], [1, 0],[0,1], [0, 1]]) #[1,0] for every angle meas and [0,1] for every speed diff meas
        x = np.matrix([[ultrasonicAngle], [0]])  # [theta, wdiff]
        P = np.matrix([[placeError, 0], [0, motorSpinError]])
        #TODO fix q and r
        Q = np.matrix([[processNoise, 0], [0, processNoise]])  # process noise
        R = np.matrix([ [0.04260563,-0.00193616,0.00063097,-0.00063855,0.00060984,-0.00044353],
[-0.00193616,0.00249706,0.00034053,-0.00034042,0.00042895,-0.000469],
[0.00063097,0.00034053,0.00093103,-0.00076006,0.00080411,-0.00081749],
 [-0.00063855, -0.00034042, -0.00076006,  0.00185051, -0.00070044,  0.00177549],
 [ 0.00060984,  0.00042895,  0.00080411, -0.00070044,  0.00077202, -0.00078121],
 [-0.00044353, -0.000469,   -0.00081749,  0.00177549, -0.00078121,  0.00187438]])

        return [A, B, H, x, P, Q, R]


if __name__ == "__main__":
    
    kalman = KalmanFilter(12)

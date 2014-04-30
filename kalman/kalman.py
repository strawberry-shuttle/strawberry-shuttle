#Kalman Filter 
#Evan Racah
#This class was written  by Greg Czerniak with some modifications
#and can be found here: http://greg.czerniak.info/guides/kalman1/


#we need numpy here...
import numpy as np
import time

# Implements a linear Kalman filter.
class KalmanFilterLinear(object):
	# I know, I know, VIJAY: you can turn this into a readme if you want, but nice to have now, while working on it
	# A: State transition matrix.
  # B: Control matrix.
  # H: Observation matrix.
  # current_state_estimate: state estimate.
  # current_prob_estimate: covariance estimate.
  # Q: Estimated error in process.
  # R: Estimated error in measurements.
  def __init__(self, kalmanParameters):
 

    self.A, self.B, self.H, self.current_state_estimate, \ 
    self.current_prob_estimate, self.Q, self.R = kalmanParameters

    self.startTime = time.time()

  def GetCurrentState(self):
    return self.current_state_estimate

  def Step(self,control_vector,measurement_vector):
    #---------------------------Prediction step-----------------------------
    predicted_state_estimate = self.A * self.current_state_estimate + self.B * control_vector
    predicted_prob_estimate = (self.A * self.current_prob_estimate) * numpy.transpose(self.A) + self.Q

    #--------------------------Observation step-----------------------------
    innovation = measurement_vector - self.H*predicted_state_estimate
    innovation_covariance = self.H*predicted_prob_estimate*numpy.transpose(self.H) + self.R

    #-----------------------------Update step-------------------------------
    kalman_gain = predicted_prob_estimate * numpy.transpose(self.H) * numpy.linalg.inv(innovation_covariance)
    self.current_state_estimate = predicted_state_estimate + kalman_gain * innovation

    # We need the size of the matrix so we can make an identity matrix.
    size = self.current_prob_estimate.shape[0]
    # eye(n) = nxn identity matrix.
    self.current_prob_estimate = (numpy.eye(size)-kalman_gain*self.H)*predicted_prob_estimate

def setUpMatrices():
  placeError = 0.001 #humanerror in placing robot straight in field
  motorSpinError = 0.00001
  processNoise = 0.001
  measNoise = 0.001
  #G = radius_of_wheeel / width of robot
	#oops these are not right yet. Oliver and I need to do more work on this
	A = np.matrix([[1, G * dt],[0, 0]])
	B = np.matrix([[0],[1]])
	H = np.matrix([[1, 0],[0,1]]) #H = np.matrix([[1, 0],[1, 0],[0,1]]) for camera
	x = np.matrix([[0],[0]])  #[theta, wdiff] 
  P = np.matrix([[placeError, 0],[0, motorSpinError]]) 
  Q = np.matrix([[processNoise,0],[0, processNoise]]) #process noise
  R = np.matrix([[measNoise,0],[0,measNoise]]) 

  return [A, B, H, x, P, Q, R]


		
if __name__ == "__main__":
	dt = 0.0001 #we need to calculate this
	kalman = KalmanFilterLinear(setUpMatrices(dt))
	
	



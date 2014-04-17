#Kalman Filter 
#Evan, Oliver 4/16/14
import cv2

class Kalman(object):
	def __init__(self,params,matrices): #params is a list of the number of elements in the F,B, and H matrix
		self.KalmanFilt = cv2.KalmanFilter(params)
		self.F, self.B, self.G,self.H,self.G,self.Z,self.P0 = matrices
		#set matrices inside kalman filter





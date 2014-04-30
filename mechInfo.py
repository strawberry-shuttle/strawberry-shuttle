#Mechanical Info

from math import pi

#TODO: Normalize units to cm
wheelDiameter = 31.75  # cm, 12.5 inches
wheelCircumference = wheelDiameter * pi
widthRobot = 25.4  # cm, 10 inches
desiredSpeed = 100  # rps, desiredSpeed in rps
distBetweenUS = 20  # cm
maxPPS = 4400  # encoder reading at max speed (pulses per second)
distForNoFurrow = 50  # cm, distances greater than this are assumed to be at the end of the furrow
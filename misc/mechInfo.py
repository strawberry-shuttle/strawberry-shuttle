#Mechanical Info

from math import pi

wheelDiameter = 31.75  # cm, 12.5 inches
wheelCircumference = wheelDiameter * pi
robotWidth = 10  # cm, 10 inches
desiredSpeed = 0.5  # rps, desiredSpeed in rps
distBetweenUS = 74.75  # cm
maxPPS = 4600  # encoder reading at max speed (pulses per second)
speedLimit = 2  # rps, max speed the robot is allowed to go
distForNoFurrow = 40  # cm, distances greater than this are assumed to be at the end of the furrow

overallTransferFunction = (wheelDiameter / 2) / robotWidth # G we need to experimentally determine (it is theta dot over omega diff desired)
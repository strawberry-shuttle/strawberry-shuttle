#Mechanical Info

from math import pi

wheelDiameter = 31.75  # cm, 12.5 inches
wheelCircumference = wheelDiameter * pi
robotWidth = 25.4  # cm, 10 inches
desiredSpeed = 0.75  # rps, desiredSpeed in rps
distBetweenUS = 77.5  # cm
maxPPS = 4600  # encoder reading at max speed (pulses per second)
distForNoFurrow = 500  # cm, distances greater than this are assumed to be at the end of the furrow
#TODO: Change distForNoFurrow back to normal after

overallTransferFunction = (wheelDiameter / 2) / robotWidth # G we need to experimentally determine (it is theta dot over omega diff desired)

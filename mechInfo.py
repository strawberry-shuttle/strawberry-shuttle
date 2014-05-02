#Mechanical Info

from math import pi

wheelDiameter = 31.75  # cm, 12.5 inches
wheelCircumference = wheelDiameter * pi
robotWidth = 25.4  # cm, 10 inches
robotDiameter = robotWidth  # TODO: This is used in EncoderProtractor. What should this be? Idk what "diameter" means in this context
desiredSpeed = 100  # rps, desiredSpeed in rps
distBetweenUS = 20  # cm
maxPPS = 4400  # encoder reading at max speed (pulses per second)
distForNoFurrow = 50  # cm, distances greater than this are assumed to be at the end of the furrow
#Oliver Chen
#tests fuzzy (i think)

from drivers.motors import Motors as m
from drivers.ultrasonic_sensors import UltrasonicSensors as us
from control.fuzzy.fuzzy import fuzzyControl as fuzz

m = m()
u = us()
f = fuzz()

while 1:
	dist = u.updateDistances()
	speed = fuzz.fuzzy([dist[2], dist[3], dist[4], dist[5]])
	m.moveForward(speed[0], speed[1])
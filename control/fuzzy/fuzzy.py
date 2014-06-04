__author__ = 'Oliver Chen'

from misc import mechInfo

class fuzzyControl:
    def __init__(self):
        self.desiredSpeed = mechInfo.desiredSpeed
        self.robotWidth = mechInfo.robotWidth
        self.turnRadius = 30

        #fuzzyAngle determines the two motor speeds [left motor, right motor] in terms of RPS
        #based on the angle of the robot relative to the furrow. It turns around a radius of
        #turnRadius*(30/angle), but that can be tweaked depending on experimental results
    def fuzzyAngle(self, angle):
        return [self.desiredSpeed*(1 - (angle/30) * self.robotWidth/(2 * self.turnRadius)),
                self.desiredSpeed*(1 + (angle/30) * self.robotWidth/(2 * self.turnRadius))]

        #Pass the function four ultrasound measurements [fl, fr, bl, br]
    def fuzzyFindDist(self, ultrasoundMeasurements):
        return [(ultrasoundMeasurements[0] + ultrasoundMeasurements[2])/2,
                (ultrasoundMeasurements[1] + ultrasoundMeasurements[3])/2]

        #fuzztDist determines the two motor speeds [left motor, right motor] in terms of RPS
        #based on the distances of the robot relative to the furrow. It only turns if you are outside
        #the center X cm of the furrow. It turns around a radius of turnRadius*(30/speedDiff), which
        #can again be tweaked depending on experimental results
        #Pass the function four ultrasound measurements [fl, fr, bl, br]
    def fuzzyDist(self, ultrasoundMeasurements):
        distances = self.fuzzyFindDist(ultrasoundMeasurements)
        speedDiff = distances[1] - distances[0]
        center = 3 #in cm
        if speedDiff > center/2:
            speedDiff = speedDiff - center/2
        elif speedDiff < -center/2:
            speedDiff = speedDiff + center/2
        else:
            speedDiff = 0
        return [self.desiredSpeed*(1 - (speedDiff/30) * self.robotWidth/(2 * self.turnRadius)),
            self.desiredSpeed*(1 + (speedDiff/30) * self.robotWidth/(2 * self.turnRadius))]

    #simply runs all of the functions
    def fuzzy(self, angle, ultrasoundMeasurements):
        fd = self.fuzzyDist(ultrasoundMeasurements)
        fa = self.fuzzyAngle(angle)
        return [fd[0] + fa[0], fd[1] + fa[1]]
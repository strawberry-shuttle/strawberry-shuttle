__author__ = 'Oliver Chen'

from misc import mechInfo

class fuzzyControl:
    """Fuzzy Control System class.
    
    A control system to determine motor speeds based on current heading angle through fuzzy logic.
    """
    def __init__(self):
        """
        
        Input: N/A
        Output: N/A
        
        Constructor for fuzzy control class. Initializes constants based on values in mechInfo.
        """
        self.desiredSpeed = mechInfo.desiredSpeed
        self.robotWidth = mechInfo.robotWidth
        self.turnRadius = 30

    def fuzzyAngle(self, angle):
        """
        
        Input: float(Heading Angle)
        Output: list([Left Motor Speeds, Right Motor Speeds])
        
        Determines the two motor speeds [left motor, right motor] in terms of RPS
        based on the angle of the robot relative to the furrow. It turns around a radius of
        turnRadius*(30/angle), but that can be tweaked depending on experimental results.
        """
        return [self.desiredSpeed*(1 - (angle/20) * self.robotWidth/(2 * self.turnRadius)),
                self.desiredSpeed*(1 + (angle/20) * self.robotWidth/(2 * self.turnRadius))]

        #Pass the function four ultrasound measurements [fl, fr, bl, br]
    @staticmethod
    def fuzzyFindDist(ultrasoundMeasurements):
        """
        
        Input: list([Left Front Ultrasonic Measurement in cm,Right Front Ultrasonic Measurement in cm,Left Back Ultrasonic Measurement in cm,Right Back Ultrasonic Measurement in cm])
        Output: 
        
        Determine distance from walls on right and left side based on input data from ultrasonic sensors.
        """
        return [(ultrasoundMeasurements[0] + ultrasoundMeasurements[2])/2,
                (ultrasoundMeasurements[1] + ultrasoundMeasurements[3])/2]


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
        return [self.desiredSpeed*(1 - (speedDiff/20) * self.robotWidth/(2 * self.turnRadius)),
            self.desiredSpeed*(1 + (speedDiff/20) * self.robotWidth/(2 * self.turnRadius))]

    #simply runs all of the functions
    def fuzzy(self, angle, ultrasoundMeasurements):
        fd = self.fuzzyDist(ultrasoundMeasurements)
        fa = self.fuzzyAngle(angle)
        return [(fd[0] + fa[0])/2, (fd[1] + fa[1])/2]
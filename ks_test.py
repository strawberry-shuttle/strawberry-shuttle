from drivers.ks import Ultrasonic_KS as US
from time import sleep

ultrasonic = US() #Uses default address, 0x74


while 1:
    if ultrasonic.ping() != -1:
        sleep(.1)  
        print "Front Distance (cm): %.1f" % (ultrasonic.read()/10.0)

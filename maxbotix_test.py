from drivers.maxbotix import Ultrasonic_MB as US

ultrasonic_front = US() #Uses default address

ultrasonic_back = US(0x71) #Uses custom address, this is handled in the class, but it's up to the user to make sure that the same address isn't used multiple times
ultrasonic_back.setAddr() #Use this very sparingly, as writing to the EEPROM decreases the lifespan of the sensor, this only needs to be done a single time, not every startup

if ultrasonic_front.ping() != -1:
    sleep(.1) #We choose to handle sleeping in the calling function because this allows for more control without affecting the class 
    print "Front Distance (cm): %d" % ultrasonic_front.read()

if ultrasonic_back.ping() != -1:
    sleep(.1) #We choose to handle sleeping in the calling function because this allows for more control without affecting the class 
    print "Back Distance (cm): %d" % ultrasonic_back.read()
    


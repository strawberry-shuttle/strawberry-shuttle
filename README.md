#Strawberry Shuttle Code

Navigation

i.) Main Directory

main.py: Main system control file

encoderAngle_test.py: 

ks_test.py: Test Kingsin Ultrasonic Driver

maxbotix_test.py: Test Maxbotix Ultrasonic Driver

motor_test.py: Service that handles starting and stopping forward movement of robot based on GPIO input or given distance.

sensor_covariance_test.py:

time_resp_motor_test.py 

ii.) camera

->BirdsEyeView: Contains Bird's Eye View related files

iii.) control

->fuzzy: 

->kalman:

->PID:

->state: Contains system state machine code, handles state transitions

iv.) drivers

buttons.py: External button functionality

ultrasonic_sensors.py: Ultrasonic Sensor API, talks to ultrasonic drivers

ks.py: Kingsin Ultrasonic Sensor Driver, don't use directly; handle through ultrasonic_sensors.py

maxbotix.py: Maxbotix Ultrasonic Sensor Driver, don't use directly; handle through ultrasonic_sensors.py

motors.py: Motor API, talks to roboclaw driver

roboclaw_lib.py: Roboclaw Motor Controller driver, don't directly access, use motors.py instead

roboclaw_test.py: Example function for roboclaw_lib

v.) misc

log.py: Logging class, use to print out stack information

mechInfo.py: Contains constants relating to physical specifications



import time

from drivers.roboclaw_lib import Roboclaw
import Adafruit_BBIO.UART as UART


UART.setup("UART1")


print "Roboclaw Example 1\r\n"

#Rasberry Pi/Linux Serial instance example
#port = serial.Serial("/dev/ttyACM0", baudrate=115200, timeout=0.1)

#Windows Serial instance example
#port = serial.Serial("COM253", baudrate=38400, timeout=1)
robo = Roboclaw(0x80, "/dev/ttyO1")

#Get version string
rcv = robo.read_version()
print repr(rcv)

cnt = 0
while True:
    cnt += 1
    print "Count = ", cnt

    print "Error State:", repr(robo.read_error_state())

    print "Temperature:", robo.read_temperature()/10.0

    print "Main Battery:", robo.read_main_battery()/10.0

    print "Logic Battery:", robo.read_logic_battery()/10.0

    m1cur, m2cur = robo.read_currents()
    print "Current M1: ", m1cur/10.0, " M2: ", m2cur/10.0

    min, max = robo.read_logic_battery_settings()
    print "Logic Battery Min:", min/10.0, " Max:", max/10.0

    min, max = robo.read_main_battery_settings()
    print "Main Battery Min:", min/10.0, " Max:", max/10.0

    p, i, d, qpps = robo.read_m1_pidq()
    print "M1 P=%.2f" % (p/65536.0)
    print "M1 I=%.2f" % (i/65536.0)
    print "M1 D=%.2f" % (d/65536.0)
    print "M1 QPPS=", qpps

    p, i, d, qpps = robo.read_m2_pidq()
    print "M2 P=%.2f" % (p/65536.0)
    print "M2 I=%.2f" % (i/65536.0)
    print "M2 D=%.2f" % (d/65536.0)
    print "M2 QPPS=", qpps

    robo.m1_forward(127)
    for i in range(5):
        m1cur, m2cur = robo.read_currents()
        print "Current M1: ", m1cur/100.0, "A M2: ", m2cur/100.0, "A"
        time.sleep(1)
    robo.m1_forward(0)
    time.sleep(5)

    #robo.set_m2_duty_accel(1500, -1500)
    #time.sleep(2)
    #robo.set_m1_duty_accel(1500, -1500)
    #robo.set_m2_duty_accel(1500, 1500)
    #time.sleep(2)

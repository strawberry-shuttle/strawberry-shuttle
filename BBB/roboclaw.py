import struct
import serial


class Roboclaw:

    def __init__(self, address, port):
        self.address = address
        self.checksum = 0
        self.port = serial.Serial(port, baudrate=38400, timeout=1)

    def send_command(self, address, command):
        self.checksum = address
        self.port.write(chr(address))
        self.checksum += command
        self.port.write(chr(command))
        return

    def read_byte(self):
        val = struct.unpack('>B', self.port.read(1))
        self.checksum += val[0]
        return val[0]
    
    def read_s_byte(self):
        val = struct.unpack('>b', self.port.read(1))
        self.checksum += val[0]
        return val[0]
    
    def read_word(self):
        val = struct.unpack('>H', self.port.read(2))
        self.checksum += (val[0] & 0xFF)
        self.checksum += (val[0] >> 8) & 0xFF
        return val[0]
    
    def read_s_word(self):
        val = struct.unpack('>h', self.port.read(2))
        self.checksum += val[0]
        self.checksum += (val[0] >> 8) & 0xFF
        return val[0]
    
    def read_long(self):
        val = struct.unpack('>L', self.port.read(4))
        self.checksum += val[0]
        self.checksum += (val[0] >> 8) & 0xFF
        self.checksum += (val[0] >> 16) & 0xFF
        self.checksum += (val[0] >> 24) & 0xFF
        return val[0]

    def read_s_long(self):
        val = struct.unpack('>l', self.port.read(4))
        self.checksum += val[0]
        self.checksum += (val[0] >> 8) & 0xFF
        self.checksum += (val[0] >> 16) & 0xFF
        self.checksum += (val[0] >> 24) & 0xFF
        return val[0]

    def write_byte(self, val):
        self.checksum += val
        return self.port.write(struct.pack('>B', val))
    
    def write_s_byte(self, val):
        self.checksum += val
        return self.port.write(struct.pack('>b', val))
    
    def write_word(self, val):
        self.checksum += val
        self.checksum += (val >> 8) & 0xFF
        return self.port.write(struct.pack('>H', val))
    
    def write_s_word(self, val):
        self.checksum += val
        self.checksum += (val >> 8) & 0xFF
        return self.port.write(struct.pack('>h', val))
    
    def write_long(self, val):
        self.checksum += val
        self.checksum += (val >> 8) & 0xFF
        self.checksum += (val >> 16) & 0xFF
        self.checksum += (val >> 24) & 0xFF
        return self.port.write(struct.pack('>L', val))
    
    def write_s_long(self, val):
        self.checksum += val
        self.checksum += (val >> 8) & 0xFF
        self.checksum += (val >> 16) & 0xFF
        self.checksum += (val >> 24) & 0xFF
        return self.port.write(struct.pack('>l', val))

    def m1_forward(self, val):
        self.send_command(128, 0)
        self.write_byte(val)
        self.write_byte(self.checksum & 0x7F)
        return

    def m1_backward(self, val):
        self.send_command(128, 1)
        self.write_byte(val)
        self.write_byte(self.checksum & 0x7F)
        return

    def set_min_main_battery(self, val):
        self.send_command(128, 2)
        self.write_byte(val)
        self.write_byte(self.checksum & 0x7F)
        return

    def set_max_main_battery(self, val):
        self.send_command(128, 3)
        self.write_byte(val)
        self.write_byte(self.checksum & 0x7F)
        return

    def m2_forward(self, val):
        self.send_command(128, 4)
        self.write_byte(val)
        self.write_byte(self.checksum & 0x7F)
        return

    def m2_backward(self, val):
        self.send_command(128, 5)
        self.write_byte(val)
        self.write_byte(self.checksum & 0x7F)
        return

    def drive_m1(self, val):
        self.send_command(128, 6)
        self.write_byte(val)
        self.write_byte(self.checksum & 0x7F)
        return

    def drive_m2(self, val):
        self.send_command(128, 7)
        self.write_byte(val)
        self.write_byte(self.checksum & 0x7F)
        return

    def forward_mixed(self, val):
        self.send_command(128, 8)
        self.write_byte(val)
        self.write_byte(self.checksum & 0x7F)
        return

    def backward_mixed(self, val):
        self.send_command(128, 9)
        self.write_byte(val)
        self.write_byte(self.checksum & 0x7F)
        return

    def right_mixed(self, val):
        self.send_command(128, 10)
        self.write_byte(val)
        self.write_byte(self.checksum & 0x7F)
        return

    def left_mixed(self, val):
        self.send_command(128, 11)
        self.write_byte(val)
        self.write_byte(self.checksum & 0x7F)
        return

    def drive_mixed(self, val):
        self.send_command(128, 12)
        self.write_byte(val)
        self.write_byte(self.checksum & 0x7F)
        return

    def turn_mixed(self, val):
        self.send_command(128,  13)
        self.write_byte(val)
        self.write_byte(self.checksum & 0x7F)
        return

    def read_m1_encoder(self):
        self.send_command(128,  16)
        enc = self.read_s_long()
        status = self.read_byte()
        crc = self.checksum & 0x7F
        if crc == self.read_byte():
            return enc, status
        return -1, -1

    def read_m2_encoder(self):
        self.send_command(128, 17)
        enc = self.read_s_long()
        status = self.read_byte()
        crc = self.checksum & 0x7F
        if crc == self.read_byte():
            return enc, status
        return -1, -1

    def read_m1_speed(self):
        self.send_command(128,  18)
        enc = self.read_s_long()
        status = self.read_byte()
        crc = self.checksum & 0x7F
        if crc == self.read_byte():
            return enc, status
        return -1, -1

    def read_m2_speed(self):
        self.send_command(128, 19)
        enc = self.read_s_long()
        status = self.read_byte()
        crc = self.checksum & 0x7F
        if crc == self.read_byte():
            return enc, status
        return -1, -1

    def reset_encoder_cnts(self):
        self.send_command(128,  20)
        self.write_byte(self.checksum & 0x7F)
        return

    def read_version(self):
        self.send_command(128, 21)
        return self.port.read(32)

    def read_main_battery(self):
        self.send_command(128, 24)
        val = self.read_word()
        crc = self.checksum & 0x7F
        if crc == self.read_byte():
            return val
        return -1

    def read_logic_battery(self):
        self.send_command(128, 25)
        val = self.read_word()
        crc = self.checksum & 0x7F
        if crc == self.read_byte():
            return val
        return -1

    def set_m1_pidq(self, p, i, d, qpps):
        self.send_command(128,  28)
        self.write_long(d)
        self.write_long(p)
        self.write_long(i)
        self.write_long(qpps)
        self.write_byte(self.checksum & 0x7F)
        return

    def set_m2_pidq(self, p, i, d, qpps):
        self.send_command(128, 29)
        self.write_long(d)
        self.write_long(p)
        self.write_long(i)
        self.write_long(qpps)
        self.write_byte(self.checksum & 0x7F)
        return

    def read_m1_inst_speed(self):
        self.send_command(128, 30)
        enc = self.read_s_long()
        status = self.read_byte()
        crc = self.checksum & 0x7F
        if crc == self.read_byte():
            return enc, status
        return -1, -1

    def read_m2_inst_speed(self):
        self.send_command(128, 31)
        enc = self.read_s_long()
        status = self.read_byte()
        crc = self.checksum & 0x7F
        if crc == self.read_byte():
            return enc, status
        return -1, -1

    def set_m1_duty(self, val):
        self.send_command(128, 32)
        self.write_s_word(val)
        self.write_byte(self.checksum & 0x7F)
        return

    def set_m2_duty(self, val):
        self.send_command(128, 33)
        self.write_s_word(val)
        self.write_byte(self.checksum & 0x7F)
        return

    def set_mixed_duty(self, m1, m2):
        self.send_command(128, 34)
        self.write_s_word(m1)
        self.write_s_word(m2)
        self.write_byte(self.checksum & 0x7F)
        return

    def set_m1_speed(self, val):
        self.send_command(128, 35)
        self.write_s_long(val)
        self.write_byte(self.checksum & 0x7F)
        return

    def set_m2_speed(self, val):
        self.send_command(128,  36)
        self.write_s_long(val)
        self.write_byte(self.checksum & 0x7F)
        return

    def set_mixed_speed(self, m1, m2):
        self.send_command(128,  37)
        self.write_s_long(m1)
        self.write_s_long(m2)
        self.write_byte(self.checksum & 0x7F)
        return

    def set_m1_speed_accel(self, accel, speed):
        self.send_command(128,  38)
        self.write_long(accel)
        self.write_s_long(speed)
        self.write_byte(self.checksum & 0x7F)
        return

    def set_m2_speed_accel(self, accel, speed):
        self.send_command(128, 39)
        self.write_long(accel)
        self.write_s_long(speed)
        self.write_byte(self.checksum & 0x7F)
        return

    def set_mixed_speed_accel(self, accel, speed1, speed2):
        self.send_command(128,  40)
        self.write_long(accel)
        self.write_s_long(speed1)
        self.write_s_long(speed2)
        self.write_byte(self.checksum & 0x7F)
        return

    def set_m1_speed_distance(self, speed, distance, buffer):
        self.send_command(128, 41)
        self.write_s_long(speed)
        self.write_long(distance)
        self.write_byte(buffer)
        self.write_byte(self.checksum & 0x7F)
        return

    def set_m2_speed_distance(self, speed, distance, buffer):
        self.send_command(128, 42)
        self.write_s_long(speed)
        self.write_long(distance)
        self.write_byte(buffer)
        self.write_byte(self.checksum & 0x7F)
        return

    def set_mixed_speed_distance(self, speed1, distance1, speed2, distance2, buffer):
        self.send_command(128, 43)
        self.write_s_long(speed1)
        self.write_long(distance1)
        self.write_s_long(speed2)
        self.write_long(distance2)
        self.write_byte(buffer)
        self.write_byte(self.checksum & 0x7F)
        return

    def set_m1_speed_accel_distance(self, accel, speed, distance, buffer):
        self.send_command(128, 44)
        self.write_long(accel)
        self.write_s_long(speed)
        self.write_long(distance)
        self.write_byte(buffer)
        self.write_byte(self.checksum & 0x7F)
        return

    def set_m2_speed_accel_distance(self, accel, speed, distance, buffer):
        self.send_command(128, 45)
        self.write_long(accel)
        self.write_s_long(speed)
        self.write_long(distance)
        self.write_byte(buffer)
        self.write_byte(self.checksum & 0x7F)
        return

    def set_mixed_speed_accel_distance(self, accel, speed1, distance1, speed2, distance2, buffer):
        self.send_command(128, 46)
        self.write_long(accel)
        self.write_s_long(speed1)
        self.write_long(distance1)
        self.write_s_long(speed2)
        self.write_long(distance2)
        self.write_byte(buffer)
        self.write_byte(self.checksum & 0x7F)
        return

    def read_buffer_cnts(self):
        self.send_command(128, 47)
        buffer1 = self.read_byte()
        buffer2 = self.read_byte()
        crc = self.checksum & 0x7F
        if crc == self.read_byte():
            return buffer1, buffer2
        return -1, -1

    def read_currents(self):
        self.send_command(128, 49)
        motor1 = self.read_word()
        motor2 = self.read_word()
        crc = self.checksum & 0x7F
        if crc == self.read_byte():
            return motor1, motor2
        return -1, -1

    def set_mixed_speed_i_accel(self, accel1, speed1, accel2, speed2):
        self.send_command(128, 50)
        self.write_long(accel1)
        self.write_s_long(speed1)
        self.write_long(accel2)
        self.write_s_long(speed2)
        self.write_byte(self.checksum & 0x7F)
        return

    def set_mixed_speed_i_accel_distance(self, accel1, speed1, distance1, accel2, speed2, distance2, buffer):
        self.send_command(128, 51)
        self.write_long(accel1)
        self.write_s_long(speed1)
        self.write_long(distance1)
        self.write_long(accel2)
        self.write_s_long(speed2)
        self.write_long(distance2)
        self.write_byte(buffer)
        self.write_byte(self.checksum & 0x7F)
        return

    def set_m1_duty_accel(self, accel, duty):
        self.send_command(128, 52)
        self.write_s_word(duty)
        self.write_word(accel)
        self.write_byte(self.checksum & 0x7F)
        return

    def set_m2_duty_accel(self, accel, duty):
        self.send_command(128, 53)
        self.write_s_word(duty)
        self.write_word(accel)
        self.write_byte(self.checksum & 0x7F)
        return

    def set_mixed_duty_accel(self, accel1, duty1, accel2, duty2):
        self.send_command(128, 54)
        self.write_s_word(duty1)
        self.write_word(accel1)
        self.write_s_word(duty2)
        self.write_word(accel2)
        self.write_byte(self.checksum & 0x7F)
        return

    def read_m1_pidq(self):
        self.send_command(128, 55)
        p = self.read_long()
        i = self.read_long()
        d = self.read_long()
        qpps = self.read_long()
        crc = self.checksum & 0x7F
        if crc == self.read_byte():
            return p, i, d, qpps
        return -1, -1, -1, -1

    def read_m2_pidq(self):
        self.send_command(128, 56)
        p = self.read_long()
        i = self.read_long()
        d = self.read_long()
        qpps = self.read_long()
        crc = self.checksum & 0x7F
        if crc == self.read_byte():
            return p, i, d, qpps
        return -1, -1, -1, -1

    def read_main_battery_settings(self):
        self.send_command(128, 59)
        min = self.read_word()
        max = self.read_word()
        crc = self.checksum & 0x7F
        if crc == self.read_byte():
            return min, max
        return -1, -1

    def read_logic_battery_settings(self):
        self.send_command(128, 60)
        min = self.read_word()
        max = self.read_word()
        crc = self.checksum & 0x7F
        if crc == self.read_byte():
            return min, max
        return -1, -1

    def set_m1_position_constants(self, kp, ki, kd, kimax, deadzone, min, max):
        self.send_command(128, 61)
        self.write_long(kd)
        self.write_long(kp)
        self.write_long(ki)
        self.write_long(kimax)
        self.write_long(min)
        self.write_long(max)
        return

    def set_m2_position_constants(self, kp, ki, kd, kimax, deadzone, min, max):
        self.send_command(128, 62)
        self.write_long(kd)
        self.write_long(kp)
        self.write_long(ki)
        self.write_long(kimax)
        self.write_long(min)
        self.write_long(max)
        return

    def read_m1_position_constants(self):
        self.send_command(128, 63)
        p = self.read_long()
        i = self.read_long()
        d = self.read_long()
        imax = self.read_long()
        deadzone = self.read_long()
        min = self.read_long()
        max = self.read_long()
        crc = self.checksum & 0x7F
        if crc == self.read_byte():
            return p, i, d, imax, deadzone, min, max
        return -1, -1, -1, -1, -1, -1, -1

    def read_m2_position_constants(self):
        self.send_command(128, 64)
        p = self.read_long()
        i = self.read_long()
        d = self.read_long()
        imax = self.read_long()
        deadzone = self.read_long()
        min = self.read_long()
        max = self.read_long()
        crc = self.checksum & 0x7F
        if crc == self.read_byte():
            return p, i, d, imax, deadzone, min, max
        return -1, -1, -1, -1, -1, -1, -1

    def set_m1_speed_accel_deccel_position(self, accel, speed, deccel, position, buffer):
        self.send_command(128, 65)
        self.write_long(accel)
        self.write_long(speed)
        self.write_long(deccel)
        self.write_long(position)
        self.write_byte(buffer)
        self.write_byte(self.checksum & 0x7F)
        return

    def set_m2_speed_accel_deccel_position(self, accel, speed, deccel, position, buffer):
        self.send_command(128, 66)
        self.write_long(accel)
        self.write_long(speed)
        self.write_long(deccel)
        self.write_long(position)
        self.write_byte(buffer)
        self.write_byte(self.checksum & 0x7F)
        return

    def set_mixed_speed_accel_deccel_position(self, accel1, speed1, deccel1, position1, accel2, speed2, deccel2, position2, buffer):
        self.send_command(128, 67)
        self.write_long(accel1)
        self.write_long(speed1)
        self.write_long(deccel1)
        self.write_long(position1)
        self.write_long(accel2)
        self.write_long(speed2)
        self.write_long(deccel2)
        self.write_long(position2)
        self.write_byte(buffer)
        self.write_byte(self.checksum & 0x7F)
        return

    def read_temperature(self):
        self.send_command(128, 82)
        val = self.read_word()
        crc = self.checksum & 0x7F
        if crc == self.read_byte():
            return val
        return -1

    def read_error_state(self):
        self.send_command(128, 90)
        val = self.read_byte()
        crc = self.checksum & 0x7F
        if crc == self.read_byte():
            return val
        return -1

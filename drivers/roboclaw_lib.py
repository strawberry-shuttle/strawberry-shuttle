import struct
import serial


class Roboclaw:

    def __init__(self, address, port):
        self.address = address
        self.checksum = 0
        self.port = serial.Serial(port, baudrate=38400, timeout=1)

    def __send_command(self, command):
        self.checksum = self.address + command
        self.port.write(bytearray([self.address, command]))
        return

    def __read_byte(self):
        val = struct.unpack('>B', self.port.read(1))
        self.checksum += val[0]
        return val[0]
    
    def __read_s_byte(self):
        val = struct.unpack('>b', self.port.read(1))
        self.checksum += val[0]
        return val[0]
    
    def __read_word(self):
        val = struct.unpack('>H', self.port.read(2))
        self.checksum += (val[0] & 0xFF)
        self.checksum += (val[0] >> 8) & 0xFF
        return val[0]
    
    def __read_s_word(self):
        val = struct.unpack('>h', self.port.read(2))
        self.checksum += val[0]
        self.checksum += (val[0] >> 8) & 0xFF
        return val[0]
    
    def __read_long(self):
        val = struct.unpack('>L', self.port.read(4))
        self.checksum += val[0]
        self.checksum += (val[0] >> 8) & 0xFF
        self.checksum += (val[0] >> 16) & 0xFF
        self.checksum += (val[0] >> 24) & 0xFF
        return val[0]

    def __read_s_long(self):
        val = struct.unpack('>l', self.port.read(4))
        self.checksum += val[0]
        self.checksum += (val[0] >> 8) & 0xFF
        self.checksum += (val[0] >> 16) & 0xFF
        self.checksum += (val[0] >> 24) & 0xFF
        return val[0]

    def __write_byte(self, val):
        self.checksum += val
        return self.port.write(struct.pack('>B', val))
    
    def __write_s_byte(self, val):
        self.checksum += val
        return self.port.write(struct.pack('>b', val))
    
    def __write_word(self, val):
        self.checksum += val
        self.checksum += (val >> 8) & 0xFF
        return self.port.write(struct.pack('>H', val))
    
    def __write_s_word(self, val):
        self.checksum += val
        self.checksum += (val >> 8) & 0xFF
        return self.port.write(struct.pack('>h', val))
    
    def __write_long(self, val):
        self.checksum += val
        self.checksum += (val >> 8) & 0xFF
        self.checksum += (val >> 16) & 0xFF
        self.checksum += (val >> 24) & 0xFF
        return self.port.write(struct.pack('>L', val))
    
    def __write_s_long(self, val):
        self.checksum += val
        self.checksum += (val >> 8) & 0xFF
        self.checksum += (val >> 16) & 0xFF
        self.checksum += (val >> 24) & 0xFF
        return self.port.write(struct.pack('>l', val))

    def __validate_checksum(self):
        crc = self.checksum & 0x7F
        return crc == self.__read_byte()

    def __write_checksum(self):
        return self.__write_byte(self.checksum & 0x7F)

    def m1_forward(self, val):
        self.__send_command(0)
        self.__write_byte(val)
        self.__write_checksum()
        return

    def m1_backward(self, val):
        self.__send_command(1)
        self.__write_byte(val)
        self.__write_checksum()
        return

    def set_min_main_battery(self, val):
        self.__send_command(2)
        self.__write_byte(val)
        self.__write_checksum()
        return

    def set_max_main_battery(self, val):
        self.__send_command(3)
        self.__write_byte(val)
        self.__write_checksum()
        return

    def m2_forward(self, val):
        self.__send_command(4)
        self.__write_byte(val)
        self.__write_checksum()
        return

    def m2_backward(self, val):
        self.__send_command(5)
        self.__write_byte(val)
        self.__write_checksum()
        return

    def drive_m1(self, val):
        self.__send_command(6)
        self.__write_byte(val)
        self.__write_checksum()
        return

    def drive_m2(self, val):
        self.__send_command(7)
        self.__write_byte(val)
        self.__write_checksum()
        return

    def forward_mixed(self, val):
        self.__send_command(8)
        self.__write_byte(val)
        self.__write_checksum()
        return

    def backward_mixed(self, val):
        self.__send_command(9)
        self.__write_byte(val)
        self.__write_checksum()
        return

    def right_mixed(self, val):
        self.__send_command(10)
        self.__write_byte(val)
        self.__write_checksum()
        return

    def left_mixed(self, val):
        self.__send_command(11)
        self.__write_byte(val)
        self.__write_checksum()
        return

    def drive_mixed(self, val):
        self.__send_command(12)
        self.__write_byte(val)
        self.__write_checksum()
        return

    def turn_mixed(self, val):
        self.__send_command(13)
        self.__write_byte(val)
        self.__write_checksum()
        return

    def read_m1_encoder(self):
        self.__send_command(16)
        enc = self.__read_s_long()
        status = self.__read_byte()
        if self.__validate_checksum():
            return enc, status
        return -1, -1

    def read_m2_encoder(self):
        self.__send_command(17)
        enc = self.__read_s_long()
        status = self.__read_byte()
        if self.__validate_checksum():
            return enc, status
        return -1, -1

    def read_m1_speed(self):
        self.__send_command(18)
        enc = self.__read_s_long()
        status = self.__read_byte()
        if self.__validate_checksum():
            return enc, status
        return -1, -1

    def read_m2_speed(self):
        self.__send_command(19)
        enc = self.__read_s_long()
        status = self.__read_byte()
        if self.__validate_checksum():
            return enc, status
        return -1, -1

    def reset_encoder_cnts(self):
        self.__send_command(20)
        self.__write_checksum()
        return

    def read_version(self):
        self.__send_command(21)
        return self.port.read(32)

    def read_main_battery(self):
        self.__send_command(24)
        val = self.__read_word()
        if self.__validate_checksum():
            return val
        return -1

    def read_logic_battery(self):
        self.__send_command(25)
        val = self.__read_word()
        if self.__validate_checksum():
            return val
        return -1

    def set_min_logic_voltage_level(self, val):
        self.__send_command(26)
        self.__write_long(val)
        self.__write_checksum()
        return

    def set_max_logic_voltage_level(self, val):
        self.__send_command(27)
        self.__write_long(val)
        self.__write_checksum()
        return

    def set_m1_pidq(self, p, i, d, qpps):
        self.__send_command(28)
        self.__write_long(d)
        self.__write_long(p)
        self.__write_long(i)
        self.__write_long(qpps)
        self.__write_checksum()
        return

    def set_m2_pidq(self, p, i, d, qpps):
        self.__send_command(29)
        self.__write_long(d)
        self.__write_long(p)
        self.__write_long(i)
        self.__write_long(qpps)
        self.__write_checksum()
        return

    def read_m1_inst_speed(self):
        self.__send_command(30)
        enc = self.__read_s_long()
        status = self.__read_byte()
        if self.__validate_checksum():
            return enc, status
        return -1, -1

    def read_m2_inst_speed(self):
        self.__send_command(31)
        enc = self.__read_s_long()
        status = self.__read_byte()
        if self.__validate_checksum():
            return enc, status
        return -1, -1

    def set_m1_duty(self, val):
        self.__send_command(32)
        self.__write_s_word(val)
        self.__write_checksum()
        return

    def set_m2_duty(self, val):
        self.__send_command(33)
        self.__write_s_word(val)
        self.__write_checksum()
        return

    def set_mixed_duty(self, m1, m2):
        self.__send_command(34)
        self.__write_s_word(m1)
        self.__write_s_word(m2)
        self.__write_checksum()
        return

    def set_m1_speed(self, val):
        self.__send_command(35)
        self.__write_s_long(val)
        self.__write_checksum()
        return

    def set_m2_speed(self, val):
        self.__send_command(36)
        self.__write_s_long(val)
        self.__write_checksum()
        return

    def set_mixed_speed(self, m1, m2):
        self.__send_command(37)
        self.__write_s_long(m1)
        self.__write_s_long(m2)
        self.__write_checksum()
        return

    def set_m1_speed_accel(self, accel, speed):
        self.__send_command(38)
        self.__write_long(accel)
        self.__write_s_long(speed)
        self.__write_checksum()
        return

    def set_m2_speed_accel(self, accel, speed):
        self.__send_command(39)
        self.__write_long(accel)
        self.__write_s_long(speed)
        self.__write_checksum()
        return

    def set_mixed_speed_accel(self, accel, speed1, speed2):
        self.__send_command(40)
        self.__write_long(accel)
        self.__write_s_long(speed1)
        self.__write_s_long(speed2)
        self.__write_checksum()
        return

    def set_m1_speed_distance(self, speed, distance, buffer):
        self.__send_command(41)
        self.__write_s_long(speed)
        self.__write_long(distance)
        self.__write_byte(buffer)
        self.__write_checksum()
        return

    def set_m2_speed_distance(self, speed, distance, buffer):
        self.__send_command(42)
        self.__write_s_long(speed)
        self.__write_long(distance)
        self.__write_byte(buffer)
        self.__write_checksum()
        return

    def set_mixed_speed_distance(self, speed1, distance1, speed2, distance2, buffer):
        self.__send_command(43)
        self.__write_s_long(speed1)
        self.__write_long(distance1)
        self.__write_s_long(speed2)
        self.__write_long(distance2)
        self.__write_byte(buffer)
        self.__write_checksum()
        return

    def set_m1_speed_accel_distance(self, accel, speed, distance, buffer):
        self.__send_command(44)
        self.__write_long(accel)
        self.__write_s_long(speed)
        self.__write_long(distance)
        self.__write_byte(buffer)
        self.__write_checksum()
        return

    def set_m2_speed_accel_distance(self, accel, speed, distance, buffer):
        self.__send_command(45)
        self.__write_long(accel)
        self.__write_s_long(speed)
        self.__write_long(distance)
        self.__write_byte(buffer)
        self.__write_checksum()
        return

    def set_mixed_speed_accel_distance(self, accel, speed1, distance1, speed2, distance2, buffer):
        self.__send_command(46)
        self.__write_long(accel)
        self.__write_s_long(speed1)
        self.__write_long(distance1)
        self.__write_s_long(speed2)
        self.__write_long(distance2)
        self.__write_byte(buffer)
        self.__write_checksum()
        return

    def read_buffer_cnts(self):
        self.__send_command(47)
        buffer1 = self.__read_byte()
        buffer2 = self.__read_byte()
        if self.__validate_checksum():
            return buffer1, buffer2
        return -1, -1

    def read_currents(self):
        self.__send_command(49)
        motor1 = self.__read_word()
        motor2 = self.__read_word()
        if self.__validate_checksum():
            return motor1, motor2
        return -1, -1

    def set_mixed_speed_i_accel(self, accel1, speed1, accel2, speed2):
        self.__send_command(50)
        self.__write_long(accel1)
        self.__write_s_long(speed1)
        self.__write_long(accel2)
        self.__write_s_long(speed2)
        self.__write_checksum()
        return

    def set_mixed_speed_i_accel_distance(self, accel1, speed1, distance1, accel2, speed2, distance2, buffer):
        self.__send_command(51)
        self.__write_long(accel1)
        self.__write_s_long(speed1)
        self.__write_long(distance1)
        self.__write_long(accel2)
        self.__write_s_long(speed2)
        self.__write_long(distance2)
        self.__write_byte(buffer)
        self.__write_checksum()
        return

    def set_m1_duty_accel(self, accel, duty):
        self.__send_command(52)
        self.__write_s_word(duty)
        self.__write_word(accel)
        self.__write_checksum()
        return

    def set_m2_duty_accel(self, accel, duty):
        self.__send_command(53)
        self.__write_s_word(duty)
        self.__write_word(accel)
        self.__write_checksum()
        return

    def set_mixed_duty_accel(self, accel1, duty1, accel2, duty2):
        self.__send_command(54)
        self.__write_s_word(duty1)
        self.__write_word(accel1)
        self.__write_s_word(duty2)
        self.__write_word(accel2)
        self.__write_checksum()
        return

    def read_m1_pidq(self):
        self.__send_command(55)
        p = self.__read_long()
        i = self.__read_long()
        d = self.__read_long()
        qpps = self.__read_long()
        if self.__validate_checksum():
            return p, i, d, qpps
        return -1, -1, -1, -1

    def read_m2_pidq(self):
        self.__send_command(56)
        p = self.__read_long()
        i = self.__read_long()
        d = self.__read_long()
        qpps = self.__read_long()
        if self.__validate_checksum():
            return p, i, d, qpps
        return -1, -1, -1, -1

    def set_main_battery_voltages(self, min, max):
        self.__send_command(57)
        self.__write_long(min)
        self.__write_long(max)
        self.__write_checksum()
        return

    def set_logic_battery_voltages(self, min, max):
        self.__send_command(58)
        self.__write_long(min)
        self.__write_long(max)
        self.__write_checksum()
        return

    def read_main_battery_settings(self):
        self.__send_command(59)
        min = self.__read_word()
        max = self.__read_word()
        if self.__validate_checksum():
            return min, max
        return -1, -1

    def read_logic_battery_settings(self):
        self.__send_command(60)
        min = self.__read_word()
        max = self.__read_word()
        if self.__validate_checksum():
            return min, max
        return -1, -1

    def set_m1_position_constants(self, kp, ki, kd, kimax, min, max):
        self.__send_command(61)
        self.__write_long(kd)
        self.__write_long(kp)
        self.__write_long(ki)
        self.__write_long(kimax)
        self.__write_long(min)
        self.__write_long(max)
        self.__write_checksum()
        return

    def set_m2_position_constants(self, kp, ki, kd, kimax, min, max):
        self.__send_command(62)
        self.__write_long(kd)
        self.__write_long(kp)
        self.__write_long(ki)
        self.__write_long(kimax)
        self.__write_long(min)
        self.__write_long(max)
        self.__write_checksum()
        return

    def read_m1_position_constants(self):
        self.__send_command(63)
        p = self.__read_long()
        i = self.__read_long()
        d = self.__read_long()
        imax = self.__read_long()
        deadzone = self.__read_long()
        min = self.__read_long()
        max = self.__read_long()
        if self.__validate_checksum():
            return p, i, d, imax, deadzone, min, max
        return -1, -1, -1, -1, -1, -1, -1

    def read_m2_position_constants(self):
        self.__send_command(64)
        p = self.__read_long()
        i = self.__read_long()
        d = self.__read_long()
        imax = self.__read_long()
        deadzone = self.__read_long()
        min = self.__read_long()
        max = self.__read_long()
        if self.__validate_checksum():
            return p, i, d, imax, deadzone, min, max
        return -1, -1, -1, -1, -1, -1, -1

    def set_m1_speed_accel_deccel_position(self, accel, speed, deccel, position, buffer):
        self.__send_command(65)
        self.__write_long(accel)
        self.__write_long(speed)
        self.__write_long(deccel)
        self.__write_long(position)
        self.__write_byte(buffer)
        self.__write_checksum()
        return

    def set_m2_speed_accel_deccel_position(self, accel, speed, deccel, position, buffer):
        self.__send_command(66)
        self.__write_long(accel)
        self.__write_long(speed)
        self.__write_long(deccel)
        self.__write_long(position)
        self.__write_byte(buffer)
        self.__write_checksum()
        return

    def set_mixed_speed_accel_deccel_position(self, accel1, speed1, deccel1, position1, accel2, speed2, deccel2, position2, buffer):
        self.__send_command(67)
        self.__write_long(accel1)
        self.__write_long(speed1)
        self.__write_long(deccel1)
        self.__write_long(position1)
        self.__write_long(accel2)
        self.__write_long(speed2)
        self.__write_long(deccel2)
        self.__write_long(position2)
        self.__write_byte(buffer)
        self.__write_checksum()
        return

    def read_temperature(self):
        self.__send_command(82)
        val = self.__read_word()
        if self.__validate_checksum():
            return val
        return -1

    def read_error_state(self):
        self.__send_command(90)
        val = self.__read_byte()
        if self.__validate_checksum():
            return val
        return -1

    def read_encoder_mode(self):
        self.__send_command(91)
        mode1 = self.__read_byte()
        mode2 = self.__read_byte()
        if self.__validate_checksum():
            return mode1, mode2
        return -1, -1

    def set_m1_encoder_mode(self, mode):
        self.__send_command(92)
        self.__write_byte(mode)
        self.__write_checksum()
        return

    def set_m2_encoder_mode(self, mode):
        self.__send_command(93)
        self.__write_byte(mode)
        self.__write_checksum()
        return

    def write_settings_to_eeprom(self):
        self.__send_command(94)
        self.__write_checksum()
        return
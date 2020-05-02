import wiringpi

# This module targets a dual mc33926 driver board, connected directly to the
# standard Raspberry Pi header pin layout

# Motor speeds for this library are specified as numbers
# between -MAX_SPEED and MAX_SPEED, inclusive.
_max_speed = 480  # 19.2 MHz / 2 / 480 = 20 kHz
MAX_SPEED = _max_speed

io_initialized = False
def io_init():
    global io_initialized
    if io_initialized:
        return

    wiringpi.wiringPiSetupGpio()
    wiringpi.pinMode(12, wiringpi.GPIO.PWM_OUTPUT)
    wiringpi.pinMode(13, wiringpi.GPIO.PWM_OUTPUT)

    wiringpi.pwmSetMode(wiringpi.GPIO.PWM_MODE_MS)
    wiringpi.pwmSetRange(MAX_SPEED)
    wiringpi.pwmSetClock(2)

    wiringpi.pinMode(22, wiringpi.GPIO.OUTPUT)
    wiringpi.pinMode(23, wiringpi.GPIO.OUTPUT)
    wiringpi.pinMode(24, wiringpi.GPIO.OUTPUT)
    wiringpi.pinMode(25, wiringpi.GPIO.OUTPUT)
    wiringpi.pinMode(26, wiringpi.GPIO.OUTPUT)
    wiringpi.pinMode(27, wiringpi.GPIO.OUTPUT)

    io_initialized = True

class Motor(object):
    MAX_SPEED = _max_speed

    def __init__(self, pwm_pin, dir1_pin, dir2_pin, en_pin):
        self.pwm_pin = pwm_pin
        self.dir1_pin = dir1_pin
        self.dir2_pin = dir2_pin
        self.en_pin = en_pin

    def enable(self):
        io_init()
        wiringpi.digitalWrite(self.en_pin, 1)

    def disable(self):
        io_init()
        wiringpi.digitalWrite(self.en_pin, 0)

    def setSpeed(self, speed):
        if speed < 0:
            speed = -speed
            dir1_value = 1
            dir2_value = 0
        else:
            dir1_value = 0
            dir2_value = 1

        if speed > MAX_SPEED:
            speed = MAX_SPEED

        io_init()
        wiringpi.digitalWrite(self.dir1_pin, dir1_value)
        wiringpi.digitalWrite(self.dir2_pin, dir2_value)
        wiringpi.pwmWrite(self.pwm_pin, speed)

class Motors(object):
    MAX_SPEED = _max_speed

    def __init__(self):
        self.motor1 = Motor(12, 24, 26, 22)
        self.motor2 = Motor(13, 25, 27, 23)  # Untested

    def enable(self):
        self.motor1.enable()
        self.motor2.enable()

    def disable(self):
        self.motor1.disable()
        self.motor2.disable()

    def setSpeed1(self, m1_speed):
        self.motor1.setSpeed(m1_speed)

    def setSpeed2(self, m2_speed):
        self.motor2.setSpeed(m2_speed)

    def setSpeeds(self, m1_speed, m2_speed):
        self.motor1.setSpeed(m1_speed)
        self.motor2.setSpeed(m2_speed)

motors = Motors()

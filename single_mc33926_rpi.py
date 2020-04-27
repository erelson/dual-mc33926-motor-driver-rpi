import wiringpi

# This module targets a mc33926 driver, connected to the standard Raspberry Pi
# header pin layout

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

  wiringpi.pwmSetMode(wiringpi.GPIO.PWM_MODE_MS)
  wiringpi.pwmSetRange(MAX_SPEED)
  wiringpi.pwmSetClock(2)

  wiringpi.pinMode(22, wiringpi.GPIO.OUTPUT)
  wiringpi.pinMode(24, wiringpi.GPIO.OUTPUT)
  wiringpi.pinMode(26, wiringpi.GPIO.OUTPUT)

  io_initialized = True

class Motor(object):
    MAX_SPEED = _max_speed

    def __init__(self, pwm_pin, dir_pin1, dir_pin2, en_pin):
        self.pwm_pin = pwm_pin
        self.dir_pin1 = dir_pin1
        self.dir_pin2 = dir_pin2
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
            dir_value1 = 1
            dir_value2 = 0
        else:
            dir_value1 = 0
            dir_value2 = 1

        if speed > MAX_SPEED:
            speed = MAX_SPEED

        io_init()
        wiringpi.digitalWrite(self.dir_pin1, dir1_value)
        wiringpi.digitalWrite(self.dir_pin2, dir2_value)
        wiringpi.pwmWrite(self.pwm_pin, speed)

class Motors(object):
    MAX_SPEED = _max_speed

    def __init__(self):
        self.motor1 = Motor(12, 24, 26, 22)

    def enable(self):
        self.motor1.enable()

    def disable(self):
        self.motor1.disable()

    def setSpeed(self, speed):
        self.motor1.setSpeed(speed)

motor = Motor()

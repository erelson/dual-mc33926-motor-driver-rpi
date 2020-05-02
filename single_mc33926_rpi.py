import RPi.GPIO as gpio

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

    gpio.setmode(gpio.BOARD)

    io_initialized = True

class Motor(object):
    MAX_SPEED = _max_speed

    def __init__(self, pwm_pin, dir1_pin, dir2_pin, en_pin):
        io_init()
        self.pwm_pin = pwm_pin
        self.dir1_pin = dir1_pin
        self.dir2_pin = dir2_pin
        self.en_pin = en_pin

        gpio.setup(self.pwm_pin, gpio.OUTPUT, initial=0)
        gpio.setup(self.dir1_pin, gpio.OUTPUT, initial=0)
        gpio.setup(self.dir2_pin, gpio.OUTPUT, initial=0)
        gpio.setup(self.en_pin, gpio.OUTPUT, initial=0)

        self.pwm = gpio.PWM(self.pwm_pin, 1000)

    def enable(self):
        gpio.output(self.en_pin, 1)
        self.pwm.start(0) # 0% duty cycle

    def disable(self):
        gpio.output(self.en_pin, 0)
        self.pwm.stop()

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

        gpio.output(self.dir1_pin, dir_value1)
        gpio.output(self.dir2_pin, dir_value2)
        self.pwm.ChangeDutyCycle(100. * abs(speed) / MAX_SPEED)

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

motor = Motors()

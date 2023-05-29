import RPi.GPIO as GPIO

class robot:
    def __init__(self):
        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False)
        self.AN2 = 13
        self.AN1 = 12
        self.DIG2 = 24
        self.DIG1 = 26
        GPIO.setup(self.AN2, GPIO.OUT)
        GPIO.setup(self.AN1, GPIO.OUT)
        GPIO.setup(self.DIG2, GPIO.OUT)
        GPIO.setup(self.DIG1, GPIO.OUT)
        self.p1 = GPIO.PWM(self.AN1, 100)
        self.p2 = GPIO.PWM(self.AN2, 100)

    def forward(self, left_speed, right_speed):
        GPIO.output(self.DIG1, GPIO.LOW)
        GPIO.output(self.DIG2, GPIO.LOW)
        self.p1.start(left_speed)
        self.p2.start(right_speed)

    def left_turn(self, speed):
        #30 is the min

        if speed < 30:
            GPIO.output(self.DIG1, GPIO.LOW)
            GPIO.output(self.DIG2, GPIO.HIGH)
            self.p1.start(30)
            self.p2.start(30)
        else:
            GPIO.output(self.DIG1, GPIO.LOW)
            GPIO.output(self.DIG2, GPIO.HIGH)
            self.p1.start(speed)
            self.p2.start(speed)


    def right_turn(self, speed):
        #30 is the min

        if speed < 30:
            GPIO.output(self.DIG1, GPIO.HIGH)
            GPIO.output(self.DIG2, GPIO.LOW)
            self.p1.start(30)
            self.p2.start(30)
        else:
            GPIO.output(self.DIG1, GPIO.HIGH)
            GPIO.output(self.DIG2, GPIO.LOW)
            self.p1.start(speed)
            self.p2.start(speed)

    def stop(self):
        GPIO.output(self.DIG1, GPIO.LOW)
        GPIO.output(self.DIG2, GPIO.LOW)
        self.p1.start(0)
        self.p2.start(0)
            
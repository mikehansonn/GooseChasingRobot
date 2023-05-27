import tkinter as tk
import RPi.GPIO as GPIO

check = False
window = tk.Tk()
label = tk.Label(text="Robot Controller")
label.config(font=('Helvetica bold', 26))
label1 = tk.Label(text="w           s           a           d")
label2 = tk.Label(text="forward, backward, spin left, spin right")
label1.config(font=('Helvetica bold', 15))
label2.config(font=('Helvetica bold', 15))

label.pack()
label1.pack()
label2.pack()

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
AN2 = 13
AN1 = 12
DIG2 = 24
DIG1 = 26
GPIO.setup(AN2, GPIO.OUT)
GPIO.setup(AN1, GPIO.OUT)
GPIO.setup(DIG2, GPIO.OUT)
GPIO.setup(DIG1, GPIO.OUT)
p1 = GPIO.PWM(AN1, 100)
p2 = GPIO.PWM(AN2, 100)


def forward():
    global GPIO
    global p1
    global p2

    GPIO.output(DIG1, GPIO.LOW)
    GPIO.output(DIG2, GPIO.LOW)
    p1.start(20)
    p2.start(20)
    print("forward function")


def backwards():
    global GPIO
    global p1
    global p2

    GPIO.output(DIG1, GPIO.HIGH)
    GPIO.output(DIG2, GPIO.HIGH)
    p1.start(20)
    p2.start(20)
    print("backwards function")


def left():
    global GPIO
    global p1
    global p2

    GPIO.output(DIG1, GPIO.LOW)
    GPIO.output(DIG2, GPIO.HIGH)
    p1.start(20)
    p2.start(20)
    print("spin left function")


def right():
    global GPIO
    global p1
    global p2

    GPIO.output(DIG1, GPIO.HIGH)
    GPIO.output(DIG2, GPIO.LOW)
    p1.start(20)
    p2.start(20)
    print("spin right function")


def stop(event):
    global check
    global GPIO
    global p1
    global p2
    if check:
        GPIO.output(DIG1, GPIO.LOW)
        GPIO.output(DIG2, GPIO.LOW)
        p1.start(0)
        p2.start(0)
        check = False


def handle_keypress(event):
    global check
    if event.char == 'w':  # forwards
        if not check:
            forward()
            check = True
    elif event.char == 's':  # backwards
        if not check:
            backwards()
            check = True
    elif event.char == 'a':  # left
        if not check:
            left()
            check = True
    elif event.char == 'd':  # right
        if not check:
            right()
            check = True


# Bind keypress event to handle_keypress()
window.bind("<Key>", handle_keypress)
window.bind('<KeyRelease>', stop)

window.mainloop()

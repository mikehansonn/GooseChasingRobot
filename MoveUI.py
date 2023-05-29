import tkinter as tk
import RPi.GPIO as GPIO

def tank_settings():
    global tank_true_terminator_false
    tank_true_terminator_false = True


def terminator_settings():
    global tank_true_terminator_false
    tank_true_terminator_false = False


def forward():
    global GPIO
    global DIG1
    global DIG2
    global p1
    global p2

    GPIO.output(DIG1, GPIO.LOW)
    GPIO.output(DIG2, GPIO.LOW)
    p1.start(20)
    p2.start(20)


def backwards():
    global GPIO
    global DIG1
    global DIG2
    global p1
    global p2


    GPIO.output(DIG1, GPIO.HIGH)
    GPIO.output(DIG2, GPIO.HIGH)
    p1.start(20)
    p2.start(20)


def left():
    global tank_true_terminator_false
    global GPIO
    global DIG1
    global DIG2
    global p1
    global p2
    
    if tank_true_terminator_false:
        GPIO.output(DIG1, GPIO.LOW)
        GPIO.output(DIG2, GPIO.HIGH)
        p1.start(20)
        p2.start(20)
    else:
        GPIO.output(DIG1, GPIO.LOW)
        GPIO.output(DIG2, GPIO.LOW)
        p1.start(20)
        p2.start(10)

    

def right():
    global tank_true_terminator_false
    global GPIO
    global DIG1
    global DIG2
    global p1
    global p2

    if tank_true_terminator_false:
        GPIO.output(DIG1, GPIO.HIGH)
        GPIO.output(DIG2, GPIO.LOW)
        p1.start(20)
        p2.start(20)
    else:
        GPIO.output(DIG1, GPIO.LOW)
        GPIO.output(DIG2, GPIO.LOW)
        p1.start(10)
        p2.start(20)


def stop(event):
    global GPIO
    global DIG1
    global DIG2
    global p1
    global p2
    global check

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



check = False
tank_true_terminator_false = True
window = tk.Tk()
label = tk.Label(text="Robot Controller")
label.config(font=('Helvetica bold', 26))
label1 = tk.Label(text="w           s           a           d")
label2 = tk.Label(text="forward, backward, spin left, spin right")
label1.config(font=('Helvetica bold', 15))
label2.config(font=('Helvetica bold', 15))

# Frame to hold the buttons
button_frame = tk.Frame(window)
button_frame.pack(pady=10)

tank_button = tk.Button(button_frame, text="Tank", command=tank_settings)
terminator_button = tk.Button(button_frame, text="Terminator", command=terminator_settings)
tank_button.pack(side='left',padx=20,pady=20)
terminator_button.pack(side='left',padx=20,pady=20)


button_frame.pack()
label.pack(side='bottom',padx=20,pady=20)
label1.pack(side='bottom',padx=20,pady=20)
label2.pack(side='bottom',padx=20,pady=20)

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



# Bind keypress event to handle_keypress()
window.bind("<Key>", handle_keypress)
window.bind('<KeyRelease>', stop)

window.mainloop()

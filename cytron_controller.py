import tkinter as tk
import SparkfungpsClass41
import RPi.GPIO as GPIO

def tank_settings():
    global tank_true_terminator_false

    tank_true_terminator_false = True
    option_label.config(text="Tank", fg="green")


def terminator_settings():
    global tank_true_terminator_false
    
    tank_true_terminator_false = False
    option_label.config(text="Terminator", fg="red")


def forward():
    GPIO.output(DIG1, GPIO.LOW)
    GPIO.output(DIG2, GPIO.LOW)
    p1.start(int(speed))
    p2.start(int(speed))


def backwards():
    GPIO.output(DIG1, GPIO.HIGH)
    GPIO.output(DIG2, GPIO.HIGH)
    p1.start(int(speed))
    p2.start(int(speed))


def left():
    percent = speed * differential
    
    if tank_true_terminator_false:
        GPIO.output(DIG1, GPIO.LOW)
        GPIO.output(DIG2, GPIO.HIGH)
        p1.start(int(speed))
        p2.start(int(speed))
    else:
        GPIO.output(DIG1, GPIO.LOW)
        GPIO.output(DIG2, GPIO.LOW)
        p1.start(int(speed))
        p2.start(percent)

    

def right():
    percent = speed * differential

    if tank_true_terminator_false:
        GPIO.output(DIG1, GPIO.HIGH)
        GPIO.output(DIG2, GPIO.LOW)
        p1.start(int(speed))
        p2.start(int(speed))
    else:
        GPIO.output(DIG1, GPIO.LOW)
        GPIO.output(DIG2, GPIO.LOW)
        p1.start(percent)
        p2.start(int(speed))


def stop(event):
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

def update_speed(value):
    global speed

    speed = int(value)


def update_differential(value):
    global differential

    differential = float(int(value)/100)


def plot_point():
    gps = SparkfungpsClass41.Gpsclass()
    list = gps.read_gps_broadcast()

    print(''.join([str(list[0]), ",", str(list[1])]))


differential = 0.75
speed = 50
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
option_label = tk.Label(text="Tank",fg="green")
button_frame = tk.Frame(window)
button_frame.pack(pady=10)
tank_button = tk.Button(button_frame, text="Tank", command=tank_settings,fg="green")
terminator_button = tk.Button(button_frame, text="Terminator", command=terminator_settings, fg="red")
tank_button.pack(side='left',padx=20,pady=20)
terminator_button.pack(side='left',padx=20,pady=20)

slider = tk.Scale(window, from_=1, to=100, orient=tk.HORIZONTAL, length=300, command=update_speed)
slider.pack(padx=20, pady=20)

differnetial_slider = tk.Scale(window, from_=1, to=100, orient=tk.HORIZONTAL, length=300, command=update_differential)
differnetial_slider.pack(padx=20, pady=20)

plot_coord_button = tk.Button(text="Plot Point", command=plot_point, fg="purple")

option_label.pack(side='top')
button_frame.pack()
slider.pack(padx=20,pady=20)
differnetial_slider.pack()
label.pack(side='bottom',padx=20,pady=20)
label1.pack(side='bottom',padx=20,pady=20)
label2.pack(side='bottom',padx=20,pady=20)
plot_coord_button.pack(side='bottom',padx=20,pady=20)

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

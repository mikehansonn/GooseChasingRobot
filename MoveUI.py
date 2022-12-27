import tkinter as tk

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


def forward():
    print("forward function")


def backwards():
    print("backwards function")


def left():
    print("spin left function")


def right():
    print("spin right function")


def stop(event):
    print("stop")


def handle_keypress(event):
    if event.char == 'w':  # forwards
        forward()
    elif event.char == 's':  # backwards
        backwards()
    elif event.char == 'a':  # left
        left()
    elif event.char == 'd':  # right
        right()


# Bind keypress event to handle_keypress()
window.bind("<Key>", handle_keypress)
window.bind('<KeyRelease>', stop)

window.mainloop()

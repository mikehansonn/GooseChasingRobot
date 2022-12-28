import tkinter as tk
import Cytronclass64

cytron = Cytronclass64.Cytronclass()
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


def forward(cytron1):
    cytron1.ramp_up(20, .01)
    print("forward function")


def backwards(cytron1):

    print("backwards function")


def left(cytron1):
    print("spin left function")


def right(cytron1):
    print("spin right function")


def stop(event, cytron1):
    # cytron1.recursiveStopMotors()
    print("stop")


def handle_keypress(event, cytron2):
    if event.char == 'w':  # forwards
        forward(cytron2)
    elif event.char == 's':  # backwards
        backwards(cytron2)
    elif event.char == 'a':  # left
        left(cytron2)
    elif event.char == 'd':  # right
        right(cytron2)


# Bind keypress event to handle_keypress()
window.bind("<Key>", lambda event, arg=cytron: handle_keypress(event, cytron))
window.bind('<KeyRelease>', lambda event, arg=cytron: stop(event, cytron))

window.mainloop()

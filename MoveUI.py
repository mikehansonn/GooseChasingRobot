import tkinter as tk
import Cytronclass64

cytron = Cytronclass64.Cytronclass()
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


def forward(cytron1, flag):
    cytron1.ramp_up(20, .01)
    print("forward function")


def backwards(cytron1):
    cytron1.ramp_up(-20, .01)
    print("backwards function")


def left(cytron1):
    print("spin left function")


def right(cytron1):
    print("spin right function")


def stop(event, cytron1):
    global check
    if check:
        cytron1.recursiveStopMotors()
        print("stop")
        check = False


def handle_keypress(event, cytron2):
    global check
    if event.char == 'w':  # forwards
        if not check:
            forward(cytron2)
            check = True
    elif event.char == 's':  # backwards
        if not check:
            backwards(cytron2)
            check = True
    elif event.char == 'a':  # left
        if not check:
            left(cytron2)
            check = True
    elif event.char == 'd':  # right
        if not check:
            right(cytron2)
            check = True


# Bind keypress event to handle_keypress()
window.bind("<Key>", lambda event, arg=cytron: handle_keypress(event, cytron))
window.bind('<KeyRelease>', lambda event, arg=cytron: stop(event, cytron))

window.mainloop()

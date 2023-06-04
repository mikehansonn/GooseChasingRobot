import tkinter as tk

number_of_points = -1


def main():
    global number_of_points
    window = tk.Tk()
    setup(window)
    window.mainloop()


def setup(window):
    global number_of_points

    how_many_points = tk.Label(text="How many points are you looking to plot?")
    how_many_points.pack()

    points_entry = tk.Entry()
    points_entry.pack()
    number_of_points = points_entry.get()

    continue_button = tk.Button(text="Continue?", command=lambda continue_button.pack_forget())
    continue_button.pack()


def continue_to_coordinate(window):
    plot_button = tk.Button(text="Save Coordinate", relief=tk.GROOVE)
    plot_button.pack()


if __name__ == "__main__":
    main()

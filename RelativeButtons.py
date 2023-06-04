import tkinter as tk
import csv
import point_to_point
import Cytronclass85c

current_position = 0

def move_new_point(lat, long):
    p2p2p = Cytronclass85c.Cytronclass()
    list = p2p2p.read_gps_correction_file("predator GPS correction file 2023-04-10.csv")
    p2p2p.navigate_point2point(lat, long, list[0])


def button_pressed(check_list, i):
    global current_position

    if i == current_position:
        print("you are already here")
    else:
        if float(check_list[i][3][current_position]) == 1:
            current_position = i
            move_new_point(check_list[i][1], check_list[i][2])
        else:
            if current_position < 12 <= i:
                move_new_point(check_list[8][1], check_list[8][2])
                current_position = 8
                if i >= 15:
                    move_new_point(check_list[14][1], check_list[14][2])
                    current_position = 14
                    if float(check_list[i][3][current_position]) == 1:
                        move_new_point(check_list[i][1], check_list[i][2])
                        current_position = i
                else:
                    if float(check_list[i][3][current_position]) == 1:
                        move_new_point(check_list[i][1], check_list[i][2])
                        current_position = i
            elif current_position < 14 < i:
                move_new_point(check_list[14][1], check_list[14][2])
                current_position = 14
                if float(check_list[i][3][current_position]) == 1:
                    move_new_point(check_list[i][1], check_list[i][2])
                    current_position = i
            elif current_position > 11 >= i:
                if current_position > 14:
                    move_new_point(check_list[14][1], check_list[14][2])
                    current_position = 14
                    move_new_point(check_list[8][1], check_list[8][2])
                    current_position = 8
                    if float(check_list[i][3][current_position]) == 1:
                        move_new_point(check_list[i][1], check_list[i][2])
                        current_position = i
                elif current_position > 11:
                    move_new_point(check_list[8][1], check_list[8][2])
                    current_position = 8
                    if float(check_list[i][3][current_position]) == 1:
                        move_new_point(check_list[i][1], check_list[i][2])
                        current_position = i
            elif current_position > 14 > i:
                move_new_point(check_list[14][1], check_list[14][2])
                current_position = 14
                if float(check_list[i][3][current_position]) == 1:
                    move_new_point(check_list[i][1], check_list[i][2])
                    current_position = i


def main():
    tuple_list = []
    master = tk.Tk()
    master.geometry("400x600")
    x = 50
    y = 25

    with open('backyarddata.txt') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        i = 0

        for row in csv_reader:
            tuple_list.append(
                [tk.Button(master, text=str(i), command=lambda m=i: button_pressed(tuple_list, m)), float(row[0]), float(row[1]),
                 row[2]])
            if i < 12:
                tuple_list[i][0].place(x=x, y=y)
                x = x + 100
                if (i + 1) % 4 == 0 and i != 0:
                    y = y + 100
                    x = 50
            elif i < 15:
                x = 50
                tuple_list[i][0].place(x=x, y=y)
                y = y + 100
            elif i == 15:
                tuple_list[i][0].place(x=150, y=525)
            elif i == 16:
                tuple_list[i][0].place(x=250, y=525)
            i = i + 1

    master.mainloop()


if __name__ == "__main__":
    main()
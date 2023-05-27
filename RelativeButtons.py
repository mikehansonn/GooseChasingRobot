import tkinter as tk
import csv

current_position = 0
current_x = 0
current_y = 0


def button_pressed(check_list, i):
    global current_position
    global current_x
    global current_y

    if i == current_position:
        print("you are already here")
    else:
        if float(check_list[i][3][current_position]) == 1:
            current_position = i
            # add movement code and update x and y
        else:
            if current_position < 12 <= i:
                # movement code to 8
                current_position = 8
                if i >= 15:
                    # movement code to 14
                    current_position = 14
                    if float(check_list[i][3][current_position]) == 1:
                        # add movement code and update x and y
                        current_position = i
                else:
                    if float(check_list[i][3][current_position]) == 1:
                        # add movement code and update x and y
                        current_position = i
            elif current_position < 14 < i:
                # movement code to 14
                current_position = 14
                if float(check_list[i][3][current_position]) == 1:
                    # add movement code and update x and y
                    current_position = i
            elif current_position > 11 >= i:
                if current_position > 14:
                    # movement code to 14
                    current_position = 14
                    # movement code to 8
                    current_position = 8
                    if float(check_list[i][3][current_position]) == 1:
                        # add movement code and update x and y
                        current_position = i
                elif current_position > 11:
                    # movement code to 8
                    current_position = 8
                    if float(check_list[i][3][current_position]) == 1:
                        # add movement code and update x and y
                        current_position = i
            elif current_position > 14 > i:
                # movement code to 14
                current_position = 14
                if float(check_list[i][3][current_position]) == 1:
                    # add movement code and update x and y
                    current_position = i
    print(current_position)

# Keys
#  0: 01111111111111100
#  1: 10111111111100000
#  2: 11011111111100000
#  3: 11101111111100000
#  4: 11110111111111100
#  5: 11111011111100000
#  6: 11111101111100000
#  7: 11111110111100000
#  8: 11111111011111100
#  9: 11111111101100000
# 10: 11111111110100000
# 11: 11111111111000000
# 12: 10001000100001100
# 13: 10001000100010100
# 14: 10001000100011011
# 15: 00000000000000101
# 16: 00000000000000110

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
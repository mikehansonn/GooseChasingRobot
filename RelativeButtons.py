import math
import tkinter as tk
import csv
import Cytronclass85c
import SparkfungpsClass41
import sys
from math import sin, cos, sqrt, atan2, radians

class rel:
    def __init__(self):
        self.tuple_list = []
        self.current_position = 0
        master = tk.Tk()
        master.geometry("400x600")
        x = 50
        y = 25

        with open('backyarddata.txt') as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')
            i = 0

            for row in csv_reader:
                self.tuple_list.append(
                    [tk.Button(master, text=str(i), command=lambda m=i: self.button_pressed(m)), float(row[0]), float(row[1]),
                    row[2]])
                if i < 12:
                    self.tuple_list[i][0].place(x=x, y=y)
                    x = x + 100
                    if (i + 1) % 4 == 0 and i != 0:
                        y = y + 100
                        x = 50
                elif i < 15:
                    x = 50
                    self.tuple_list[i][0].place(x=x, y=y)
                    y = y + 100
                elif i == 15:
                    self.tuple_list[i][0].place(x=150, y=525)
                elif i == 16:
                    self.tuple_list[i][0].place(x=250, y=525)
                i = i + 1

        master.bind('<KeyPress>', self.on_key_press)
        self.find_start_point()
        master.mainloop()


    def on_key_press(self, event):
        if event.char.lower() == 'q':
            sys.exit()


    def calculate_distance_two_points(self, lat, long):
        gps = SparkfungpsClass41.Gpsclass()
        list_gps = gps.read_gps_broadcast() # lat in 0 long in 1
        
        lat1 = radians(lat)
        lon1 = radians(long)
        lat2 = radians(list_gps[0])
        lon2 = radians(list_gps[1])

        radius = 6371

        dlat = lat2 - lat1
        dlon = lon2 - lon1

        a = sin(dlat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(dlon / 2) ** 2
        c = 2 * atan2(math.sqrt(a), sqrt(1 - a))
        distance_km = radius * c

        distance_m = distance_km * 1000

        return distance_m
    
    def calculate_two_given_points(self, lat1, long1, lat2, long2):
        lat1 = radians(lat1)
        lon1 = radians(long1)
        lat2 = radians(lat2)
        lon2 = radians(long2)

        radius = 6371

        dlat = lat2 - lat1
        dlon = lon2 - lon1

        a = sin(dlat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(dlon / 2) ** 2
        c = 2 * atan2(math.sqrt(a), sqrt(1 - a))
        distance_km = radius * c

        distance_m = distance_km * 1000

        return distance_m


    def find_start_point(self):
        biggest_distance = 10000000
        index = 0

        for i in range(len(self.tuple_list)):
            distance =  self.calculate_distance_two_points(self.tuple_list[i][1], self.tuple_list[i][2])
            if distance < biggest_distance:
                index = i
                biggest_distance = distance

        self.current_position = index


    def move_new_point(self, lat, long):
        p2p2p = Cytronclass85c.Cytronclass()
        list = p2p2p.read_gps_correction_file("predator GPS correction file 2023-04-10.csv")
        p2p2p.navigate_point2point(lat, long, list[0])


    def calculate_distance(self, i):
        current = self.current_position
        list = [] # [[distance, at, [route]], ...]

        for j in range(len(self.tuple_list)):
            if self.tuple_list[current][3][j] == "1":
                distance = self.calculate_two_given_points(self.tuple_list[current][1], self.tuple_list[current][2], self.tuple_list[j][1], self.tuple_list[j][2])
                sample = [distance, j, [j]]
                list.append(sample)
        for l in range(3):
            for j in range(len(list)):
                if list[j][2][len(list[j][2]) - 1] != i:
                    for k in range(len(self.tuple_list)):
                        if self.tuple_list[list[j][1]][3][k] == "1":
                            distance = self.calculate_two_given_points(self.tuple_list[list[j][1]][1], self.tuple_list[list[j][1]][2], self.tuple_list[k][1], self.tuple_list[k][2])
                            new_sample = [list[j][0] + distance, k, list[j][2] + [k]]
                            list.append(new_sample)

        return list


    def button_pressed(self, i):
        small_distance = 100000000
        go_to = []

        if self.tuple_list[self.current_position][3][i] == "1":
            self.move_new_point(self.tuple_list[i][1], self.tuple_list[i][2])
        else:
            list = self.calculate_distance(i)
            for j in range(len(list)):
                if list[j][0] < small_distance and list[j][2][-1] == i:
                    go_to = list[j][2]
                    small_distance = list[j][0]

            for q in range(len(go_to)):
                self.move_new_point(self.tuple_list[go_to[q]][1], self.tuple_list[go_to[q]][2])


def __main__():
    obj = rel()

if __name__ == "__main__":
    __main__()
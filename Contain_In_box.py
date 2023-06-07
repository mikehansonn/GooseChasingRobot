import TankInit
import SparkfungpsClass41
from math import sin, cos, sqrt, atan2, radians



def __init__(self, file_name):
    self.move = TankInit.robot()
    self.gps = SparkfungpsClass41.Gpsclass()
    self.gps_list = []
    self.equations = [] # make these as tuples but the slope is at 0 and the y intercept is at 1
    append_list = []

    with open(file_name, "r") as file:
        for line in file:
            if line.strip() == "inside":
                append_list.insert(0, 0)
                self.gps_list.append(append_list)
                append_list = []
            elif line.strip() == "outside":
                append_list.insert(0, 1)
                self.gps_list.append(append_list)
                append_list = []
            else:
                x, y = line.strip().split(',')
                point = [float(x), float(y)]
                append_list.append(point)

    make_slope_equations()
    


def is_inside_shape(self):
    for i in range(len(self.equations)):
        for j in range(len(self.equations[i])):
            coords = self.gps.get_coordinates() # lat in 0, long in 1



def make_slope_equations(self):
    add_list = []
    for i in range(len(self.gps_list)):
        for j in range(len(self.gps_list[i])):
            if j == 0:
                add_list.append(self.gps_list[i][j])
            else:
                if j < len(self.gps_list[i]) - 1:
                    add_list.append(find_slope(self.gps_list[i][j], self.gps_list[i][j + 1]))
                else:
                    add_list.append(find_slope(self.gps_list[i][j], self.gps_list[i][1]))

        self.equations.append(add_list)
        add_list = []


def find_slope(self, p1, p2):
    x1, y1 = p1
    x2, y2 = p2

    m = (y2 - y1) / (x2 - x1)
    b = y1 - m * x1

    return (m, b)
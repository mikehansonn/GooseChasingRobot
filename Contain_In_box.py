import TankInit
import SparkfungpsClass41
from math import sin, cos, sqrt, atan2, radians



def __init__(self, file_name):
    self.move = TankInit.robot()
    self.gps = SparkfungpsClass41.Gpsclass()
    self.gps_list = []
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

    


def is_inside_shape(point, shape_coordinates):
    x, y = point
    num_vertices = len(shape_coordinates)
    inside = False
    j = num_vertices - 1

    for i in range(num_vertices):
        if ((shape_coordinates[i][1] > y) != (shape_coordinates[j][1] > y)) and \
                (x < (shape_coordinates[j][0] - shape_coordinates[i][0]) * (y - shape_coordinates[i][1]) /
                     (shape_coordinates[j][1] - shape_coordinates[i][1]) + shape_coordinates[i][0]):
            inside = not inside
        j = i

    return inside

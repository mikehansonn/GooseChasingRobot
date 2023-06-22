#import Contain_In_box


class TraverseBox:
    def __init__(self, file_name):
        self.gps_coordinates = []
        self.list_of_boxes = []

        with open(file_name, "r") as file:
                for line in file:
                    x, y = line.strip().split(',')
                    self.gps_coordinates.append([float(x), float(y)])



        print(self.gps_coordinates)
        list = self.left_right_up_down()
        self.make_extra_lines(list)


    def left_right_up_down(self):
        left = 100000
        right = -100000
        down = 100000
        up = -100000

        for i in range(len(self.gps_coordinates)):
            x, y = self.gps_coordinates[i]

            if x < left:
                left = x
            if x > right:
                right = x
            if y < down:
                down = y
            if y > up:
                up = y    

        return left, right, down, up


    def make_extra_lines(self, extremes):
        x_split = abs(extremes[0] - extremes[1])/3
        y_split = abs(extremes[2] - extremes[3])/3

        x_equals = []
        y_equals = []

        for i in range(4):
            x_equals.append(extremes[0] + i * x_split)
            y_equals.append(extremes[2] + i * y_split)

        print("x_equals = ")
        print(x_equals)

        print("y_equals = ")
        print(y_equals)



#box = TraverseBox("traverse_box_points.txt")
box = TraverseBox("test_traverse_points.txt")
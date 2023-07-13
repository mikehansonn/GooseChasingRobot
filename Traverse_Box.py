#import Contain_In_box


class TraverseBox:
    def __init__(self, file_name):
        self.gps_coordinates = []
        self.outer_equations = []
        self.list_of_boxes = []

        with open(file_name, "r") as file:
                for line in file:
                    x, y = line.strip().split(',')
                    self.gps_coordinates.append([float(x), float(y)])

        list = self.left_right_up_down()
        self.x_equals_equations, self.y_equals_equations = self.make_extra_lines(list)
        self.make_slope_equations()

        print(self.gps_coordinates)
        print(self.outer_equations)
        print(self.x_equals_equations)
        print(self.y_equals_equations)


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

        return x_equals, y_equals


    def make_slope_equations(self):
        add_list = []
        for j in range(len(self.gps_coordinates)):
            if j < len(self.gps_coordinates) - 1:
                add_list.append(self.find_slope(self.gps_coordinates[j], self.gps_coordinates[j + 1]))
            else:
                add_list.append(self.find_slope(self.gps_coordinates[j], self.gps_coordinates[0]))

            self.outer_equations.append(add_list)
            add_list = []


    def find_slope(self, p1, p2):
        x1, y1 = p1
        x2, y2 = p2

        m = (y2 - y1) / (x2 - x1)
        b = y1 - m * x1

        return [m, b, (x1, y1), (x2, y2)]
    

#box = TraverseBox("traverse_box_points.txt")
box = TraverseBox("test_traverse_points.txt")
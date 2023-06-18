from math import sin, cos, sqrt, atan2, radians


class box:
    def __init__(self, file_name):
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

        self.make_slope_equations()
        print(self.equations)
        self.find_intercept()
        

    def find_intercept(self):
        coords = [41.62536983,-73.78451466]
        get_list = self.check_equations(coords)
        print(get_list)
 

    def check_equations(self, current_coordinate):
        checks = [[1, current_coordinate[0]], [0, current_coordinate[1]]]
        check_bools = [False, False]
        found_indexes = []
        append_list = []

        for i in range(len(checks)):
            for j in range(len(self.equations)):
                if j > 0:
                    bool_check = self.find_exact_intercept(self.equations[j], checks[i][0], checks[i][1])

                    if not bool_check:
                        pass
                    else:
                        check_bools[i] = True
                        append_list.append(bool_check)
            found_indexes.append(append_list)
            append_list = []

        check_bools[0] = self.check_higher_lower(0, found_indexes[1], checks[0][1])
        check_bools[1] = self.check_higher_lower(1, found_indexes[0], checks[1][1])

        return check_bools


        #true in box, false not in box
    def check_higher_lower(self, up_one_right_zero, intersections, original_value):
        low = 1000
        high = -1000
        
        for i in range(len(intersections)):
            print()
            print(intersections[i][up_one_right_zero])
            print(original_value)
            if intersections[i][up_one_right_zero] >= original_value and high == -1000:
                high = intersections[i][up_one_right_zero]
            elif  intersections[i][up_one_right_zero] <= original_value and low == 1000:
                low =  intersections[i][up_one_right_zero]

        if low != 1000 and high != -1000:
            print("low: ", low)
            print("original: ", original_value)
            print("high: ", high)
            return True
        else:
            return False
        

    #need to use this to check every equation for each y=/x= 
    def find_exact_intercept(self, slope_intercept, if_x, num): #if_x == 1, num is in x= form, if_x == 0, is y= form
        slope, intercept, p1, p2 = slope_intercept

        if if_x == 1:
            y_value = (slope * num) + intercept
            x_value = num
        else:
            x_value = (num - intercept)/slope
            y_value = num

        if x_value >= p1[0] and x_value <= p2[0] and y_value >= p1[1] and y_value <= p2[1]:
            return (x_value, y_value)
        elif x_value >= p1[0] and x_value <= p2[0] and y_value <= p1[1] and y_value >= p2[1]:
            return (x_value, y_value)
        elif x_value <= p1[0] and x_value >= p2[0] and y_value >= p1[1] and y_value <= p2[1]:
            return (x_value, y_value)
        elif x_value <= p1[0] and x_value >= p2[0] and y_value <= p1[1] and y_value >= p2[1]:
            return (x_value, y_value)
        else:
            return False 


    def make_slope_equations(self):
        add_list = []
        for i in range(len(self.gps_list)):
            for j in range(len(self.gps_list[i])):
                if j == 0:
                    add_list.append(self.gps_list[i][j])
                else:
                    if j < len(self.gps_list[i]) - 1:
                        add_list.append(self.find_slope(self.gps_list[i][j], self.gps_list[i][j + 1]))
                    else:
                        add_list.append(self.find_slope(self.gps_list[i][j], self.gps_list[i][1]))

            self.equations = add_list
            add_list = []


    def find_slope(self, p1, p2):
        x1, y1 = p1
        x2, y2 = p2

        m = (y2 - y1) / (x2 - x1)
        b = y1 - m * x1

        return [m, b, (x1, y1), (x2, y2)]


check = box("box_points.txt")
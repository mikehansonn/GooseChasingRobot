gps_list = []
append_list = []
equations = []

with open("points.txt", "r") as file:
    for line in file:
        if line.strip() == "inside":
            append_list.insert(0, 0)
            gps_list.append(append_list)
            append_list = []
        elif line.strip() == "outside":
            append_list.insert(0, 1)
            gps_list.append(append_list)
            append_list = []
        else:
            x, y = line.strip().split(',')
            point = [float(x), float(y)]
            append_list.append(point)

def make_slope_equations():
    add_list = []
    for i in range(len(gps_list)):
        for j in range(len(gps_list[i])):
            if j == 0:
                add_list.append(gps_list[i][j])
            else:
                if j < len(gps_list[i]) - 1:
                    add_list.append(find_slope(gps_list[i][j], gps_list[i][j + 1]))
                else:
                    add_list.append(find_slope(gps_list[i][j], gps_list[i][1]))

        equations.append(add_list)
        add_list = []


def find_slope(p1, p2):
    print(p1)
    print(p2)
    print()
    x1, y1 = p1
    x2, y2 = p2

    m = (y2 - y1) / (x2 - x1)
    b = y1 - m * x1

    return (m, b)



make_slope_equations()
print(equations)




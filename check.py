gps_list = []
append_list = []

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

print(gps_list)

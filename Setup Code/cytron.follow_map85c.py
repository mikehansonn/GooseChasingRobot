# 5.15.23 cytron.follow_map85c.py Use Cytronclass85c and test for erroneous RealTime calculations
# 5.8.23 cytron.follow_map85b.py created fixing infinite spinning
# 5.2.23 cytron.follow_map85a.py created using Cytronclass85a tweaking real time compass corrections
# 4.26.23 Cytronclass85.py upgrade, Final Location Statistics log
# 4.17.23 Cytronclass83.py upgrade, Real Time Compass corrections
# 4.11.23 Cytronclass82d.py
# 3.28.23 Cytronclass82b upgrade and reduced matrix print to just 4 elements plus total traverse time print.
# 3.20.23 Cytronclass81 upgrade
# 3.6.23 Cytronclass8 upgrade
# 3.5.23 cytron.follow_map.py started
# 2.9.23 test reading a map.csv file

import Cytronclass85c

cytron = Cytronclass85c.Cytronclass()

# initialize variables
map_matrix_index_first = 0
map_file_row_count = 0

map_filename = input("What is the map short name?")

if map_filename in "home_path":
    map_filename = "map_home_path.csv"
elif map_filename in "nest":
    map_filename = "map_nest.csv"
elif map_filename in "perimeter":
    map_filename = "map_perimeter.csv"
elif map_filename in "economs_corner":
    map_filename = "map_economs_corner.csv"
elif map_filename in "hicksons_corner":
    map_filename = "map_hicksons_corner.csv"
elif map_filename in "pond":
    map_filename = "map_pond.csv"
elif map_filename in "woods":
    map_filename = "map_woods.csv"
# if no existing map is recognized, the original map_filename is used as the file_name

# (0) START Read Map file into a matrix
# determine number of rows in the map
temp_file_handle = open(map_filename)  # file handle
# The following for loop counts all the rows in the file
for temp_iteration_variable in temp_file_handle:
    map_file_row_count = map_file_row_count + 1
print(map_filename, "has", map_file_row_count, "rows.")

# initiating map matrix
map_matrix = [0, 0, 0, 0]
count = 0
# load map_matrix with four zeros per row
for x in range(0, map_file_row_count, 1):  # initializing matrix from 0 to row_count, step=1
    map_matrix.append([0, 0, 0, 0])

# Open map file .csv and read into map_matrix
map_file_handle = open(map_filename)
# The following for loop will iterate through all lines of the file creating the matrix
for map_file_iteration_variable in map_file_handle:
    map_list = map_file_iteration_variable.rstrip('\n')  # first, strip off new line \n
    map_list = map_list.split(',')  # split into a list
    map_matrix[map_matrix_index_first] = map_list
    # print(map_list)
    # print(map_matrix[map_matrix_index_first])
    map_matrix_index_first = map_matrix_index_first + 1
print(map_filename, " has been read into follow_map.py...")

# print out the map matrix
print("Now printing Matrix:")
for count in range(0, map_file_row_count, 1):
    print(map_matrix[count][0:4])
# (0) END Read Map file into a matrix

# read in correction files
gps_correction_list, gps_correction_delta_list = cytron.read_gps_correction_file("predator GPS correction file 2023-04-10.csv")

# print(gps_correction_list)
# print("XXXXXXXXXX")
# print(gps_correction_delta_list)

target_waypoint = input("What is the name of the target waypoint?")

cytron.map_traverse(map_filename, target_waypoint, gps_correction_list)

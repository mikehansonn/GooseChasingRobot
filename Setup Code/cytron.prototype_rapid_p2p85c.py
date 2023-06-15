# 5.26.23 Adding more target points
# 5.15.23 cytron.prototype_rapid_p2p85c.py created checking RealTime compass corrections for erroneous calculations
# 5.8.23 cytron.prototype_rapid_p2p85b.py created fixing infinite spinning
# 5.1.23 cytron_prototype_rapid_p2p85a.py repairing RT correction to improve the RT corrections log
# 4.26.23 cytron_prototype_rapid_p2p85.py created to use Cytronclass85.py with real time compass correction tweaks (% increase correction)
# 4.24.23 cytron_prototype_rapid_p2p84.py created to use Cytronclass84.py with real time compass correction tweaks (% increase correction)
# 4.12.23 cytron_prototype_rapid_p2p83.py created to use Cytronclass83.py with real time compass corrections
# 4.10.23 cytron_prototype_rapid_p2p7e.py to utilize predator GPS correction file 2023-04-10.csv
# 4.3.23 CytronClass82d upgrade, 0.4 Multiplier added to shorten SL cycle and receive more GPS reads
# 3.29.23 CytronClass82c upgrade troubleshooting target heading corrections
# 3.21.23 Cytronclass82 upgrade with real time compass corrections
# 3.20.23 Cytronclass81 reduce printing in straightline and navigate_point2point
# 3.19.23 Cytronclass8 Upgrade with 100mS GPS read
# 2.24.23 Cytronclass76 Final Approach code for last GPS read added
# 2.22.23 correction file name updated to a 2.19 version
# 2.18.23 Cytronclass75 GPS drop solution found, now working on Final Approach coding
# 2.7.23 Cytronclass74a used to experiment with larger adjustment factors
# 1.28.23 Cytronclass73 function upgrade for log_an_event
# 1.25.23 Cytronclass72 for navigate_point2point modifications for GPS correction file input
# 1.25.23 cytron.prototype_rapid_p2p2.py adding GPS correction file read to pass it to navigate_point2point
# 1.14.23 cytron.prototype_rapid_p2p1.py fine tuning arriving at target point
# 1.5.22 cytron.prototype_rapid_p2p.py started
# 1.4.22 cytron.movetopoint1.py started, upgraded to SparkfungpsClass31 to fix GPS reading issue with queueing data
# 12.28.22 cytron.movetopoint.py started
# 12.28.22 navigate_coordinates1.py upgraded to correct get_heading_to_next_coordinate by subtracting atan2 from 360
# 12.21.22 Started navigate_coordinates.py

import Cytronclass85c
import sys
import SparkfungpsClass41
from time import sleep

cytron = Cytronclass85c.Cytronclass()  # execute Cytronclass __init__
sensor_gps = SparkfungpsClass41.Gpsclass()

if len(sys.argv) == 2:
    read_parameter = str(sys.argv[1])
else:
    read_parameter = "No input arguments were added!!"

# defaults: these variables need to be initialized
to_coordinate_x = 0
to_coordinate_y = 0
activate_return_to_starting_point = 0
starting_coordinate_x = 0
starting_coordinate_y = 0

# read input parameters
print("Input Arguments:", read_parameter)
if read_parameter == "-spearhead":
    print("Return Flag -spearhead found")
    activate_return_to_starting_point = 1
    starting_coordinate_x, starting_coordinate_y, time_stamp, x, y, hacc, hacc_status, temp_count = sensor_gps.read_gps_broadcast()
    print("Starting Coordinates:", starting_coordinate_x, starting_coordinate_y)

# reading in correction file
gps_correction_list = [0]
gps_correction_delta_list = [0]
count = 0
# load correction_list with 361 zeros to initialize list size (0-360 elements)
while count < 360: # initializing list to 361 elements (0-360)
    gps_correction_list.append(0)
    gps_correction_delta_list.append(0)
    count = count+1

gps_correction_list, gps_correction_delta_list = cytron.read_gps_correction_file("predator GPS correction file 2023-04-10.csv")

# print all the "To:" coordinate options.  "From:" is the coordinate of the current location.
print("center economs")
print("center backyard")
print("center hicksons")
print("center pond grangers")
print("center pool fence")
print("elbow")
print("drain")
print("basketball elbow")
print("5th stone")
print("goose main entrance")
print("mid1")
print("mid2")
print("midgh")
print("4m")
print("deep corner")
print("under tree") # dirt patch by wood pile tree
print("pond mid")
print("nest 10")
print("pool fence corner")
print("driveway1")
print("driveway2")
print("  ")
print("Use -spearhead flag when calling program:")
print("This will command an automatic return to the starting point...")
print("  ")

# start select target point from a set of hard coded points
move_to_point_name = input("What is the name of the target point?")
if move_to_point_name.lower() == "center economs":
    to_coordinate_x = 41.62536033
    to_coordinate_y = 73.7845110
elif move_to_point_name.lower() == "center backyard":
    to_coordinate_x = 41.62548604
    to_coordinate_y = 73.78442733
elif move_to_point_name.lower() == "center hicksons":
    to_coordinate_x = 41.62557783
    to_coordinate_y = 73.78435967
elif move_to_point_name.lower() == "center pond grangers":
    to_coordinate_x = 41.62555417
    to_coordinate_y = 73.78455967
elif move_to_point_name.lower() == "elbow":
    to_coordinate_x = 41.62534867
    to_coordinate_y = 73.78442750
elif move_to_point_name.lower() == "drain":
    to_coordinate_x = 41.6252715
    to_coordinate_y = 73.78428217
elif move_to_point_name.lower() == "basketball elbow":
    to_coordinate_x = 41.62521312
    to_coordinate_y = 73.78417304
elif move_to_point_name.lower() == "5th stone":
    to_coordinate_x = 41.62529495
    to_coordinate_y = 73.78404829
elif move_to_point_name.lower() == "goose main entrance":
    to_coordinate_x = 41.62538300
    to_coordinate_y = 73.78460909
elif move_to_point_name.lower() == "mid1":
    to_coordinate_x = 41.6252540425
    to_coordinate_y = 73.78411066625
elif move_to_point_name.lower() == "mid2":
    to_coordinate_x = 41.62524231375
    to_coordinate_y = 73.78422760625
elif move_to_point_name.lower() == "4m":
    to_coordinate_x = 41.62552
    to_coordinate_y = 73.78450967
elif move_to_point_name.lower() == "center pool fence":
    to_coordinate_x = 41.62540075
    to_coordinate_y = 73.784281750
elif move_to_point_name.lower() == "midgh":
    to_coordinate_x = 41.62556600
    to_coordinate_y = 73.78445967
elif move_to_point_name.lower() == "deep corner":
    to_coordinate_x = 41.62566283
    to_coordinate_y = 73.78444633
elif move_to_point_name.lower() == "pool fence corner":
    to_coordinate_x = 41.625357
    to_coordinate_y = 73.784334
elif move_to_point_name.lower() == "driveway1":
    to_coordinate_x = 41.625161
    to_coordinate_y = 73.78406817
elif move_to_point_name.lower() == "driveway2":
    to_coordinate_x = 41.62509429
    to_coordinate_y = 73.78396325
elif move_to_point_name.lower() == "under tree":
    to_coordinate_x = 41.62552
    to_coordinate_y = 73.78426633
elif move_to_point_name.lower() == "nest10":
    to_coordinate_x = 41.6254895
    to_coordinate_y = 73.784592
elif move_to_point_name.lower() == "pond mid":
    to_coordinate_x = 41.62555866
    to_coordinate_y = 73.7845375
else:
    print("No matching hard coded To point")
    print("Quitting Code!!")
    quit()
    # save this old code for eventual switching to a file instead of hard code
    # open txt file for data_to_write
    # measurement_time_stamp = datetime.datetime.now()
    # obstacles_file_name = "obstacles_file.txt"
    # print("Opening text file for obstacle coordinate data:", obstacles_file_name)
    # write_file_handle = open(obstacles_file_name, 'w')
# end select target point from a set of hard coded points

try:
    cytron.navigate_point2point(to_coordinate_x, to_coordinate_y, gps_correction_list)
    print("Returned from navigate_point2point function")
    print("$$$$$$$$$$ Robot arrived at Waypoint:", move_to_point_name)
    if activate_return_to_starting_point == 1:
        sleep(1)
        print("Now returning to starting point:", starting_coordinate_x, starting_coordinate_y)
        cytron.navigate_point2point(starting_coordinate_x, starting_coordinate_y, gps_correction_list)
        print("$$$$$$$$$$ Robot returned to original Starting point")

except KeyboardInterrupt:  # exit program when keyboard interrupt
    print("cytron.prototype_rapid_p2pXX.py exception detected")
    cytron.recursiveStopMotors()
    print("about to execute QUIT")
    quit()

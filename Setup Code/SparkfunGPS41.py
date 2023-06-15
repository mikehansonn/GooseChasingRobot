# 3.14.23 SparkfunGPS41.py started, adding averageGPS read time and Max GPS Read time
# 2.2.23 SparkfunGPS4.py started, creating a GPS broadcast mechanism by writing GPS coordinates to a file
# 1.23.23 SparkfunGPS3.py replacing main GPS-read code with equivalent SparkfungpsClass32 get_bearing function call
# 11.14.22 Adding Drift Calculation
# 11.14.22 updated position data to 8 decimal digits
# 11.14.22 Started SparkfunGPS2.py
# 9.14.22 SparkfunGPS.test.py initial test of SparkFun RTK GPS

import SparkfungpsClass34
import Watchdogclass1
from time import time           # import for real time monitoring
import sys

sensor_gps = SparkfungpsClass34.Gpsclass()
watchdog = Watchdogclass1.Watchdogclass()

# initialize variables
total_readings_count = 0
lat_max = 0
lat_min = 0
longi_max = 0
longi_min = 0
last_gps_read_time_stamp = time()
max_gps_read_time = 0
avg_gps_read_time = 1 # start with a high time and let average reduce over time

try:
    while True:
        # take gps measurement with watchdog
        watchdog.watchdog_call("gps", "start", 2)
        lat, longi = sensor_gps.get_coordinates()
# need to add get_hacc here, probably need to combine this with get_coordinates otherwise may kick off new epoch
        watchdog.watchdog_call("gps", "stop", 2)

# start Average GPS Read calculation
        # weight the average number 90% and the newest measurement 10%
        # this allows drifting of GPS measurement time to gradually influence the average time
        this_gps_read_time_stamp = time()
        this_gps_read_time = this_gps_read_time_stamp - last_gps_read_time_stamp
        # weight the average GPS value as 90% and the newest time measurement as 10%
        avg_gps_read_time = (avg_gps_read_time*9 + this_gps_read_time)/10
        if this_gps_read_time > max_gps_read_time:
            max_gps_read_time = this_gps_read_time # overwrite old max GPS read time
        last_gps_read_time_stamp = this_gps_read_time_stamp # update last_gps_read_time for next loop
# end Average GPS Read calculation

# WRITE TO BROADCAST FILE started
        gps_broadcast_file_name = "gps_broadcast.txt"
        write_gps_broadcast_file_handle = open(gps_broadcast_file_name, 'w+')
        print("Writing GPS Broadcast Avg Read Time:", f"{avg_gps_read_time:.2f}", "Max Read Time:", f"{max_gps_read_time:.2f}")
        # print("Writing GPS Broadcast w/ timestamp:", this_gps_read_time_stamp)

        data_to_write = (str(lat) + "," + str(longi) + "," + str(this_gps_read_time_stamp) + "," + str(avg_gps_read_time) + "," + str(max_gps_read_time))  # Writing broadcast file
        write_gps_broadcast_file_handle.write(data_to_write)
        write_gps_broadcast_file_handle.close()
# WRITE TO BROADCAST FILE complete

        # set min/max readings during first 5 measurements
        total_readings_count = total_readings_count + 1
        if total_readings_count == 5:  # set initial values of min and max after 5 readings
            lat_max = float(lat)
            lat_min = float(lat)
            longi_max = float(longi)
            longi_min = float(longi)
            print("Min and Max variables set after first 5 readings")

        # calculate drift for next 15 measurements, then reset count and start new min/max readings
        if total_readings_count > 5:  # delay drift calculation till after first 5 total_readings_count
            if float(lat) > lat_max:
                lat_max = float(lat)  # set lat max to new higher reading
            if float(lat) < lat_min:
                lat_min = float(lat)  # set lat min to new lower reading
            if float(longi) > longi_max:
                longi_max = float(longi)  # set longi max to new higher reading
            if float(longi) < longi_min:
                longi_min = float(longi)  # set lat longi to new higher reading
            lat_drift = (lat_max - lat_min) * 100000000
            longi_drift = (longi_max - longi_min) * 100000000
            print("Latitude Drift**> ", int(lat_drift), "  Longitude Drift**> ", int(longi_drift), "Total Readings:", total_readings_count)
            if total_readings_count > 50:
                total_readings_count = 1  # clear the total after 20 readings and start recalculating drift

except KeyboardInterrupt:
    sys.exit(0)

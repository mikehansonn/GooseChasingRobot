# 4.9.23 added a "bad data" loop to read_gps_broadcast
# 3.18.23 SparkfungpsClass41.py fixed get_coordinates to return coordinates, hacc and hacc_status all in function call
# 3.15.23 SparkfungpsClass4.py Upgrade get_coordinates with pyubx2.UBXReader.read(), 100mS GPS cycletime & hacc read
# 2.24.23 SparkfungpsClass33.py coding calculate_my_current_speed
# 1.23.23 SparkfungpsClass32.py turning off print statements in debug of 31
# 1.4.23 SparkfungpsClass31.py started to debug queueing of GPS data by manipulating serial commands
# 1.3.23 SparkfungpsClass3.py started to debug movetopoint.py
# 12.28.22 Correcting get_heading_to_next_coordinate by subtracting atan2 result from 360 to determine angle
# 12.21.22 Adding coordinate direction and coordinate distance
# 11.23.22 Started SparkfungpsClass.py

import math
from serial import Serial
from pyubx2 import UBXReader
from time import time
import fontstyle


class Gpsclass:
    def __init__(self):
        # print("Running Gpsclass().__init__()")
        self.bad_read_gps_broadcast_count = None
        self.repeat_read_gps_broadcast = None
        self.count = None
        self.max_gps_read_time = None
        self.avg_gps_read_time = None
        self.red_alert = None
        self.orange_alert = None
        self.yellow_alert = None
        self.green_alert = None
        self.blue_alert = None
        self.gngll_read_done = None
        self.posllh_read_done = None
        self.speed_mph = None
        self.speed_mps = None
        self.time_between_coordinates = None
        self.y_coordinate = None
        self.x_coordinate = None
        self.gps_broadcast_file_handle = None
        self.gps_broadcast_file_name = None
        self.hypotenuse = None
        self.slope = None
        self.position = None
        self.mm_mmmm = None
        self.degrees = None
        self.decimal_value = None
        self.last_time_stamp = None
        self.hacc_status = None
        self.heading_to_next_coordinate = None
        self.gps_read_cycle_time = None
        self.longi = None
        self.temp2 = None
        self.lat = None
        self.hacc = None
        self.hacc_substring = None
        self.parsed_data_list = None
        self.parsed_data_string = None
        self.temp1 = None
        self.ubr = None
        self.stream = None
        self.metres_between_coordinates = None
        self.time_stamp = None
        self.gps_broadcast_read_iteration_variable = None
        self.gps_broadcast_data = None
        # self.ser = serial.Serial("/dev/ttyS0", 38400)  # 1.4.23 configure serial port and open port
        # print(self.ser.is_open, "<<<If True Serial port is Open during Gpsclass __init__")
        # self.ser.close() # 1.9.23 added back in
        # print(self.ser.is_open, "<<<If False Serial port is Closed during Gpsclass __init__")
        self.gngll_info = "$GNGLL"

    def get_coordinates(self):
        self.last_time_stamp = time()

        self.stream = Serial('/dev/ttyS0', 38400, timeout=3)
        self.ubr = UBXReader(self.stream)
        self.posllh_read_done = 0
        self.gngll_read_done = 0

        while True:

            (self.raw_data, self.parsed_data) = self.ubr.read()
            # print(parsed_data)
            self.parsed_data_string = str(self.parsed_data)
            self.parsed_data_list = self.parsed_data_string.split(',')

            # parse out hacc data and create hacc_status
            if self.parsed_data_list[0] == "<UBX(NAV-POSLLH":
                self.hacc_substring = self.parsed_data_list[6]
                self.hacc = int(self.hacc_substring[6:10])
                if self.hacc < 20:
                    self.blue_alert = fontstyle.apply('>>>> LOCKED <<<<', 'bold/white/blue_BG')
                    self.hacc_status = self.blue_alert
                elif self.hacc < 75:
                    self.green_alert = fontstyle.apply('$$$$$ GREEN $$$$$', 'bold/white/green_BG')
                    self.hacc_status = self.green_alert
                elif self.hacc < 150:
                    self.yellow_alert = fontstyle.apply('///// YELLOW /////', 'bold/white/yellow_BG')
                    self.hacc_status = self.yellow_alert
                elif self.hacc < 240:
                    self.orange_alert = fontstyle.apply('!!!!! ORANGE !!!!!', 'bold/white/purple_BG')
                    self.hacc_status = self.orange_alert
                else:
                    self.red_alert = fontstyle.apply('XXXX RED ALERT XXXXX', 'bold/white/red_BG')
                    self.hacc_status = self.red_alert
                # print("hacc:", self.hacc, self.hacc_status)
                self.posllh_read_done = 1

            # parse out coordinates and determine GPS Read cycle time
            if self.parsed_data_list[0] == "<NMEA(GNGLL":
                self.temp1 = self.parsed_data_list[1]
                self.lat = float(self.temp1[5:16])
                self.temp2 = (self.parsed_data_list[3])
                self.longi = float(self.temp2[6:17])  # 6-17 strips leading '-'
                # print("Latitude:", self.lat, "Longitude:", self.longi)
                # determine GPS Read cycle time
                self.gps_read_cycle_time = time() - self.last_time_stamp
                # print("GPS Read Cycle Time:", self.gps_read_cycle_time)
                self.last_time_stamp = time()  # prepare for next loop
                self.gngll_read_done = 1

            if self.posllh_read_done and self.gngll_read_done:
                return self.lat, self.longi, self.hacc, self.hacc_status

    def convert_to_degrees(self, raw_value):
        self.decimal_value = raw_value / 100.00
        self.degrees = int(self.decimal_value)
        self.mm_mmmm = (self.decimal_value - int(self.decimal_value)) / 0.6
        self.position = self.degrees + self.mm_mmmm
        self.position = float("%.8f" % self.position)
        return self.position

    def get_heading_to_next_coordinate(self, from_coordinate_x, from_coordinate_y, to_coordinate_x, to_coordinate_y):
        # Mikey's Angle Calculator 12.21.22

        self.slope = math.atan2((to_coordinate_y - from_coordinate_y), (to_coordinate_x - from_coordinate_x))

        self.slope = (self.slope * 180) / math.pi  # convert to degrees

        if self.slope < 0:
            self.slope = self.slope + 360

        self.heading_to_next_coordinate = 360-self.slope

        return self.heading_to_next_coordinate

    def get_distance_to_next_coordinate(self, from_coordinate_x, from_coordinate_y, to_coordinate_x, to_coordinate_y):

        self.hypotenuse = math.sqrt((to_coordinate_y - from_coordinate_y) ** 2 + (to_coordinate_x - from_coordinate_x) ** 2)

        self.metres_between_coordinates = self.hypotenuse * 100000 * 1.11
        # 100,000 moves the decimal point to the 5th digit which is meteres
        # since it is not exactly metres, 1.11 multiplier converts it to actual metres
        # http://wiki.gis.com/wiki/index.php/Decimal_degrees

        return self.metres_between_coordinates

    def read_gps_broadcast(self):
        self.bad_read_gps_broadcast_count = 0
        self.repeat_read_gps_broadcast = 1
        while self.repeat_read_gps_broadcast == 1:
            self.gps_broadcast_file_name = "/home/pi/robot/cytron/gps_broadcast.txt"
            self.gps_broadcast_file_handle = open(self.gps_broadcast_file_name, 'r+')
            for self.gps_broadcast_read_iteration_variable in self.gps_broadcast_file_handle:
                self.gps_broadcast_data = self.gps_broadcast_read_iteration_variable.split(",")  # create list by splitting string into coordinates and time stamp
            if self.gps_broadcast_data is None: # this has to be first check otherwise everything else abends
                print("GPS Broadcast Read was empty causing NoneType")
                self.repeat_read_gps_broadcast = 1
                self.bad_read_gps_broadcast_count = self.bad_read_gps_broadcast_count + 1
                if self.bad_read_gps_broadcast_count == 10:
                    print("10 BAD read_gps_broadcast loops, calling QUIT()")
                    quit()
            elif len(self.gps_broadcast_data) == 8:
                self.x_coordinate = float(self.gps_broadcast_data[0])
                self.y_coordinate = float(self.gps_broadcast_data[1])
                self.time_stamp = float(self.gps_broadcast_data[2])
                self.avg_gps_read_time = float(self.gps_broadcast_data[3])
                self.max_gps_read_time = float(self.gps_broadcast_data[4])
                self.hacc = int(self.gps_broadcast_data[5])
                self.hacc_status = str(self.gps_broadcast_data[6])
                self.count = int(self.gps_broadcast_data[7])
                self.repeat_read_gps_broadcast = 0 # do not reread GPS broadcast file and just return data
            else:
                print("BAD GPS data in ", self.gps_broadcast_file_name)
                self.repeat_read_gps_broadcast = 1
                self.bad_read_gps_broadcast_count = self.bad_read_gps_broadcast_count + 1
                if self.bad_read_gps_broadcast_count == 10:
                    print("10 BAD read_gps_broadcast loops, calling QUIT()")
                    quit()
        return self.x_coordinate, self.y_coordinate, self.time_stamp, self.avg_gps_read_time, self.max_gps_read_time, self.hacc, self.hacc_status, self.count

    def calculate_my_current_speed(self, now_coordinate_x, now_coordinate_y, now_time_stamp, last_coordinate_x, last_coordinate_y, last_time_stamp):
        self.metres_between_coordinates = self.get_distance_to_next_coordinate(now_coordinate_x, now_coordinate_y, last_coordinate_x, last_coordinate_y)
        self.time_between_coordinates = now_time_stamp - last_time_stamp
        self.speed_mps = self.metres_between_coordinates / self.time_between_coordinates
        self.speed_mph = self.speed_mps*3600*(1/1609) # 3600 converts m/sec to m/hour 1/1609 converts m/hour to mph
        print(self.metres_between_coordinates, "meters @", self.time_between_coordinates, "seconds is", self.speed_mps, "mps or", self.speed_mph, "mph.")
        return self.speed_mps, self.speed_mph
    
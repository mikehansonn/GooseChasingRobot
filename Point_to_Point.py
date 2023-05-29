import math
import TankInit
import SparkfungpsClass41
import gy271compassrobot81
from math import sin, cos, sqrt, atan2, radians

class p2p:
    # lat long are the ones we want to go to, current location stored in new_gps 
    def __init__(self, latitude, longitude):
        self.bot = TankInit.robot()
        self.latitude = latitude
        self.longitude = longitude
        self.sensor_gps = SparkfungpsClass41.Gpsclass()
        self.sensor_compass = gy271compassrobot81.compass()
        self.desired_angle = 0


    def find_new_angle(self):
        list_gps = self.sensor_gps.get_coordinates()
        self.desired_angle = math.atan2((self.longitude - list_gps[1]), (self.latitude - list_gps[0]))

        self.desired_angle = (self.desired_angle * 180)/math.pi

        if self.desired_angle < 0:
            self.desired_angle = self.desired_angle + 360


    def find_correct_angle_direction(self):
        list_compass = self.sensor_compass.get_bearing()
        self.increment_or_decrement = 1  # 1 for increment -1 for decrement
        at_angle = list_compass[0]

        clockwise_distance = (self.desired_angle - at_angle) % 360
        counterclockwise_distance = (at_angle - self.desired_angle) % 360

        if clockwise_distance < counterclockwise_distance:
            self.increment_or_decrement = -1


    def calculate_distance_two_points(self):
        list_gps = self.sensor_gps.get_coordinates()
        lat1 = radians(self.latitude)
        lon1 = radians(self.longitude)
        lat2 = radians(list_gps[0])
        lon2 = radians(list_gps[1])

        radius = 6371

        dlat = lat2 - lat1
        dlon = lon2 - lon1

        a = sin(dlat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(dlon / 2) ** 2
        c = 2 * atan2(math.sqrt(a), sqrt(1 - a))
        distance_km = radius * c

        distance_m = distance_km * 1000

        return distance_m
    

    def calculate_distance_two_angles(self):
        list_compass = self.sensor_compass.get_bearing()
        diff = abs(self.desired_angle - list_compass[0])
    
        # Handle the wraparound case
        if diff > 180:
            diff = 360 - diff

        return diff
    

    def go_to_next_point(self):
        self.find_new_angle()
        self.find_correct_angle_direction()
        
        while self.calculate_distance_two_angles() > 3:
            if self.calculate_distance_two_angles() > 50:
                if self.increment_or_decrement == 1:
                    self.bot.left_turn(100)
                else:
                    self.bot.right_turn(100)
            elif self.calculate_distance_two_angles() > 30:
                if self.increment_or_decrement == 1:
                    self.bot.left_turn(50)
                else:
                    self.bot.right_turn(50)
            elif self.calculate_distance_two_angles() > 10:
                if self.increment_or_decrement == 1:
                    self.bot.left_turn(30)
                else:
                    self.bot.right_turn(30)
        
        self.bot.stop()

        while self.calculate_distance_two_points() > .5:
            if self.calculate_distance_two_points() > 3:
                self.bot.forward(100, 100)
            elif self.calculate_distance_two_points() > 2:
                self.bot.forward(75, 75)
            elif self.calculate_distance_two_points() > 1:
                self.bot.forward(50, 50)





to_coordinate_x = 41.62548604
to_coordinate_y = 73.78442733

point = p2p(to_coordinate_x,to_coordinate_y)
point.go_to_next_point()
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
            
        self.desired_angle = 360 - self.desired_angle


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
        diff = abs(self.desired_angle - list_compass[0] - 12.9)
        # Handle the wraparound case
        if diff > 180:
            diff = 360 - diff

        return diff
    

    def turn_to_angle(self):
        self.find_new_angle()
        self.find_correct_angle_direction()

        while self.calculate_distance_two_angles() > 10:
            self.find_correct_angle_direction()
            if self.calculate_distance_two_angles() > 75:
                if self.increment_or_decrement == 1:
                    self.bot.left_turn(90)
                else:
                    self.bot.right_turn(90)
            elif self.calculate_distance_two_angles() > 50:
                if self.increment_or_decrement == 1:
                    self.bot.left_turn(70)
                else:
                    self.bot.right_turn(70)
        
        self.bot.stop()


    def adjust_when_moving(self, value):
        self.find_new_angle()
        self.find_correct_angle_direction()
        difference_value = self.calculate_distance_two_angles()
        if self.increment_or_decrement == 1:
            left_motor = value
            right_motor = value - (difference_value * 2)
        else:
            left_motor = value - (difference_value * 2)
            right_motor = value

        return left_motor, right_motor


    def go_to_next_point(self):
        self.turn_to_angle()

        while self.calculate_distance_two_points() > .25:
            self.find_new_angle()
            if self.calculate_distance_two_points() > 3:
                list = self.adjust_when_moving(100)
            else:
                list = self.adjust_when_moving(80)

                
            self.bot.forward(list[0], list[1])
        
        self.bot.stop()


point = p2p(41.625455, 73.78449066)
point.go_to_next_point()
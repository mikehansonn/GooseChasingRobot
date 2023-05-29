 # 5.13.23 Added comments with this date as future Patrol() code
# 5.11.23 Cytronclass85c started, figuring out if real time compass adjustments are + or -
# 5.8.23 Cytronclass85b started, working on fixing infinite spinning problem
# 4.30.23 Cytronclass85a started, corrected RT compass correction calculation around 0/360 boundary
# 4.27.23 Deflection from a straight line bewtween "From" and "To" coordinate calculated and logged
# 4.26.23 Cytronclass85 started (skipped Cytronclass84 function which did not work)
# 4.10.23 Cytronclass83 started, designing real-time compass correction
# 4.3.23 Cytronclass82d started, experimenting changing SL from max 1 second sleep to .05 second
# 3.24.23 Cytronclass82b started, redefining target_heading_corrected as target_heading-file/correction
# 3.20.23 Cytronclass82 started, adding Real Time Compass corrections to navigate_point2point
# 3.20.23 Cytronclass81 minimizing print statements in Straight_line and navigate_point2point
# 3.6.23 Cytronclass8 added map_traverse and read_gps_correction_file functions
# 2.24.23 Cyronclass76 Final approach coding for last leg after final GPS read, forces cruisetime to end at target point.
# 2.18.23 Cytronclass75 Final Approach coding of navigate_point2point
# 2.7.23 Cytronclass74a experimenting with straight_line adjustment factor line 805
# 2.3.23 Cytronclass74 started, replacing GPS read with retrieving the GPS measurements from the broadcast file
# 1.28.23 Cytronclass73 started, added log_an_event calls to navigate_point2point
# 1.25.23 Cytronclass72 started, added gps_correction_list to navigate_point2point
# 1.14.23 Cytronclass71 started, fine tuning navigate_point2point & adding GPS watchdog to navigate_p2p
# 1.4.23 Cytronclass7.py started, creating navigate_point2point function from cytron.movetopoint1.py
# 12.5.22 gy271compassrobot8 changed to include a self.drdy_polling_error_flag which gets returned from get_bearing
# 12.2.22 Cytronclass64.py modified 75% and 90% turn speeds AND reduced incremental correction step to .0156 seconds or ~1degree
# 12.2.22 Cytronclass63.py further fine tuning and debugging both left and right spins
# 11.30.22 Cytronclass62.py started Fine Tuning Spin function by adding overshoot/correction code
# 11.16.22 Cytronclass6.py started to include Spin functionality based on turnto code execution
# 11.8.22 gy271compassrobot7 change with new try except continue errors for compass drdy error
# 11.8.22 Modified Try Except for .move() and .straightline() to catch Compass errors and force Motor Stops
# 8.29.22 Cytronclass53.py started, creating straightline() function from straightline9.py
# 8.18.22 Cytronclass52.py started, creating rampup and rampdown functions
# 8.15.22 Cytronclass51.py correcting compass bouncing for 0/360 compass crossing
# 8.12.22 Debug turnto
# 8.5.22 Cytronclass5.py started, adding turnto functionality to move()
# 8.4.22 uturnleft verified
# 8.3.22 uturnright and previous commands from Cytronclass3 confirmed functional
# 7.29.22 Cytronclass4 started to add uturnleft and uturnright function
# 7.15.22 Adding rockmeloose() For Loop Range increment of 5 to speed up ramp-up and ramp-down
# 7.11.22 Cytronclass2 Adding ramp-up and ramp-down code encapsulating full speed operation
# 7.11.22 Cytronclass2 Adding 5 Recursive Stop
# 7.4.22 Start Cytronclass1.py eliminating "self" from variables being used in a function
# 7.3.22 Start Cytronclass.py

import RPi.GPIO as GPIO  # using Rpi.GPIO module
from time import sleep  # import function sleep for delay
from time import time  # import for real time monitoring in straight_line
# import sys
import gy271compassrobot81 as GY271
# 7.29.22 Adding compass functionality
# 8.1.22 gy271compassrobot6 started, clean up get_bearing with self. and exception handling
import SparkfungpsClass41
# 2.24.23 Adding GPS functionality navigate_point2point that includes mps and mph calculation
import Watchdogclass1
# 4.27.23
import math
import fontstyle


# 1.14.23 Adding GPS Watchdog functionality to navigate_p2p


class Cytronclass():

    def __init__(self):
        # Initialize Cytron Motor Driver
        self.start_heading = None
        self.special_condition_count = None
        self.crossed_end_boundary = None
        self.temp_now_heading = None
        self.crossed_0_360_boundary = None
        self.skipped_first_waypoint_flag = None
        self.traverse_start_time = None
        self.gps_stall_flag = None
        self.gps_stall_count = None
        self.delta_count = None
        self.distance_traveled_after_motion = None
        self.current_atan2_heading_after_motion = None
        self.snapshot_target_heading_corrected = None
        self.update_previous_coordinate_flag = None
        self.previous_coordinate_x = None
        self.previous_coordinate_y = None
        self.first_straightline_flag = None
        self.fresh_gps_broadcast_read = None
        self.correction_steps_count = None
        self.overshoot_angle = None
        self.opposite_start_heading = None
        self.turnto_command = None
        self.end_heading = None
        self.compass_turn_command = None
        self.spin_command = None
        self.time_navp2p_loop_start = None
        self.clock_position = None
        self.clock_position_angle = None
        self.final_now_heading = None
        self.final_target_heading = None
        self.final_target_distance = None
        self.turn_command = None
        self.delta_turn_angle = None
        self.angle_add_75 = None
        self.angle_add_90 = None
        self.heading_75 = None
        self.heading_90 = None
        self.stop_spin_overshoot_correction = None
        self.cross_key_boundary = None
        self.compass_bounce_detected = None
        self.crossed_key_boundary = None
        self.previous_heading = None
        self.compass_turn_ramp_down = None
        self.gps_correction_delta_list = None
        self.traverse_running_time_seconds = None
        self.traverse_running_time_minutes = None
        self.ramp_step_time = None
        self.move_forward_flag = None
        self.move_backward_flag = None
        self.gps_operation_prevent_stop_motors_flag = None
        self.hacc_status = None
        self.hacc = None
        self.block_real_time_compass_correction = None
        self.start_time = None
        self.stop_time = None
        self.drdy_polling_error_flag = None
        self.intermediate_real_time_compass_correction = None
        self.now_heading = None
        self.boundary_condition = None
        self.delta_heading = None
        self.adjustment_factor = None
        self.number_of_right_adjustments = None
        self.very_first_calculated_target_heading = None
        self.real_time_compass_correction = None
        self.total_adjustment_time = None
        self.number_of_left_adjustments = None
        self.total_adjustment_factor = None
        self.total_number_of_adjustments = None
        self.run_motors_flag = None
        self.actual_cruisetime = None
        self.sensor_compass = None
        self.watchdog = None
        self.log_filename_snippet = None
        self.dig2_control = None
        self.dig1_control = None
        self.rockme_spin_flag = None
        self.time_stamp = None
        self.collision_with_object_knocked_off_course = None
        self.last_target_distance = None
        self.gps_broadcast_modified_cruisetime = None
        self.gps_broadcast_age = None
        self.now_time = None
        self.ran_past_coordinate_y = None
        self.detect45_delta_heading = None
        self.z = None
        self.y = None
        self.x = None
        self.topspeed = None
        self.detect45_now_heading = None
        self.no_spin_allowed = None
        self.last_time_stamp = None
        self.last_coordinate_x = None
        self.last_coordinate_y = None
        self.final_approach_leg_stop_flag = None
        self.current_mph_speed = None
        self.current_mps_speed = None
        self.time_to_target = None
        self.target_heading_corrected = None
        self.target_heading = None
        self.first_motion_flag = None
        self.rock_count = None
        self.next_coordinate_y = None
        self.next_coordinate_x = None
        self.next_waypoint = None
        self.next_waypoint_sequence_number = None
        self.closest_coordinate_y = None
        self.closest_coordinate_x = None
        self.increment_sequence_number_to_follow_path = None
        self.closest_waypoint = None
        self.closest_distance = None
        self.found_end_waypoint_in_map_file = None
        self.correction_file_name = None
        self.closest_waypoint_sequence_number = None
        self.end_waypoint_sequence_number = None
        self.target_distance = None
        self.how_close = None
        self.now_time_stamp = None
        self.ran_past_coordinate_x = None
        self.now_coordinate_y = None
        # self.one_second_countdown_watchdog_started = None
        self.check_validity_of_gps_broadcast = None
        print("Running Cytronclass __init__")
        # global p1
        # global p2
        GPIO.setmode(GPIO.BCM)  # GPIO numbering
        GPIO.setwarnings(False)  # enable warning from GPIO
        self.AN2 = 13  # set pwm2 pin on MD10-Hat
        self.AN1 = 12  # set pwm1 pin on MD10-hat
        self.DIG2 = 24  # set dir2 pin on MD10-Hat
        self.DIG1 = 26  # set dir1 pin on MD10-Hat
        GPIO.setup(self.AN2, GPIO.OUT)  # set pin as output
        GPIO.setup(self.AN1, GPIO.OUT)  # set pin as output
        GPIO.setup(self.DIG2, GPIO.OUT)  # set pin as output
        GPIO.setup(self.DIG1, GPIO.OUT)  # set pin as output
        self.p1 = GPIO.PWM(self.AN1, 100)  # set pwm for M1
        self.p2 = GPIO.PWM(self.AN2, 100)  # set pwm for M2
        # Initialization for map_traverse
        self.now_coordinate_x = None
        self.read_file_handle = None
        self.next_sequence_number = None
        self.read_iteration_variable = None
        self.temp_list = None
        self.gps_correction_list = None
        self.sensor_gps = None
        self.temp_file_handle = None
        self.map_file_row_count = None
        self.count = None
        self.map_list = None
        self.map_matrix = None
        self.map_matrix_index_first = None
        self.map_file_handle = None
        self.map_file_iteration_variable = None

    def move(self, move_direction, topspeed, cruisetime, ramp_step_time, turn_differential, turnto_angle):
        print(move_direction, topspeed, cruisetime, ramp_step_time, turn_differential, turnto_angle)
        self.turn_command = 0
        self.spin_command = 0
        self.turn_right = 0
        self.turnto_command = 0
        self.compass_turn_command = 0  # 8.5.22 changed from uturn_command to this new variable including turnto
        self.compass_turn_ramp_down = 0  # 7.29.22 add
        self.crossed_0_360_boundary = 0 # 5.3.23 debugging infinite spinning problem
        self.special_condition_count = 0 # 5.4.23 debugging infinite spinning problem

        # 8.3.22 Limit compass __init__ just to commands requiring compass due to initialization delay
        if "uturn" in move_direction.lower() or "turnto" in move_direction.lower():
            print("DEBUG: Entered compass __init_ If statement, move_direction.lower():", move_direction.lower())
            self.sensor_compass = GY271.compass()  # 7.29.22 runs compass __init__

        if "turnto" in move_direction.lower() and turn_differential == 0:
            self.spin_command = 1  # 11.16.22 A spin command was identified by "turnto" and turn_differential=0
            print("Spin detected...move_direction.lower:", move_direction.lower(), "turn_differential:",
                  turn_differential, "Spin_command:", self.spin_command)

        if move_direction.lower() == "forward" or move_direction.lower() == "turnrightforward" or move_direction.lower() == "turnleftforward" or "uturn" in move_direction.lower() or "turnto" in move_direction.lower():
            self.dig1_control = GPIO.LOW
            self.dig2_control = GPIO.LOW
            if "turn" in move_direction.lower():
                self.turn_command = 1
            # the following If handles initating the first compass read and start/end heading
            if "uturn" in move_direction.lower() or "turnto" in move_direction.lower():  # added 7.29.22 modified 8.5.22 to add turnto_angle
                self.compass_turn_command = 1
                # 12.5.22 self.drdy_polling_error_flag check added
                self.start_heading, self.x, self.y, self.drdy_polling_error_flag = self.sensor_compass.get_bearing()  # intial compass read for start of uturn
                print("DEBUG: Just read Compass for start_heading:", self.start_heading, "~line 244") # 5.4.23 
                # self.x and self.y are data returned from compass get_bearing() and not needed
                if self.drdy_polling_error_flag == 1:
                    print("Compass reported a drdy polling error count over 50!!")
                    print("Calling recursiveStopMotors() and quit()")
                    self.recursiveStopMotors()
                    quit()

                # the following If sets the end_heading based on the type of command and then does a correction
                if "uturn" in move_direction.lower():
                    self.end_heading = self.start_heading - 180  # end_heading for uturn
                else:  # therefore turnto command
                    self.end_heading = turnto_angle  # end_heading for turnto
                if self.end_heading < 0:  # correct for 0/360 boundary case
                    self.end_heading = self.end_heading + 360

            if "right" in move_direction.lower():
                self.turn_right = 1  # turn_right=0 for a left turn

            #  Need to use the turnto algo to determine if a left or right turn is needed and set the turn_right flag accordingly.
            # Start algo for turnto direction decision
            if "turnto" in move_direction.lower():
                self.turnto_command = 1
                # calculate the angle 180 degrees opposite start_heading
                self.opposite_start_heading = self.start_heading + 180
                if self.opposite_start_heading > 360:
                    self.opposite_start_heading = self.opposite_start_heading - 360
                # check for special case of turn being exactly 180 degrees
                if self.end_heading == self.opposite_start_heading:
                    self.turn_right = 1  # force a right turn if turn exactly 180 degrees
                else:
                    # right mirror (0 to 179)
                    if self.start_heading >= 0 and self.start_heading < 180:  # right mirror
                        if self.end_heading < self.start_heading or self.end_heading > self.opposite_start_heading:
                            self.turn_right = 0
                        else:
                            self.turn_right = 1  # case end>start AND end<opposite, right turn

                    # left mirror (180 to 360)
                    if self.start_heading >= 180 and self.start_heading < 360:  # left mirror
                        if self.end_heading < self.start_heading and self.end_heading > self.opposite_start_heading:
                            self.turn_right = 0
                        else:
                            self.turn_right = 1  # case end>start or end<opposite, right turn
            # End algo for turnto direction decision

        else:
            if move_direction.lower() == "backward" or move_direction.lower() == "turnrightbackward" or move_direction.lower() == "turnleftbackward":
                self.dig1_control = GPIO.HIGH
                self.dig2_control = GPIO.HIGH
                if "turn" in move_direction.lower():
                    self.turn_command = 1
                if "right" in move_direction.lower():
                    self.turn_right = 1  # turn_right=0 for a left turn

            else:  # 11.16.22 tab adjusted after commentingout above code, this is a catch-all for bad commands
                print("Cytronclass.move() error, improper command:", move_direction)
                print("Cytronclass.move() recursive stop motors and quit()")
                self.recursiveStopMotors()
                quit()

        # 11.29.22 This is a final check for a spin command which changes the treads to turn opposite instead of together
        # line 61 should set spin_command to 1
        if self.spin_command == 1 and self.turn_right == 1:  # for Spin command, have to modify rampup to be a spin instead of gradual forward ramp
            self.dig1_control = GPIO.HIGH  # set Right tread to turn backwards to turn right
        if self.spin_command == 1 and self.turn_right == 0:
            self.dig2_control = GPIO.HIGH  # set Left tread to turn backwards to turn left
        print("Prior to ramp_up>>spin_command:", self.spin_command, "turn_right:", self.turn_right)
        print("dig1_control:", self.dig1_control, "dig2_control:", self.dig2_control)
        print("If dig1_control is HIGH, robot should turn RIGHT")
        print("If dig2_control is HIGH, robot should turn LEFT")

        # begin motion
        try:
            print(move_direction, " speed: ", topspeed, "Cruise Time: ", cruisetime, "Angle:", turnto_angle)
            GPIO.output(self.DIG1, self.dig1_control)  # set DIG1 according to input variable move_direction
            GPIO.output(self.DIG2, self.dig2_control)  # set DIG2 according to input variable move_direction

            # start ramp up
            if self.spin_command == 0:
                self.ramp_up(topspeed, ramp_step_time)
            # end ramp up

            # start main cruise at top speed
            if self.turn_command == 0:
                self.p1.start(topspeed)  # set speed for M1 to topspeed
                self.p2.start(topspeed)  # set speed for M2 to topspeed
                sleep(cruisetime)  # delay amount of cruisetime seconds
            else:  # turn command detected, now determine direction & if uturn or turn_to command
                if self.turnto_command == 1 and self.turn_right == 0:  # left turnto
                    self.delta_turn_angle = self.start_heading - self.end_heading
                    # correct for 0/360 boundary crossing
                    if self.delta_turn_angle < 0:
                        self.delta_turn_angle = self.delta_turn_angle + 360
                if self.turnto_command == 1 and self.turn_right == 1:  # right turnto
                    self.delta_turn_angle = self.end_heading - self.start_heading
                    # correct for 0/360 boundary crossing
                    if self.delta_turn_angle < 0:
                        self.delta_turn_angle = self.delta_turn_angle + 360

                if self.turn_right == 1:  # right turn
                    print("DEBUG: Right Turn Loop started")
                    if self.spin_command == 1:
                        print("DEBUG: spin_command=1")
                        print("dig2_control:", self.dig2_control)
                        print("prior to change dig1_control:", self.dig1_control)
                        self.dig1_control = GPIO.HIGH  # 11.16.22 switch right side to run backwards, opposite left side
                        print("post change dig1_control:", self.dig1_control)
                        self.p1.start(topspeed)  # 11.16.22 run at full speed
                        print("Debug: Spin detected, eliminated turn_differential in right turn 100% start")
                        # send direction change command:
                        GPIO.output(self.DIG1, self.dig1_control)
                    else:
                        self.p1.start(topspeed * turn_differential)  # set speed for M1 to topspeed
                    self.p2.start(topspeed)  # reduce speed for M1 to make right turn
                    print("Right Turn speed 100%")
                    # start right turn handling
                    if self.compass_turn_command == 1:
                        print("Compass Turn Command:", self.compass_turn_command)
                        if self.turnto_command == 0:
                            print("Turnto Command:", self.turnto_command)
                            self.heading_75 = self.start_heading + 135  # 75% of 180 degrees
                            if self.heading_75 > 360:  # correct for 0/360 boundary case
                                self.heading_75 = self.heading_75 - 360
                            self.heading_90 = self.start_heading + 162  # 90% of 180 degrees
                            if self.heading_90 > 360:  # correct for 0/360 boundary case
                                self.heading_90 = self.heading_90 - 360
                        else:  # turnto_command=1, create 75 and 90 based on delta_turn_angle
                            # calculate amount of degrees from total in 75% and 90% turn
                            self.angle_add_75 = .75 * self.delta_turn_angle
                            self.angle_add_90 = .9 * self.delta_turn_angle

                            # 11.30.22 to slow down spin, change 75% to 50% of angle and 90% to 75%
                            if self.spin_command == 1:
                                self.angle_add_75 = .5 * self.delta_turn_angle
                                self.angle_add_90 = .75 * self.delta_turn_angle
                            # 11.30.22 end change

                            # since this is the "turn_right" branch, just add angles and correct
                            self.heading_75 = self.start_heading + self.angle_add_75
                            if self.heading_75 > 360:  # correct for 0/360 boundary crossing
                                self.heading_75 = self.heading_75 - 360
                            self.heading_90 = self.start_heading + self.angle_add_90
                            if self.heading_90 > 360:  # correct for 0/360 boundary crossing
                                self.heading_90 = self.heading_90 - 360
                            print("Turn Right")
                            print("Start_heading:", self.start_heading)
                            print("End Heading:", self.end_heading)
                            print("Delta turn angle:", self.delta_turn_angle)
                            print("Heading 75:", self.heading_75)
                            print("Heading 90:", self.heading_90)

                        # print("Entered Right UTurn handling")
                        # print("Start heading:",self.start_heading)
                        # print("75% heading:",self.heading_75)
                        # print("90% heading:",self.heading_90)
                        # print("End Heading:",self.end_heading )

                        # 8.1.22 previous_heading and crossed_key_boundary meant to fix 0/360 bug
                        self.previous_heading = self.start_heading  # initiate this variable as part of 0/360 boundary handling
                        self.crossed_key_boundary = 0  # initiate this variable, detect 0/360 boundary crossing, start 0 which means no crossing yet
                        self.compass_bounce_detected = 0  # 8.15.22  required to detect compass bouncing around 0/360 boundary
                        self.stop_spin_overshoot_correction = 0
                        # RIGHT TURN While Loop
                        while True:  # start right turn While Loop

                            if self.start_heading == self.end_heading:  # detect if robot is already pointing in the desired direction
                                print("Robot already pointed ", self.end_heading, "breaking turn loop.")
                                self.stop_spin_overshoot_correction = 1
                                break  # no need for a spin so break spin loop, otherwise it will do a 360 spin
                            self.compass_bounce_detected = 0  # 8.15.22 have to clear this flag after every iteration
                            self.crossed_0_360_boundary = 0 # 5.8.23 reset flag after each iteration
                            self.crossed_end_boundary = 0 # 5.9.23 reset flag after each iteration

                            # 12.5.22 self.drdy_polling_error_flag check added
                            self.now_heading, self.x, self.y, self.drdy_polling_error_flag = self.sensor_compass.get_bearing()  # intial compass read for start of uturn
                            # self.x and self.y are data returned from compass get_bearing() and not needed
                            if self.drdy_polling_error_flag == 1:
                                print("Compass reported a drdy polling error count over 50!!")
                                print("Calling recursiveStopMotors() and quit()")
                                self.recursiveStopMotors()
                                quit()

                            print("DEBUG: Now Heading:", self.now_heading)
                            print("DEBUG: Previous Heading:", self.previous_heading)

                            # 8.15.22 compass bounce detection around 0/360 boundary crossing:
                            # if the first boundary condition '0/360 crossing' has previously occured,
                            # this code detects a bounce if the compass reading bounces back to the other side of the boundary.
                            if self.crossed_key_boundary == 1 and abs(self.now_heading - self.previous_heading) > 180:
                                # compass bounce has occured
                                # back to measurements prior to a crossing BUT the crossed_key_boundary flag was previously set.
                                # so we must continue to adjust now_heading
                                # This flag will force an adjustment and also clear the crossed_key_boundary flag.
                                self.compass_bounce_detected = 1
                                print("Compass BOUNCE detected!!")

                            # first boundary condition: 0/360 crossing
                            if abs(self.now_heading - self.previous_heading) > 180:
                                # 8.2.22 this detects crossing the 0/360 boundary,
                                # a change >180 won't happen in a half second of a normal robot turn
                                # so it has to be crossing the 0/360 boundary
                                self.crossed_0_360_boundary = 1 # 5.3.23 debugging infinite spinning problem
                                self.crossed_key_boundary = 1
                                print("0/360 Crossing Detected! Key Boundary Flag set to 1")
                                print("0/360 Crossing Detected! 0/360 Boundary Flag set to 1")

                            # second boundary condition: end_heading Crossing
                            # 05.08.23 New Code
                            print("Entering new 5.8.23 end_heading crossing code")
                            print("Debug1 crossed_end_boundary flag:", self.crossed_end_boundary)
                            if self.crossed_0_360_boundary == 0:  # normal operation in rest of compass range
                                print("No 0/360 crossing detected...prev-end-now:", self.previous_heading, self.end_heading, self.now_heading)
                                if self.previous_heading < self.end_heading and (self.now_heading == self.end_heading or self.now_heading > self.end_heading):
                                    # this if is looking to see if the previous heading was before the end_heading and the new heading is = or after the end_heading
                                    print("No 0/360 crossing detected but end_crossing detected!")
                                    self.crossed_end_boundary = 1
                                    print("Debug2 crossed_end_boundary flag:", self.crossed_end_boundary)
                            else:  # special condition to detect 0/360 crossing and end crossing in same loop
                                print("Debug3 crossed_end_boundary flag:", self.crossed_end_boundary)
                                print("0/360 crossing detected...prev-end-now:", self.previous_heading,
                                      self.end_heading, self.now_heading)
                                if self.end_heading > 180:  # end_heading is before 0/360
                                    print("End_heading is before 0/360")
                                    self.temp_now_heading = self.now_heading + 360  # special conversion for crossing
                                    print("temp_now_heading:", self.temp_now_heading)
                                    if self.temp_now_heading > self.end_heading:
                                        print("0/360 crossing detected and end_crossing detected!")
                                        self.crossed_end_boundary = 1
                                        print("Debug4 crossed_end_boundary flag:", self.crossed_end_boundary)
                                if self.end_heading < 180:  # end is after 0/360 boundary
                                    print("End_heading is after 0/360")
                                    if self.now_heading > self.end_heading:
                                        self.crossed_end_boundary = 1
                                        print("0/360 crossing detected and end_crossing detected!")
                                        print("Debug4.5 crossed_end_boundary flag:", self.crossed_end_boundary)
                            # end: second boundary condition

                            print("DEBUG: now_heading", self.now_heading, "end_heading", self.end_heading)
                            print("DEBUG: if now_heading = or > end_heading motors should stop!")
                            # 5.3.23 Added following print
                            print("Special Condition flags:", self.crossed_0_360_boundary, self.crossed_end_boundary)
                            # 5.3.23 (self.crossed_0_360_boundary and self.crossed_end_boundary) added to the following IF to cover crossing 0/360 & end_heading in same loop
                            print("Debug5 crossed_end_boundary flag:", self.crossed_end_boundary)
                            if self.crossed_end_boundary == 1:
                                print("DEBUG: Motors Stopped!!")
                                self.p1.start(0)  # stop motors
                                self.p2.start(0)  # stop motors
                                self.compass_turn_ramp_down = 1
                                print("Turn complete, Break loop")
                                break  # End right turn While Loop
                            else:
                                if self.now_heading > self.heading_90:
                                    if self.spin_command == 1:  # if Spin @ 90% turn, reduce speed to 80%, eliminate turn_differential
                                        self.p2.start(.80 * topspeed)
                                        self.dig1_control = GPIO.HIGH  # 11.16.22 switch right side to run backwards, opposite right side
                                        self.p1.start(
                                            .80 * topspeed)  # 11.30.22 run at 80% to maximize speed to end_heading
                                        print("Debug: Spin detected, @ 90% turn, reduce speed to 80%")
                                    else:
                                        self.p2.start(.50 * topspeed)  # cut M1 speed to 1/2
                                        self.p1.start(
                                            .50 * topspeed * turn_differential)  # reduce speed for M2 to make left turn
                                        print("Turn speed 50%")
                                # commented out 11.29.22            sleep(.25)
                                else:
                                    if self.now_heading > self.heading_75:
                                        if self.spin_command == 1:
                                            self.p2.start(topspeed)  # 12.2.22 @75% of spin, leave speed at 100%
                                            self.dig1_control = GPIO.HIGH  # 11.16.22 switch right side to run backwards, opposite right side
                                            self.p1.start(topspeed)  # 12.2.22 @75% of spin, leave speed at 100%
                                            print("Debug: Spin detected, @ 75% turn, leave speed at 100%")
                                        else:
                                            self.p2.start(.75 * topspeed)  # cut M1 speed to 3/4
                                            self.p1.start(
                                                .75 * topspeed * turn_differential)  # reduce speed for M2 to make right turn
                                            print("Turn speed 75%")
                            self.previous_heading = self.now_heading # 5.15.23 This some how got dropped, adding back.....

                        # Start right spin correction sequence after spin command AND if now_heading does not already equal end_heading
                        if self.spin_command == 1 and self.stop_spin_overshoot_correction == 0:  # this is a spin command AND overshoot correction is needed
                            print("Start right spin overshoot correction sequence...")

                            # determine overshoot
                            self.overshoot_angle = self.now_heading - self.end_heading
                            if self.overshoot_angle < 0:  # detect 0/360 boundary Crossing
                                self.overshoot_angle = self.overshoot_angle + 360
                            print("Overshoot angle:", self.overshoot_angle)

                            # reverse tread direction to retrace overshoot angles
                            print("Reverse treads for left turning...")
                            self.dig1_control = GPIO.LOW
                            self.dig2_control = GPIO.HIGH
                            GPIO.output(self.DIG1,
                                        self.dig1_control)  # set DIG1 according to input variable move_direction
                            GPIO.output(self.DIG2,
                                        self.dig2_control)  # set DIG2 according to input variable move_direction

                            # loop to retrace overshoot angle
                            print("Start Overshoot retrace loop")
                            self.correction_steps_count = 0
                            self.overshoot_angle = 1  # have to initiate this variable to non-zero to initiate the following while loop

                            # 12.2.22 Likely can just use while True: since there is a break at the end of this loop that breaks the loop under similar conditions
                            print("Now Heading at beginning of Overshoot correction:", self.now_heading)
                            while self.overshoot_angle > 0:
                                # take one small incremental step
                                print("Take one small incremental step.")
                                self.p1.start(50)
                                self.p2.start(50)
                                sleep(.05)  # .0156 approx 1 degree at speed 50 ...
                                self.p1.start(0)
                                self.p2.start(0)

                                # measure new now_heading
                                print("Take new compass heading reading...")
                                # 12.5.22 self.drdy_polling_error_flag check added
                                self.now_heading, self.x, self.y, self.drdy_polling_error_flag = self.sensor_compass.get_bearing()  # intial compass read for start of uturn
                                # self.x and self.y are data returned from compass get_bearing() and not needed
                                print("Now Heading after one more correction step:", self.now_heading)
                                if self.drdy_polling_error_flag == 1:
                                    print("Compass reported a drdy polling error count over 50!!")
                                    print("Calling recursiveStopMotors() and quit()")
                                    self.recursiveStopMotors()
                                    quit()

                                # 5.4.23 new determine new overshoot angle
                                if self.now_heading < 180 and self.end_heading > 180:
                                    self.overshoot_angle = self.now_heading + 360 - self.end_heading
                                else:
                                    self.overshoot_angle = self.now_heading - self.end_heading
                                # this code assumes that the overshoot angle is significantly less than 180 at all times
                                # the if statement is for a calculation that crosses the 0/360 boundary
                                # the else statement is for a calculation either to one side or the other of the boundary

                                self.correction_steps_count = self.correction_steps_count + 1
                                print("Correction Steps Count:", self.correction_steps_count)
                                print("New Overshoot angle:", self.overshoot_angle)

                                # 5.14.23 This if is being added to abend code if a infinite spin is occurring
                                if self.correction_steps_count > 20:
                                    print("ERROR ERROR ERROR!!")
                                    print("Possible infinite RIGHT Spin Occurring with more than 20 correction steps")
                                    print("Quitting to capture error condition")
                                    quit()

                                if self.overshoot_angle <= 0:
                                    print("Finished correction Steps")
                                    print("Arrived at final angle:", self.now_heading)
                                    # print("Calling Recursive Stop Command")
                                    # self.recursiveStopMotors()
                                    print("Now Breaking out of Correction Loop")
                                    break  # met correction goal, breaking out of correction loop.
                    # end right turn handling

                    else:  # right turn but not a turn command so sleep for entire cruisetime
                        sleep(cruisetime)
                else:  # left turn
                    self.p1.start(topspeed)  # set speed for M1 to topspeed
                    print("DEBUG: Left Turn Loop started")
                    if self.spin_command == 1:
                        print("DEBUG: spin_command=1")
                        print("dig1_control:", self.dig1_control)
                        print("prior to change dig2_control:", self.dig2_control)
                        self.dig2_control = GPIO.HIGH  # 11.16.22 switch left side to run backwards, opposite right side
                        print("post change dig2_control:", self.dig2_control)
                        self.p2.start(topspeed)  # 11.16.22 run at full speed
                        print("Debug: Spin detected, eliminated turn_differential in left turn 100% start")
                        # send direction change command:
                        GPIO.output(self.DIG2, self.dig2_control)
                    else:
                        self.p2.start(topspeed * turn_differential)  # reduce speed for M2 to make left turn
                    print("Left Turn speed 100%")
                    # start left turn handling
                    if self.compass_turn_command == 1:
                        print("Compass Turn Command:", self.compass_turn_command)
                        if self.turnto_command == 0:
                            print("Turnto Command:", self.turnto_command)
                            self.heading_75 = self.start_heading - 135  # 75% of 180 degrees
                            if self.heading_75 < 0:  # correct for 0/360 boundary case
                                self.heading_75 = self.heading_75 + 360
                            self.heading_90 = self.start_heading - 162  # 90% of 180 degrees
                            if self.heading_90 < 0:  # correct for 0/360 boundary case
                                self.heading_90 = self.heading_90 + 360
                        else:  # turnto_command=1, create 75 and 90 based on delta_turn_angle
                            # calculate amount of degrees from total in 75% and 90% turn
                            self.angle_add_75 = .75 * self.delta_turn_angle
                            self.angle_add_90 = .9 * self.delta_turn_angle

                            # 11.30.22 to slow down spin, change 75% to 50% of angle and 90% to 75%
                            if self.spin_command == 1:
                                self.angle_add_75 = .5 * self.delta_turn_angle
                                self.angle_add_90 = .75 * self.delta_turn_angle
                            # 11.30.22 end change

                            # since this is the "turn_left" branch, just subtract angles and correct
                            self.heading_75 = self.start_heading - self.angle_add_75
                            if self.heading_75 < 0:  # correct for 0/360 boundary crossing
                                self.heading_75 = self.heading_75 + 360
                            self.heading_90 = self.start_heading - self.angle_add_90
                            if self.heading_90 < 0:  # correct for 0/360 boundary crossing
                                self.heading_90 = self.heading_90 + 360
                            print("Turn Left")
                            print("Start_heading:", self.start_heading)
                            print("End Heading:", self.end_heading)
                            print("Delta turn angle:", self.delta_turn_angle)
                            print("Heading 75:", self.heading_75)
                            print("Heading 90:", self.heading_90)

                        # print("Entered Left UTurn handling")
                        # print("Start heading:",self.start_heading)
                        # print("75% heading:",self.heading_75)
                        # print("90% heading:",self.heading_90)
                        # print("End Heading:",self.end_heading )

                        # 8.4.22 previous_heading and crossed_key_boundary meant to fix 0/360 bug
                        self.previous_heading = self.start_heading  # initiate this variable as part of 0/360 boundary handling
                        self.crossed_key_boundary = 0  # initiate this variable, detect 0/360 boundary crossing, start 0 which means no crossing yet
                        self.stop_spin_overshoot_correction = 0  # this is a flag to stop spin correction if start and end headings are the same
                        # LEFT TURN While Loop
                        while True:  # start left turn While Loop
                            # detect if robot is already pointing in the desired direction
                            if self.start_heading == self.end_heading:
                                print("Robot already pointed ", self.end_heading, "breaking turn loop.")
                                self.stop_spin_overshoot_correction = 1  # this is a flag to stop spin correction if start and end headings are the same
                                break  # no need for a spin so break spin loop, otherwise it will do a 360 spin

                            # 12.5.22 self.drdy_polling_error_flag check added
                            self.now_heading, self.x, self.y, self.drdy_polling_error_flag = self.sensor_compass.get_bearing()  # intial compass read for start of uturn
                            # self.x and self.y are data returned from compass get_bearing() and not needed
                            if self.drdy_polling_error_flag == 1:
                                print("Compass reported a drdy polling error count over 50!!")
                                print("Calling recursiveStopMotors() and quit()")
                                self.recursiveStopMotors()
                                quit()

                            self.compass_bounce_detected = 0  # 8.15.22 have to clear this flag after every iteration
                            self.crossed_0_360_boundary = 0 # 5.8.23 reset flag after each iteration
                            self.crossed_end_boundary = 0 # 5.9.23 reset flag after each iteration

                            print("DEBUG: Now Heading:", self.now_heading)
                            print("DEBUG: Previous Heading:", self.previous_heading)

                            # 8.15.22 compass bounce detection around 0/360 boundary crossing:
                            # if the first boundary condition '0/360 crossing' has previously occured,
                            # this code detects a bounce if the compass reading bounces back to the other side of the boundary.
                            if self.crossed_key_boundary == 1 and abs(self.now_heading - self.previous_heading) > 180:
                                # compass bounce has occured
                                # back to measurements prior to a crossing BUT the crossed_key_boundary flag was previously set.
                                # so we must continue to adjust now_heading
                                # This flag will force an adjustment and also clear the crossed_key_boundary flag.
                                self.compass_bounce_detected = 1
                                print("Compass BOUNCE detected!!")

                            # first boundary condition: 0/360 crossing
                            if abs(self.now_heading - self.previous_heading) > 180:
                                # 8.2.22 this detects crossing the 0/360 boundary,
                                # a change >180 won't happen in a half second of a normal robot turn
                                # so it has to be crossing the 0/360 boundary
                                self.crossed_0_360_boundary = 1 # 5.3.23 debugging infinite spinning problem
                                self.crossed_key_boundary = 1
                                print("0/360 Crossing Detected! Key Boundary Flag set to 1")
                                print("0/360 Crossing Detected! 0/360 Boundary Flag set to 1")

                            # second boundary condition: end_heading Crossing
                            # 05.08.23 New Code

                            print("Entering new 5.8.23 end_heading crossing code")
                            print("Debug1L crossed_end_boundary flag:", self.crossed_end_boundary)
                            if self.crossed_0_360_boundary == 0: # normal operation in rest of compass range
                                print("No 0/360 crossing detected...prev-end-now:", self.previous_heading, self.end_heading, self.now_heading)
                                print("Debug1.5L crossed_end_boundary flag:", self.crossed_end_boundary)
                                if self.previous_heading > self.end_heading and (self.now_heading == self.end_heading or self.now_heading < self.end_heading):
                                    # this if is looking to see if the previous heading was before the end_heading and the new heading is = or after the end_heading
                                    print("No 0/360 crossing detected but end_crossing detected!")
                                    self.crossed_end_boundary = 1
                                    print("Debug2L crossed_end_boundary flag:", self.crossed_end_boundary)
                            else: # special condition to detect 0/360 crossing and end crossing in same loop
                                print("0/360 crossing detected...prev-end-now:", self.previous_heading, self.end_heading, self.now_heading)
                                if self.end_heading <180: # end_heading is before 0/360
                                    print("End_heading is before 0/360")
                                    self.temp_now_heading = self.now_heading - 360 # special conversion for crossing
                                    print("temp_now_heading:", self.temp_now_heading)
                                    if self.temp_now_heading < self.end_heading:
                                        print("0/360 crossing detected and end_crossing detected!")
                                        self.crossed_end_boundary = 1
                                        print("Debug3L crossed_end_boundary flag:", self.crossed_end_boundary)
                                if self.end_heading >180: # end is after 0/360 boundary
                                    print("End_heading is after 0/360")
                                    if self.now_heading < self.end_heading:
                                        self.crossed_end_boundary = 1
                                        print("0/360 crossing detected and end_crossing detected!")
                                        print("Debug4L crossed_end_boundary flag:", self.crossed_end_boundary)
                            # end: second boundary condition

                            print("DEBUG: now_heading", self.now_heading, "end_heading", self.end_heading)
                            print("DEBUG: if now_heading = or > end_heading motors should stop!")
                            # 5.3.23 Added following print
                            print("Special Condition flags:", self.crossed_0_360_boundary, self.crossed_end_boundary)
                            # 5.3.23 (self.crossed_0_360_boundary and self.crossed_end_boundary) added to the following IF to cover crossing 0/360 & end_heading in same loop
                            print("Debug5L crossed_end_boundary flag:", self.crossed_end_boundary)
                            if self.crossed_end_boundary == 1:
                                print("DEBUG: Motors Stopped!!")
                                self.p1.start(0)  # stop motors
                                self.p2.start(0)  # stop motors
                                self.compass_turn_ramp_down = 1
                                print("Turn complete, Break loop")
                                break  # End left turn While Loop
                            else:
                                if self.now_heading < self.heading_90:
                                    if self.spin_command == 1:  # if Spin @ 90% turn, reduce speed to 80%, eliminate turn_differential
                                        self.p1.start(.80 * topspeed)
                                        self.dig2_control = GPIO.HIGH  # 11.16.22 switch left side to run backwards, opposite right side
                                        self.p2.start(
                                            .80 * topspeed)  # 11.30.22 run at 80% to maximize speed to end_heading
                                        print("Debug: Spin detected, @ 90% turn, reduce speed to 80%")
                                    else:
                                        self.p1.start(.50 * topspeed)  # cut M1 speed to 1/2
                                        self.p2.start(
                                            .50 * topspeed * turn_differential)  # reduce speed for M2 to make left turn
                                        print("Turn speed 50%")
                                # commented out 11.29.22            sleep(.25)
                                else:
                                    if self.now_heading < self.heading_75:
                                        if self.spin_command == 1:
                                            self.p2.start(topspeed)  # 12.2.22 @75% of spin, leave speed at 100%
                                            self.dig2_control = GPIO.HIGH  # 11.16.22 switch left side to run backwards, opposite right side
                                            self.p2.start(topspeed)  # 12.2.22 @75% of spin, leave speed at 100%
                                            print("Debug: Spin detected, @ 75% turn, leave speed at 100%")
                                        else:
                                            self.p1.start(.75 * topspeed)  # cut M1 speed to 3/4
                                            self.p2.start(
                                                .75 * topspeed * turn_differential)  # reduce speed for M2 to make left turn
                                            print("Turn speed 75%")
                            self.previous_heading = self.now_heading # 5.15.23 This some how got dropped, adding back.....
                        # end left turn handling

                        # Start left spin correction sequence after spin command AND if now_heading does not already equal end_heading
                        if self.spin_command == 1 and self.stop_spin_overshoot_correction == 0:  # this is a spin command AND overshoot correction is needed
                            print("Start left spin overshoot correction sequence...")

                            # determine overshoot
                            self.overshoot_angle = self.end_heading - self.now_heading
                            if self.overshoot_angle < 0:  # detect 0/360 boundary Crossing
                                self.overshoot_angle = self.overshoot_angle + 360
                            print("Overshoot angle:", self.overshoot_angle)

                            # reverse tread direction to retrace overshoot angles
                            print("Reverse treads for right turning...")
                            self.dig1_control = GPIO.HIGH
                            self.dig2_control = GPIO.LOW
                            GPIO.output(self.DIG1,
                                        self.dig1_control)  # set DIG1 according to input variable move_direction
                            GPIO.output(self.DIG2,
                                        self.dig2_control)  # set DIG2 according to input variable move_direction

                            # loop to retrace overshoot angle
                            print("Start Overshoot retrace loop")
                            self.correction_steps_count = 0
                            self.overshoot_angle = 1  # have to initiate this variable to non-zero to initiate the following while loop

                            # 12.2.22 Likely can just use while True: since there is a break at the end of this loop that breaks the loop under similar conditions
                            print("Now Heading at beginning of Overshoot correction:", self.now_heading)
                            while self.overshoot_angle > 0:
                                # take one small incremental step
                                print("Take one small incremental step.")
                                self.p1.start(50)
                                self.p2.start(50)
                                sleep(.05)  # .0156 approx 1 degree at speed 50 ... set to .03 during debug
                                self.p1.start(0)
                                self.p2.start(0)

                                # measure new now_heading
                                print("Take new compass heading reading...")
                                # 12.5.22 self.drdy_polling_error_flag check added
                                self.now_heading, self.x, self.y, self.drdy_polling_error_flag = self.sensor_compass.get_bearing()  # intial compass read for start of uturn
                                # self.x and self.y are data returned from compass get_bearing() and not needed
                                print("Now Heading after one more correction step:", self.now_heading)
                                if self.drdy_polling_error_flag == 1:
                                    print("Compass reported a drdy polling error count over 50!!")
                                    print("Calling recursiveStopMotors() and quit()")
                                    self.recursiveStopMotors()
                                    quit()

                                # 5.4.23 new determine new overshoot angle
                                if self.now_heading < 180 and self.end_heading > 180:
                                    self.overshoot_angle = self.now_heading + 360 - self.end_heading
                                else:
                                    self.overshoot_angle = self.now_heading - self.end_heading
                                # this code assumes that the overshoot angle is significantly less than 180 at all times
                                # the if statement is for a calculation that crosses the 0/360 boundary
                                # the else statement is for a calculation either to one side or the other of the boundary

                                self.correction_steps_count = self.correction_steps_count + 1
                                print("Correction Steps Count:", self.correction_steps_count)
                                print("New Overshoot angle:", self.overshoot_angle)

                                # 5.14.23 This if is being added to abend code if a infinite spin is occurring
                                if self.correction_steps_count > 20:
                                    print("ERROR ERROR ERROR!!")
                                    print("Possible infinite LEFT Spin Occurring with more than 20 correction steps")
                                    print("Quitting to capture error condition")
                                    quit()

                                if self.overshoot_angle <= 0:
                                    print("Finished correction Steps")
                                    print("Arrived at final angle:", self.now_heading)
                                    # print("Calling Recursive Stop Command")
                                    # self.recursiveStopMotors()
                                    print("Now Breaking out of Correction Loop")
                                    break  # met correction goal, breaking out of correction loop.

                        # end left turn handling

                    else:  # left turn but not a uturn command so sleep for entire cruisetime
                        sleep(cruisetime)

            # start ramp down
            if self.spin_command == 1 and self.turn_right == 1:  # for Spin command, have to modify rampup to be a spin instead of gradual forward ramp
                self.dig1_control = GPIO.HIGH  # set Right tread to turn backwards to turn right
            if self.spin_command == 1 and self.turn_right == 0:
                self.dig2_control = GPIO.HIGH  # set Left tread to turn backwards to turn left
            print("Prior to ramp_down>>spin_command:", self.spin_command, "turn_right:", self.turn_right)

            if self.spin_command == 0:  # 11.30.22 only do ramp-down if non-spin command
                self.ramp_down(topspeed, ramp_step_time, 1)
                print("DEBUG: I just ran the spin_command=0 ramp down...wha?????")
            # end ramp Down

            # Stop Motors
            self.recursiveStopMotors()  # Send rapid 5 stop motor commands

        except OSError:
            print("Compass Error likely detected! While running:")
            print("CytronclassXX.Cytronclass().move()")
            print("Recursive Motor Stop:")
            self.recursiveStopMotors()
            print("about to execute QUIT")
            quit()

        except:  # exit programe when keyboard interupt
            print("Recursive Motor Stop:")
            self.recursiveStopMotors()
            print("CytronclassXX.Cytronclass().move() exception detected")
            print("about to execute QUIT")
            quit()

    def straight_line(self, move_direction, topspeed, cruisetime, target_heading):
        # initialize total_adjustment_time to keep track of the amount of time adjusting steering
        self.total_adjustment_time = 0
        # delay in each step of ramp_up and ramp_down
        self.ramp_step_time = 0.01
        self.gps_operation_prevent_stop_motors_flag = 0

        if (target_heading > 360) or (target_heading < 0):
            print("Error: Heading must be between 0 and 360 degrees!")
            print("cytron.straightlineX.py Terminating")
            quit()

        if topspeed > 100:
            topspeed = 100
        # Max speed is 100

        if cruisetime > 50:
            cruisetime = 1
            print("Cruise Time was >50.  Forced to 1.")

        # print("Direction: ", move_direction, 'Top Speed:', topspeed, 'Cruise Time:', cruisetime, "Heading:", target_heading)

        self.sensor_compass = GY271.compass()

        # initialize counters for debug
        self.number_of_right_adjustments = 0
        self.number_of_left_adjustments = 0
        self.total_adjustment_time = 0
        self.total_adjustment_factor = 0
        self.total_number_of_adjustments = 0

        # initialize flags
        self.run_motors_flag = 1  # this flag needs to be '1' while motors are running
        self.move_forward_flag = 0
        self.move_backward_flag = 0

        # set Cytron Motor Driver to FORWARD
        if move_direction.lower() == "forward":
            self.move_forward_flag = 1
            self.dig1_control = GPIO.LOW
            self.dig2_control = GPIO.LOW
            GPIO.output(self.DIG1, self.dig1_control)  # set DIG1 according to input variable move_direction
            GPIO.output(self.DIG2, self.dig2_control)  # set DIG2 according to input variable move_direction

        # set Cytron Motor Driver to FORWARD but with a gps flag to prevent stopping at end
        # for GPS, the motion cycles through straightline with course correction and then continued motion with no correction
        # during the no correction phase, the GPS is being read for details to fed into next straightline cycle.
        if move_direction.lower() == "forwardgps":
            self.move_forward_flag = 1
            self.gps_operation_prevent_stop_motors_flag = 1
            self.dig1_control = GPIO.LOW
            self.dig2_control = GPIO.LOW
            GPIO.output(self.DIG1, self.dig1_control)  # set DIG1 according to input variable move_direction
            GPIO.output(self.DIG2, self.dig2_control)  # set DIG2 according to input variable move_direction

        # set Cytron Motor Driver to BACKWARD
        if move_direction.lower() == "backward":
            self.move_backward_flag = 1
            self.dig1_control = GPIO.HIGH
            self.dig2_control = GPIO.HIGH
            GPIO.output(self.DIG1, self.dig1_control)  # set DIG1 according to input variable move_direction
            GPIO.output(self.DIG2, self.dig2_control)  # set DIG2 according to input variable move_direction

        # Begin Ramp up unless GPS forward
        if self.gps_operation_prevent_stop_motors_flag == 0:
            self.ramp_up(topspeed, self.ramp_step_time)
        # Robot has ramped up to Top Speed

        try:
            self.start_time = time()  # real time snapshot at beginning of motion loop
            self.stop_time = self.start_time + cruisetime  # calculation of real time stop target

            # the following for loop is meant to keep the now_heading on course for the target_heading throughout the cruisetime
            while self.run_motors_flag == 1:  # CruiseTimeForLoop
                # each loop runs to the completion of a single adjustment, no matter how long it takes
                # looping stops when stop_time equals real

                # call robotcompass which returns current now heading
                # 12.5.22 self.drdy_polling_error_flag check added
                self.watchdog.watchdog_call("compass", "start", .15)
                self.now_heading, self.x, self.y, self.drdy_polling_error_flag = self.sensor_compass.get_bearing()
                # self.x and self.y are data returned from compass get_bearing() and not needed
                self.watchdog.watchdog_call("compass", "stop", .15)
                # start correct for 0/360 boundary:
                if self.now_heading < 0:
                    self.now_heading = self.now_heading + 360
                if self.now_heading > 360:
                    self.now_heading = self.now_heading - 360
                # end correct for 0/360 boundary:

# 4.12.23 commented out to remove real time corrections filtering into SL, will all be calculated in nav_p2p
                # self.now_heading_corrected = self.now_heading + real_time_compass_correction
                # compass get_bearing has built-in compass calibration from the original construction (part of now_heading)
                # add real_time_compass_correction which is the compass error observed in real time from calculations using GPS and navigate_point2point
                # start correct for 0/360 boundary:
                # if self.now_heading_corrected < 0:
                #    self.now_heading_corrected = self.now_heading_corrected + 360
                # if self.now_heading_corrected > 360:
                #    self.now_heading_corrected = self.now_heading_corrected - 360
                # end correct for 0/360 boundary:

                if self.drdy_polling_error_flag == 1:
                    print("Compass reported a drdy polling error count over 50!!")
                    print("Calling recursiveStopMotors() and quit()")
                    self.recursiveStopMotors()
                    quit()
                # xtemp and ytemp are returned for debug purposes only and ignored for code functionality

                # flip compass reading by 180 degrees for backward direction
                if self.move_backward_flag == 1:
                    if self.now_heading < 180:
                        self.now_heading = self.now_heading + 180
                    else:
                        self.now_heading = self.now_heading - 180

                # 0/360 boundary condition calculation of delta_heading=target_heading-now_heading
                self.boundary_condition = 0
                if target_heading > 315 and self.now_heading < 45:
                    self.delta_heading = target_heading - (self.now_heading + 360)
                    self.boundary_condition = 1
                if target_heading < 45 and self.now_heading > 315:
                    self.delta_heading = target_heading + 360 - self.now_heading
                    self.boundary_condition = 1
                if self.boundary_condition == 0:
                    self.delta_heading = target_heading - self.now_heading
                # print("Target Heading: " , target_heading , "Now Heading: " , self.now_heading , "Delta_Heading: " , self.delta_heading)

                # if delta_heading>45 print "Error!  Off course!!" quit()
                if abs(self.delta_heading) > 45:
                    print("Error! Off Course by more than 45 degrees!!")
                    print("Recursive Motor Stop:")
                    self.recursiveStopMotors()
                    # 2.19.23 do not perform the following quit() if this is a GPS operation
                    if self.gps_operation_prevent_stop_motors_flag == 0:
                        print("Error! Quitting cytron.straightlinex.py....")
                        quit()

                # if delta_heading=0 go back to check compass
                # Do this by checking >0 and <0, the case of 0 will end CruiseTimeForloop
                # then go back and start over with a compass check.

                self.adjustment_factor = 1 - abs(self.delta_heading / 40)
                # 4.21.23 changed to 30 from 40  2.12.23 changed to 40 from 90 to experiment with navigate_p2p
                # the adjustment factor controls how long the motors cause a turn to adjust heading
                # *************************
                # Adjustment factor calculation assumes a worse case delta_heading of 45, will force a 50% slow down of one motor for the turn
                # A delta_heading of 1, will only force a 1% slow down
                # *************************
                # the smaller the delta, the smaller amout of time spent in adjustment_factor
                if self.adjustment_factor < 0:
                    self.adjustment_factor = 0  # it's possible that the adjustment factor becomes negative causing a cytron failure....
                # print adjustment factor
                print("STRAIGHT LINE parameters")
                print("Target Heading corrected INPUT:", int(target_heading), "\ntarget_heading_corrected_delta INPUT:")
                print("now_heading", int(self.now_heading))
                print("Delta_Heading:", int(self.delta_heading))
                print("Adjustment Factor:", self.adjustment_factor)
                print("UUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUU")

                # correct by turning right
                if (self.delta_heading > 0 and self.move_forward_flag == 1) or (
                        self.delta_heading < 0 and self.move_backward_flag == 1):  # Turn Right
                    print("TURN RIGHT correction >>>")
                    self.number_of_right_adjustments = self.number_of_right_adjustments + 1
                    # slow right tread
                    self.p1.start(topspeed * self.adjustment_factor)  # cut M2 speed to adjust heading
                    self.p2.start(topspeed)  # M1 remains at full speed
                    # Allow adjustment turn to continue for 1-adjustment_factor seconds
                    # a 45 degree delta will cause a 1/2 second turn
                    # a 1 degree delta will cause a .01 second turn
                    # 4.3.23 0.05 Multiplier added to shorten SL cycle and receive more GPS reads
                    sleep((1 - self.adjustment_factor)*0.4) # 4.21.23 Mutliplier set to .4 (see Notebook 2 Page 82-82)
                    # speed-up right tread back to topspeed
                    self.p1.start(topspeed)  # M2 speed back to full speed
                    self.p2.start(topspeed)  # M1 remains at full speed

                # correct by turning left
                if (self.delta_heading < 0 and self.move_forward_flag == 1) or (
                        self.delta_heading > 0 and self.move_backward_flag == 1):  # Turn Left
                    # slow left tread
                    print("TURN LEFT correction <<<")
                    self.number_of_left_adjustments = self.number_of_left_adjustments + 1
                    self.p1.start(topspeed)  # M2 remains at full speed
                    self.p2.start(topspeed * self.adjustment_factor)  # cut M1 speed to adjust heading
                    # Allow adjustment turn to continue for 1-adjustment_factor seconds
                    # a 45 degree delta will cause a 1/2 second turn
                    # a 1 degree delta will cause a .01 second turn
                    # 4.3.23 0.05 Multiplier added to shorten SL cycle and receive more GPS reads
                    sleep((1 - self.adjustment_factor)*0.4) # 4.21.23 Mutliplier set to .4 (see Notebook 2 Page 82-82)
                    # speed-up left tread back to topspeed
                    self.p1.start(topspeed)  # M2 remains at full speed
                    self.p2.start(topspeed)  # M1 speed back to full speed

                # keep track of how much time was spent in adjustment right/left 'turns'
                self.total_adjustment_time = self.total_adjustment_time + (1 - self.adjustment_factor)
                self.total_adjustment_factor = self.total_adjustment_factor + self.adjustment_factor
                self.total_number_of_adjustments = self.total_number_of_adjustments + 1
                # print("Total number of right adjustments:", self.number_of_right_adjustments)
                # print("Total number of left adjustments:", self.number_of_left_adjustments)
                if time() >= self.stop_time:
                    self.now_time = time()
                    self.actual_cruisetime = self.now_time - self.start_time
                    self.run_motors_flag = 0  # Stop loop!!

                # end of For loop, go back to increment cruise time

            # print("Total Adjustment Time: ", self.total_adjustment_time,"seconds.")
            # print("Total Travel Time:", self.stop_time-self.start_time,"seconds.")
            # print("Number of right adjustments: ", self.number_of_right_adjustments)
            # print("Number of left adjustments: ", self.number_of_left_adjustments)
            # print("Average Adjustment: ", self.total_adjustment_factor/self.total_number_of_adjustments)
            # print("Start Time:", self.start_time)
            # print("Stop Time:", self.stop_time)
            # print("Actual Cruise Time:", self.actual_cruisetime)

            if self.gps_operation_prevent_stop_motors_flag == 0:
                self.ramp_down(topspeed, self.ramp_step_time, 0)
                # stop motors
                print("Recursive Motor Stop:")
                self.recursiveStopMotors()  # Send rapid 5 stop motor commands
            # else:
            # print("Straight_line skipped recursiveStopMotors for GPS operation")

        except OSError:
            print("Compass Error likely detected! While running:")
            print("CytronclassXX.Cytronclass().straightline()")
            print("Recursive Motor Stop:")
            self.recursiveStopMotors()
            print("about to execute QUIT")
            quit()

        except:  # exit programe when keyboard interupt
            print("Recursive Motor Stop:")
            self.recursiveStopMotors()
            print("CytronclassXX.Cytronclass().straightline() exception detected")
            print("about to execute QUIT")
            quit()

    def navigate_point2point(self, to_coordinate_x, to_coordinate_y, gps_correction_list):

        self.time_navp2p_loop_start = time()

        to_coordinate_x = float(to_coordinate_x)
        to_coordinate_y = float(to_coordinate_y)

        # Error Detect
        if to_coordinate_x == 0 or to_coordinate_y == 0:
            print("ERROR DETECTED in navigate p2p: 0,0 passed as to_coordinates for navigate_p2p")
            print("Recursive Stop Motors and Quit()")
            self.recursiveStopMotors()
            quit()

        self.sensor_gps = SparkfungpsClass41.Gpsclass()  # execute SparkfungpsClass __init__
        self.sensor_compass = GY271.compass()  # execute gy271compassrobotXX.py __init__
        self.watchdog = Watchdogclass1.Watchdogclass()

        # initiate parameters
        self.first_motion_flag = 1  # will allow for a spin to target_heading at the very beginning of motion
        self.first_straightline_flag = 1 # will allow first straightline to be ignored by real time compass correction
        self.no_spin_allowed = 0  # within 3M of target, no spin will be allowed
        self.last_target_distance = 1000  # used for 'ran past' test, will return if current distance > than this variable
        self.collision_with_object_knocked_off_course = 0
        self.now_time = time()
        self.log_filename_snippet = "log_navigate_p2p_" + str(self.now_time)
        # self.check_validity_of_gps_broadcast = 1
        self.detect45_delta_heading = 0
        self.final_approach_leg_stop_flag = 0
        self.last_coordinate_x = 0
        self.last_coordinate_y = 0
        self.last_time_stamp = 0
        self.real_time_compass_correction = 0
        self.current_atan2_heading_after_motion = 0
        self.distance_traveled_after_motion = 0
        self.update_previous_coordinate_flag = 0
        self.fresh_gps_broadcast_read = 0
        self.time_navp2p_loop_measured_preSL = 0
        self.time_navp2p_loop_measured_SL = 0
        self.time_navp2p_loop_measured_postSL = 0
        self.time_navp2p_loop_one = 0
        self.time_navp2p_loop_two = 0
        self.time_navp2p_loop_start = 0
        self.time_navp2p_loop_end = 0
        self.last_count = 0
        self.gps_stall_flag = 0
        self.gps_stall_count = 0
        self.to_coordinate_initial_distance = 0
        self.to_coordinate_initial_distance_flag = 1
        self.deflection_distance = 0

        # 4.11.23 Real Time Compass Correction turned ON
        self.block_real_time_compass_correction = 'n'

        try:
            while True:  # return is used to break loop after arriving within 1/10 meter of to coordinate
                print("   ")
                print("00000 START Navigate_p2p BLOCK 00000")
                self.time_navp2p_loop_start = time()
                # start read GPS broadcast
                # this while loop delays releasing the broadcast read data until it is <.02 seconds old
                # this is to ensure that the entire nav_p2p loop is executed within one GPS epoch cycle
                while self.fresh_gps_broadcast_read == 0:
                    self.now_coordinate_x, self.now_coordinate_y, self.time_stamp, self.x, self.y, self.hacc, self.hacc_status, self.count = self.sensor_gps.read_gps_broadcast()
                    if time() - self.time_stamp < 0.02:
                        print("GPS is Fresh, fresh_gps_broadcast_read = 1")
                        self.fresh_gps_broadcast_read = 1
                    # the following catches a GPS stall, where data get's too old
                    if time() - self.time_stamp > 0.5: # this would indicate 5 GPS reads were skipped
                        print("GPS STALL detected during check of broadcast freshness, forcing a STOP")
                        print("Internal p2pX watchdog triggered for bad GPS data!!  Data age:", time() - self.time_stamp)
                        print("Stopping motors until GPS returns!!")
                        self.recursiveStopMotors()
                        self.gps_stall_flag = 1
                    print("---------------GPS FRESH LOOP")

                    print("time()", time(),  "minus self.time_stamp:", self.time_stamp, "Equals:", time() - self.time_stamp)
                    print("Fresh if < .02, stalled if > .5 ")
                    
                if self.gps_stall_flag == 1:
                    self.gps_stall_count = self.gps_stall_count + 1
                print("GPS stall count:", self.gps_stall_count)
                self.fresh_gps_broadcast_read = 0
                print("GPS Broadcast read:", self.now_coordinate_x, self.now_coordinate_y, self.hacc, self.hacc_status, self.count)
                self.delta_count = self.count - self.last_count - 1 # determine how many GPS measurements were skipped
                # determine age of broadcast and set cruisetime
                self.now_time = time()
                self.gps_broadcast_age = self.now_time - float(self.time_stamp)
                self.gps_broadcast_modified_cruisetime = .1 - self.gps_broadcast_age # 4.21.23 .05 changed to .1 to add more time for adjustments
                print("GPS broadcast modified Cruisetime:", self.gps_broadcast_modified_cruisetime)
                # end read GPS broadcast

                # start heading and distance calculations to "To:" point
                # First calculate heading with atan2 using get_heading_to_next_coordinate
                self.time_navp2p_window_a = time()
                self.target_heading = self.sensor_gps.get_heading_to_next_coordinate(self.now_coordinate_x, self.now_coordinate_y, to_coordinate_x, to_coordinate_y)
                # Second, using the gps_correction_list, substitute the atan2 heading calculation with the gps_correction_list compass heading
                # -12.9 declination is added to the atan2/true north calculation
                self.target_heading_corrected = int(float(gps_correction_list[int(self.target_heading)]))
                # 4.27.23 the very_first_calculated_target_heading is used for "deflection" calculation from a straightline between "initial from" and "to" coordinates
                # decided the angle used would be atan2 + file correction but not RealTime correction since it can vary significantly
                # the plan is to use historical RealTime measurements to tweak and improve the file_correction making RealTime of smaller and smaller significance.
                if self.first_motion_flag == 1:
                    self.very_first_calculated_target_heading = self.target_heading_corrected
                # finally, calculate distance to "To:" point
                self.target_distance = self.sensor_gps.get_distance_to_next_coordinate(self.now_coordinate_x, self.now_coordinate_y, to_coordinate_x, to_coordinate_y)
                # the following if statement records the to point initial distance for log file Final Landing Statistics
                if self.to_coordinate_initial_distance_flag == 1:
                    self.to_coordinate_initial_distance = self.target_distance
                    self.to_coordinate_initial_distance_flag = 0

                print("Now coordinate:", self.now_coordinate_x, ",", self.now_coordinate_y, "To coordinate:", to_coordinate_x, ",", to_coordinate_y)
                print("atan2 calculated heading to coordinate:", int(self.target_heading), "corrected heading:", int(self.target_heading_corrected))
                self.distance_red_alert = fontstyle.apply(self.target_distance, 'bold/white/red_BG')
                print(">>>>>>>>>>Distance to coordinate:", self.distance_red_alert, "Last distance:", self.last_target_distance)
                # end heading and distance calculations to "To:" point

                # 4.27.23 ERROR Condition Detected
                if self.target_distance > 50:
                    print("ERROR DETECTED!!")
                    print("Target Distance exceeds maximum pf 50M:", self.target_distance)
                    # stop motors
                    print("Recursive Motor Stop:")
                    self.recursiveStopMotors()  # Send rapid 5 stop motor commands
                    print("Quitting Code since can't keep trying to move toward this incorrect point")
                    quit()

                # ****** Start Real Time Compass reading correction
                # point 0 coordinate: previous_coordinate_x, previous_coordinate_y
                # point 1 coordinate: now_coordinate_x, now_coordinate_y
                # point 2 coordinate: to_coordinate_X, to_coordinate_y
                # atan2 calculated heading: target_heading
                # file corrected heading: target_heading_corrected

                if self.block_real_time_compass_correction != 'y': # 4.11.23 this code was enabled
                    # expected heading
                    # actual experienced heading
                    # error = diff between these two
                    if self.first_straightline_flag == 0:
                        # skip the first straightline loop because there is no previous coordinate on first motion
                        print("WXWXWXWXWXWXWXWXWXWXWXWXW")
                        print("****Navigate_p2p Real Time Compass Correction:****")
                        print("Previous Coordinate:", self.previous_coordinate_x, self.previous_coordinate_y)
                        print("Now Coordinate:", self.now_coordinate_x, self.now_coordinate_y)
                        self.distance_traveled_after_motion = self.sensor_gps.get_distance_to_next_coordinate(self.previous_coordinate_x, self.previous_coordinate_y, self.now_coordinate_x, self.now_coordinate_y)
                        self.current_atan2_heading_after_motion = self.sensor_gps.get_heading_to_next_coordinate(self.previous_coordinate_x, self.previous_coordinate_y, self.now_coordinate_x, self.now_coordinate_y)
                        # Real Time Compass correction calculation and 0/360 boundary correction
                        # target_heading is original atan2, delta is the amount of real time compass error that is measured between original atan2 and current_atan2
                        # 5.16.23 See Book 2 page 97 which explains that this error correction is then subtracted...
                        # 5.16.23 from the target_heading_corrected (file_corrected_heading) to correct for the compass error.
                        self.real_time_compass_correction = self.current_atan2_heading_after_motion - self.target_heading
                        if self.real_time_compass_correction < -180:
                            self.real_time_compass_correction = self.real_time_compass_correction + 360
                        if self.real_time_compass_correction > 180:
                            self.real_time_compass_correction = self.real_time_compass_correction - 360

                        print("Original atan2 calculated Target Heading", self.target_heading)
                        print("Target Heading file corrected only....prior to Real Time correction:", self.target_heading_corrected)
                        print("Current atan2 heading after motion:", self.current_atan2_heading_after_motion)
                        print("Distance traveled in first motion:", self.distance_traveled_after_motion)
                        print("Real time Compass correction:", self.real_time_compass_correction)
                        if self.distance_traveled_after_motion > 0.15: # GPS accuracy not good enough to allow for accurate heading calculations below .15
                            self.snapshot_target_heading_corrected = self.target_heading_corrected # save value for log_an_event prior to real time correction
                            self.target_heading_corrected = self.target_heading_corrected - self.real_time_compass_correction
                            # start correct for 0/360 boundary:
                            if self.target_heading_corrected < 0:
                                self.target_heading_corrected = self.target_heading_corrected + 360
                            if self.target_heading_corrected > 360:
                                self.target_heading_corrected = self.target_heading_corrected - 360
                            print("Target Heading Corrected with Real Time correction:", self.target_heading_corrected)
                            self.update_previous_coordinate_flag = 1
                            # end correct for 0/360 boundary
                            self.watchdog.log_an_event("REALTIME_compass_corrections_", "navigate_p2pX",
                                                       "distance_traveled_after_motion:", self.distance_traveled_after_motion,
                                                       "atan2 target_heading:", self.target_heading,
                                                       "file corrected target_heading:", self.snapshot_target_heading_corrected,
                                                       "atan2 heading after motion", self.current_atan2_heading_after_motion,
                                                       "Real Time Compass correction:", self.real_time_compass_correction,
                                                       "Real Time Corrected Heading:", self.target_heading_corrected)
                        else:
                            print("Distance Traveled is too short:", self.distance_traveled_after_motion, "Real Time Correction SUPPRESSED!!")

                    # set up previous coordinates (point 0) for next loop
                    self.previous_coordinate_x = self.now_coordinate_x
                    self.previous_coordinate_y = self.now_coordinate_y

                else:
                    print("RT COMPASS CORRECTION IS TURNED OFF")
                # End Real Time Compass reading correction

                self.time_navp2p_window_b = time()

                # Start FINAL APPROACH following last GPS read
                print("VVVVVVVVVVVVVVVVEntering Final Approach Calculations:")
                # start Calculate mps and mph
                self.current_mps_speed, self.current_mph_speed = self.sensor_gps.calculate_my_current_speed(
                    self.now_coordinate_x, self.now_coordinate_y, self.time_stamp, self.last_coordinate_x,
                    self.last_coordinate_y, self.last_time_stamp)
                # end Calculate mps and mph
                # start log speed data 3.1.23
                if self.current_mph_speed > .5:
                    self.watchdog.log_an_event("_Predator_speed_", "navigate_p2p", self.current_mph_speed, self.current_mps_speed, time())
                # end log speed data

                # calculate time to target coordinate based on speed
                if self.current_mps_speed > 0:
                    self.time_to_target = self.target_distance / self.current_mps_speed
                    print("Target Distance:", self.target_distance, "Current mps Speed:", self.current_mps_speed,
                          "Time to target:", self.time_to_target, "seconds")
                    # print("Time to target:", self.time_to_target, "seconds")

                if self.time_to_target < self.gps_broadcast_modified_cruisetime:  # time_to_target is less than remaining age of last GPS broadcast, no more GPS reads before arriving at the target point
                    self.gps_broadcast_modified_cruisetime = self.time_to_target  # reset cruisetime to time it takes to get to the point
                    print("Since this is less than remaining GPS broadcast age, modifying cruisetime to:",
                          self.gps_broadcast_modified_cruisetime)
                    self.watchdog.log_an_event(self.log_filename_snippet, "navigate_p2pX",
                                               "Since this is less than remaining GPS broadcast age, modifying cruisetime to:",
                                               self.gps_broadcast_modified_cruisetime, time())
                    self.final_approach_leg_stop_flag = 1
                    self.recursiveStopMotors()
                    print("Line 1213: Stopped after determining time_to_target is less than time to next GPS read")
                    print("Note GPS broadcast modified cruisetime above^^^^^ This should be the final movement time")
                    print("Should be on final approach to target coordinate")
                    print("Last GPS Broadcast Age:", self.gps_broadcast_age)
                    print("@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@")
                    print("DEBUG: Time_stamp of this GPS broadcast:", self.time_stamp)
                    print("DEBUG: Current Time:", time())
                    print("DEBUG: Elapsed time between GPS broadcast and current time:", time() - self.time_stamp)
                    print("@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@")
                    print()
                else:
                    self.last_coordinate_x = self.now_coordinate_x
                    self.last_coordinate_y = self.now_coordinate_y
                    self.last_time_stamp = self.time_stamp
                    print("Since this is greater than remaining GPS broadcast age:",
                          self.gps_broadcast_modified_cruisetime, "go back for another GPS cycle:")
                print("^^^^^^^^^^^^^^^^^ Leaving Final Approach Calculations")
                # End FINAL APPROACH following last GPS read

                self.time_navp2p_window_c = time()

                # Test if within target distance
                if self.target_distance < .25:  # 3.31.23 changed to .25M with final approach fine tuning
                    print("Robot arrived at target Point through ARRIVED WITHIN .25M!!")
                    self.watchdog.log_an_event(self.log_filename_snippet, "navigate_p2pX",
                                               "Robot has arrived within .25M of the TO coordinates.", time())
                    self.recursiveStopMotors()
                    # determine coordinates of & target distance from the Landing Coordinates
                    print("Standby, calculating distance from ARRIVAL POINT to TARGET POINT")
                    sleep(.11)  # delay to make sure a GPS read is done at the current stopped point
                    self.now_coordinate_x, self.now_coordinate_y, self.time_stamp, self.x, self.y, self.hacc, self.hacc_status, self.z = self.sensor_gps.read_gps_broadcast()
                    self.final_target_distance = self.sensor_gps.get_distance_to_next_coordinate(self.now_coordinate_x, self.now_coordinate_y, to_coordinate_x, to_coordinate_y)
                    self.final_target_heading = self.sensor_gps.get_heading_to_next_coordinate(self.now_coordinate_x, self.now_coordinate_y, to_coordinate_x, to_coordinate_y)
                    self.final_now_heading, self.x, self.y, self.z = self.sensor_compass.get_bearing()
                    print("$$$$$$$$$$$ Final Distance to target point:", self.final_target_distance)
                    print("$$$$$$$$$$$ Final Heading to target point:", self.final_target_heading)
                    self.clock_position_angle = self.final_target_heading - self.final_now_heading
                    if self.clock_position_angle < 0:
                        self.clock_position_angle = self.clock_position_angle + 360
                    if self.clock_position_angle > 360:
                        self.clock_position_angle = self.clock_position_angle - 360
                    self.clock_position = round(self.clock_position_angle/360*12)
                    print("Target is positioned at ", self.clock_position, "o'clock")
                    self.watchdog.log_an_event(self.log_filename_snippet, "navigate_p2pX",
                                               "Robot arrived within .25M of target:", self.final_target_distance)
                    self.watchdog.log_an_event(self.log_filename_snippet, "navigate_p2pX",
                                               "The target coordinates were:", to_coordinate_x, to_coordinate_y)
                    self.watchdog.log_an_event(self.log_filename_snippet, "navigate_p2pX",
                                               "Final LANDING coordinates:", self.now_coordinate_x, self.now_coordinate_y)
                    self.watchdog.log_an_event(self.log_filename_snippet, "navigate_p2pX",
                                               "The last target heading:", self.target_heading_corrected,
                                               "Last NOW heading", self.detect45_now_heading)
                    self.watchdog.log_an_event(self.log_filename_snippet, "navigate_p2pX",
                                               "The Delta angle error:", self.detect45_delta_heading)
                    self.watchdog.log_an_event(self.log_filename_snippet, "navigate_p2pX",
                                               "Final LANDING Clock Postion:", self.clock_position)

                    # 4.26.23 Adding log file for final landing statistics
                    self.watchdog.log_an_event("_Final_Landing_statistics_", "navigate_p2p",
                                               "Robot arrived within .25M of target:", self.final_target_distance,
                                               "Final LANDING Clock Postion:", self.clock_position,
                                               "Initial Distance:", self.to_coordinate_initial_distance,
                                               time())

                    print("Now Returning from function...")
                    return

                # Start Calculating Closing Boundary parameters
                if self.target_distance < 3:  # within 3 meter so switch to slower speed
                    self.topspeed = 100  # 1.15.23 set to 75 was 50
                    self.no_spin_allowed = 1  # no spins are allowed within 3M of target
                    # print("Within 3 meter still at 100% speed and no correcting spins allowed")
                else:
                    self.topspeed = 100
                    # print("Running FULL Speed")
                # End Calculating Closing Boundary parameters

                # start check for delta > 45 to insert a spin mid journey
                self.watchdog.watchdog_call("compass", "start", .15)
                self.detect45_now_heading, self.x, self.y, self.z = self.sensor_compass.get_bearing()
                self.watchdog.watchdog_call("compass", "stop", .15)
                if self.detect45_now_heading > self.target_heading_corrected:
                    self.detect45_delta_heading = self.detect45_now_heading - self.target_heading_corrected
                    if self.detect45_delta_heading > 180:
                        self.detect45_delta_heading = abs(self.detect45_delta_heading - 360)
                    print("Now heading:", self.detect45_now_heading, "is greater than target heading",
                          self.target_heading_corrected, "Delta Heading is:", self.detect45_delta_heading)
                if self.detect45_now_heading < self.target_heading_corrected:
                    self.detect45_delta_heading = self.target_heading_corrected - self.detect45_now_heading
                    if self.detect45_delta_heading > 180:
                        self.detect45_delta_heading = abs(self.detect45_delta_heading - 360)
                    print("Now heading:", self.detect45_now_heading, "is less than target heading",
                          self.target_heading_corrected, "Delta Heading is:", self.detect45_delta_heading)
                # 2.22.23 following IF could be combined with one of the above two IF,
                # but since this was a logic error, breaking it out as a separate IF to verify correct operation
                if self.detect45_now_heading == self.target_heading_corrected:
                    print("Now heading:", self.detect45_now_heading, "equals target heading",
                          self.target_heading_corrected)
                    self.detect45_delta_heading = 0
                    print("Delta Heading is:", self.detect45_delta_heading)
                # start detected an obstacle knocking robot off course
                if self.first_motion_flag == 0 and self.detect45_delta_heading > 35 and self.no_spin_allowed == 0:
                    # indicates an object struck robot off course before reaching within 3M of the target.
                    # 1.15.23 was 45, had reading of 44.6 caused compass-error-band straightline 45 quit
                    print("Object has knocked robot off course!! Ramp down!!")
                    self.ramp_down(self.topspeed, .01, 0)  # ramp down from current straightline speed to execute a spin
                    print("collision with object detected!!!")
                    self.collision_with_object_knocked_off_course = 1  # a >45° change in heading indicates robot is off course (here, because of an object)
                    # 5.16.23 Following pause added to stop the code after collision to DEBUG intermittent "Knocked off course errors"
                    print("DEBUG intermittent >>Knocked off course errors<<")
                    print("Robot is being paused to examine state that caused this error")
                    self.recursiveStopMotors()
                    self.pause_now = input("Hit enter to continue....")
                    print("Not sure what happens now since a recursiveStopMotors was run")

                # end detected an object knocking the robot off course
                # END check for delta > 45 to insert a spin mid journey

                # Start Test if robot 'ran past' the target point by detecting large delta angle
                if self.first_motion_flag == 0 and self.detect45_delta_heading > 25 and self.no_spin_allowed == 1:
                    print("Robot has passed the target point.  Stop!!!")
                    print("Detected by large delta angle at time:", time())
                    print("Last Target Distance:", self.last_target_distance, "Now target distance:",
                          self.target_distance)
                    print("Now Target Heading:", self.detect45_now_heading, "Last Target Heading:",
                          self.target_heading_corrected)
                    print("Detect45 delta (off from tgt heading):", self.detect45_delta_heading)
                    self.recursiveStopMotors()

                    # "ran past" error, start read GPS broadcast
                    print("Robot arrived at target Point through RAN PAST ERROR!!")
                    sleep(.11)  # delay long enough to ensure next GPS read
                    self.now_coordinate_x, self.now_coordinate_y, self.time_stamp, self.x, self.y, self.hacc, self.hacc_status, self.z = self.sensor_gps.read_gps_broadcast()
                    self.final_target_distance = self.sensor_gps.get_distance_to_next_coordinate(
                        self.now_coordinate_x, self.now_coordinate_y, to_coordinate_x, to_coordinate_y)
                    self.final_target_heading = self.sensor_gps.get_heading_to_next_coordinate(
                        self.now_coordinate_x, self.now_coordinate_y, to_coordinate_x, to_coordinate_y)
                    self.final_now_heading, self.x, self.y, self.z = self.sensor_compass.get_bearing()
                    print("$$$$$$$$$$$ Distance to target point:", self.final_target_distance)
                    print("$$$$$$$$$$$ Heading to target point:", self.final_target_heading)
                    self.clock_position_angle = self.final_target_heading - self.final_now_heading
                    if self.clock_position_angle < 0:
                        self.clock_position_angle = self.clock_position_angle + 360
                    if self.clock_position_angle > 360:
                        self.clock_position_angle = self.clock_position_angle - 360
                    self.clock_position = round(self.clock_position_angle / 360 * 12)
                    print("Target is positioned at ", self.clock_position, "o'clock")
                    self.watchdog.log_an_event(self.log_filename_snippet, "navigate_p2pX",
                                               "Robot RAN PAST the target coordinates by:", self.final_target_distance)
                    self.watchdog.log_an_event(self.log_filename_snippet, "navigate_p2pX",
                                               "Final LANDING coordinates:", self.now_coordinate_x, self.now_coordinate_y)
                    self.watchdog.log_an_event(self.log_filename_snippet, "navigate_p2pX",
                                               "The Target coordinates were:", to_coordinate_x, to_coordinate_y)
                    self.watchdog.log_an_event(self.log_filename_snippet, "navigate_p2pX",
                                               "The last target heading:", self.target_heading_corrected,
                                               "Last NOW heading", self.detect45_now_heading)
                    self.watchdog.log_an_event(self.log_filename_snippet, "navigate_p2pX",
                                               "The Delta angle error:", self.detect45_delta_heading)
                    self.watchdog.log_an_event(self.log_filename_snippet, "navigate_p2pX",
                                               "Final LANDING Clock Postion:", self.clock_position)

                    # 4.26.23 Adding log file for final landing statistics
                    self.watchdog.log_an_event("_Final_Landing_statistics_", "navigate_p2p",
                                               "Robot RAN PAST the target coordinates by:", self.final_target_distance,
                                               "Final LANDING Clock Postion:", self.clock_position,
                                               "Initial Distance:", self.to_coordinate_initial_distance,
                                               time())

                    print("Now Returning from function...")
                    # quit() 3.5.23 replaced with return
                    return
                else:
                    self.last_target_distance = self.target_distance  # set this variable for next loop to check for 'ran past'
                # End Test if robot 'ran past' the target point by detecting large delta angle

                # Start Test if robot 'ran past' the target point by now target distance > last target distance
                if self.first_motion_flag == 0 and self.target_distance > self.last_target_distance and self.no_spin_allowed == 1:
                    print("Robot has passed the target point.  Stop!!!")
                    print("Detected by now target distance > last target distance at time:", time())
                    print("Last Target Distance:", self.last_target_distance, "Now target distance:",
                          self.target_distance)
                    print("Now Target Heading:", self.detect45_now_heading, "Last Target Heading:",
                          self.target_heading_corrected)
                    print("Detect45 delta (off from tgt heading):", self.detect45_delta_heading)
                    print("Real Time Correction likely masking this Ran Past state")
                    self.recursiveStopMotors()

                    # "ran past" error, start read GPS broadcast
                    print("Robot arrived at target Point through RAN PAST ERROR now_target_distance > last_target_distance!!")
                    sleep(.11)  # delay long enough to ensure next GPS read
                    self.now_coordinate_x, self.now_coordinate_y, self.time_stamp, self.x, self.y, self.hacc, self.hacc_status, self.z = self.sensor_gps.read_gps_broadcast()
                    self.final_target_distance = self.sensor_gps.get_distance_to_next_coordinate(
                        self.now_coordinate_x, self.now_coordinate_y, to_coordinate_x, to_coordinate_y)
                    self.final_target_heading = self.sensor_gps.get_heading_to_next_coordinate(
                        self.now_coordinate_x, self.now_coordinate_y, to_coordinate_x, to_coordinate_y)
                    self.final_now_heading, self.x, self.y, self.z = self.sensor_compass.get_bearing()
                    print("$$$$$$$$$$$ Distance to target point:", self.final_target_distance)
                    print("$$$$$$$$$$$ Heading to target point:", self.final_target_heading)
                    self.clock_position_angle = self.final_target_heading - self.final_now_heading
                    if self.clock_position_angle < 0:
                        self.clock_position_angle = self.clock_position_angle + 360
                    if self.clock_position_angle > 360:
                        self.clock_position_angle = self.clock_position_angle - 360
                    self.clock_position = round(self.clock_position_angle / 360 * 12)
                    print("Target is positioned at ", self.clock_position, "o'clock")
                    self.watchdog.log_an_event(self.log_filename_snippet, "navigate_p2pX",
                                               "Robot RAN PAST the target coordinates by now target distance > last target distance")
                    self.watchdog.log_an_event(self.log_filename_snippet, "navigate_p2pX",
                                               "Robot RAN PAST the target coordinates by:", self.final_target_distance)
                    self.watchdog.log_an_event(self.log_filename_snippet, "navigate_p2pX",
                                               "Final LANDING coordinates:", self.now_coordinate_x, self.now_coordinate_y)
                    self.watchdog.log_an_event(self.log_filename_snippet, "navigate_p2pX",
                                               "The Target coordinates were:", to_coordinate_x, to_coordinate_y)
                    self.watchdog.log_an_event(self.log_filename_snippet, "navigate_p2pX",
                                               "Last distance to point:", self.last_target_distance)
                    self.watchdog.log_an_event(self.log_filename_snippet, "navigate_p2pX",
                                               "Now distance to point:", self.target_distance)
                    self.watchdog.log_an_event(self.log_filename_snippet, "navigate_p2pX",
                                               "The last target heading:", self.target_heading_corrected,
                                               "Last NOW heading", self.detect45_now_heading)
                    self.watchdog.log_an_event(self.log_filename_snippet, "navigate_p2pX",
                                               "The Delta angle error:", self.detect45_delta_heading)
                    self.watchdog.log_an_event(self.log_filename_snippet, "navigate_p2pX",
                                               "Final LANDING Clock Postion:", self.clock_position)

                    # 4.26.23 Adding log file for final landing statistics
                    self.watchdog.log_an_event("_Final_Landing_statistics_", "navigate_p2p",
                                               "Robot RAN PAST the target coordinates by:", self.final_target_distance,
                                               "Final LANDING Clock Postion:", self.clock_position,
                                               "Initial Distance:", self.to_coordinate_initial_distance,
                                               time())

                    print("Now Returning from function...")
                    # quit() 3.5.23 replaced with return
                    return
                else:
                    self.last_target_distance = self.target_distance  # set this variable for next loop to check for 'ran past'
                # End Test if robot 'ran past' the target point by detecting large delta angle





                self.time_navp2p_window_d = time()
                # Start Spin due to either first motion or an object detected
                if self.first_motion_flag == 1 or self.collision_with_object_knocked_off_course == 1:  # do a spin at start or due to an obstacle
                    print("Executing Spin, detect45_delta_heading:", self.detect45_delta_heading)
                    self.move("turnto", self.topspeed, 0, .01, 0, self.target_heading_corrected)  # spin to calculated heading
                    # turnto command with 0 turn differential decodes to a spin by Cytronclass64
                    print("Spin executed for first motion:", self.first_motion_flag, "or Collision with Object:",
                          self.collision_with_object_knocked_off_course)
                    if self.collision_with_object_knocked_off_course == 1:
                        self.collision_with_object_knocked_off_course = 0  # clear flag after spin
                        self.first_straightline_flag = 1 # no previous coordinates so need to set this flag to 1 to avoid repeated spins
                # End Spin
                # Start straightline
                else:
                    print("UUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUU")
                    print("NAVIGATE P2P parameters")
                    print("Straightline parameters:topspeed", self.topspeed, "\ngps mod cruisetime", self.gps_broadcast_modified_cruisetime)
                    print("Target Heading:", self.target_heading, "\ntarget heading corrected", self.target_heading_corrected)
                    print("Very_first_calculated_target_heading:", self.very_first_calculated_target_heading)

                    # 4.27.23 Calculating distance deflection from a straight line drawn between original "From" coordinate and target "To" coordinate
                    print("////////////////Deflection calculation headings:", self.very_first_calculated_target_heading, self.snapshot_target_heading_corrected)
                    self.deflection_angle = abs(self.very_first_calculated_target_heading - self.target_heading_corrected)
                    print("////////////////Deflection Angle:", self.deflection_angle)
                    self.deflection_angle_radians = (self.deflection_angle/180 * math.radians(180))
                    self.deflection_distance = self.target_distance * math.sin(self.deflection_angle_radians)
                    print("///////////////Deflection Distance:", self.deflection_distance)
                    print("Robot is deflected ", self.deflection_distance, "meters from the straight line path between the >From< and >To< points")

                    self.time_navp2p_loop_one = time()
                    self.straight_line("forwardgps", self.topspeed, self.gps_broadcast_modified_cruisetime, self.target_heading_corrected)
                    self.time_navp2p_loop_two = time()
                    
                    self.first_straightline_flag = 0 # turn off first straightline flag so that next loop calculates real time compass correction

                    # print("Completed this leg.  Going back to beginning of loop to calculate next leg.")
                    if self.final_approach_leg_stop_flag == 1:  # just completed last straightline, we should be at point, STOP!!!
                        print(" The Last Leg was FINAL APPROACH Leg!!")
                        print("Arrived at the target Coordinate!!")
                        print("STOPPING MOTORS")
                        self.ramp_down(100, .001, 0)
                        self.recursiveStopMotors()
                        print("Robot arrived at target Point through FINAL APPROACH!!")
                        print("Standby, calculating distance from ARRIVAL POINT to TARGET POINT")
                        sleep(.11)  # delay to make sure a GPS read is done at the current stopped point
                        self.now_coordinate_x, self.now_coordinate_y, self.time_stamp, self.x, self.y, self.hacc, self.hacc_status, self.z = self.sensor_gps.read_gps_broadcast()
                        self.final_target_distance = self.sensor_gps.get_distance_to_next_coordinate(
                            self.now_coordinate_x, self.now_coordinate_y, to_coordinate_x, to_coordinate_y)
                        self.final_target_heading = self.sensor_gps.get_heading_to_next_coordinate(
                            self.now_coordinate_x, self.now_coordinate_y, to_coordinate_x, to_coordinate_y)
                        self.final_now_heading, self.x, self.y, self.z = self.sensor_compass.get_bearing()
                        print("$$$$$$$$$$$ Distance to target point:", self.final_target_distance)
                        print("$$$$$$$$$$$ Heading to target point:", self.final_target_heading)
                        self.clock_position_angle = self.final_target_heading - self.final_now_heading
                        if self.clock_position_angle < 0:
                            self.clock_position_angle = self.clock_position_angle + 360
                        if self.clock_position_angle > 360:
                            self.clock_position_angle = self.clock_position_angle - 360
                        self.clock_position = round(self.clock_position_angle / 360 * 12)
                        print("Target is positioned at ", self.clock_position, "o'clock")
                        # log final approach details
                        self.watchdog.log_an_event(self.log_filename_snippet, "navigate_p2pX",
                                                   "Robot FINAL APPROACHed the target coordinates within:", self.target_distance)
                        self.watchdog.log_an_event(self.log_filename_snippet, "navigate_p2pX",
                                                   "The target coordinates were:", to_coordinate_x, to_coordinate_y)
                        self.watchdog.log_an_event(self.log_filename_snippet, "navigate_p2pX",
                                                   "Final LANDING coordinates:", self.now_coordinate_x,
                                                   self.now_coordinate_y)
                        self.watchdog.log_an_event(self.log_filename_snippet, "navigate_p2pX",
                                                   "The last target heading:", self.target_heading_corrected,
                                                   "Last NOW heading", self.detect45_now_heading)
                        self.watchdog.log_an_event(self.log_filename_snippet, "navigate_p2pX",
                                                   "The Delta angle error:", self.detect45_delta_heading)
                        self.watchdog.log_an_event(self.log_filename_snippet, "navigate_p2pX",
                                                   "Final LANDING Clock Postion:", self.clock_position)

                        # 4.26.23 Adding log file for final landing statistics
                        self.watchdog.log_an_event("_Final_Landing_statistics_", "navigate_p2p",
                                                   "Robot FINAL APPROACHed the target coordinates within:",
                                                   self.final_target_distance,
                                                   "Final LANDING Clock Postion:", self.clock_position,
                                                   "Initial Distance:", self.to_coordinate_initial_distance,
                                                   time())

                        # quit() 3.5.23 replaced with return
                        return
                # print("first motion flag set to 0")
                self.first_motion_flag = 0
                # setting flag to 0 ensures prior spin is only done at the very beginning
                # End straightline

                self.time_navp2p_loop_end = time()

                self.time_navp2p_loop_measured_preSL = self.time_navp2p_loop_one - self.time_navp2p_loop_start
                self.time_navp2p_loop_measured_SL = self.time_navp2p_loop_two - self.time_navp2p_loop_one
                self.time_navp2p_loop_measured_postSL = self.time_navp2p_loop_end - self.time_navp2p_loop_two
                self.time_navp2p_loop_measured_total = self.time_navp2p_loop_end - self.time_navp2p_loop_start

                self.time_navp2p_loop_GPS_read = self.time_navp2p_window_a - self.time_navp2p_loop_start
                self.time_navp2p_loop_compass_read = self.time_navp2p_window_b - self.time_navp2p_window_a
                self.time_navp2p_loop_final_approach = self.time_navp2p_window_c - self.time_navp2p_window_b
                self.time_navp2p_loop_position_checks = self.time_navp2p_window_d - self.time_navp2p_window_c
                self.time_navp2p_loop_spin = self.time_navp2p_loop_one - self.time_navp2p_window_d
                print(">>>Total Code Execution Time Elapsed:", self.time_navp2p_loop_measured_total,
                                           "pre: " + str(self.time_navp2p_loop_measured_preSL),
                                           "SL: " + str(self.time_navp2p_loop_measured_SL),
                                           "post: " + str(self.time_navp2p_loop_measured_postSL),
                                           "GPS Br: " + str(self.time_navp2p_loop_GPS_read),
                                            "Compass: " + str(self.time_navp2p_loop_compass_read),
                                            "Final A: " + str(self.time_navp2p_loop_final_approach),
                                            "Position checks: " + str(self.time_navp2p_loop_position_checks),
                                            "Spin: " + str(self.time_navp2p_loop_spin))
                # log data start
                self.watchdog.log_an_event(self.log_filename_snippet, "navigate_p2pX", "NEW",
                                           self.now_coordinate_x, self.now_coordinate_y,
                                           to_coordinate_x, to_coordinate_y,self.previous_coordinate_x,self.previous_coordinate_y,
                                           self.count, # infinite counting loop that allows determination of how many GPS reads get skipped between straightline executions
                                           "Skipped: ", self.delta_count,
                                           "age: " + str(self.gps_broadcast_age),
                                           self.target_distance,
                                           self.deflection_distance, # deflected distance from line drawn between "From" and "To" coordinates
                                           self.target_heading_corrected,
                                           # self.real_time_compass_correction,  # real time correction data passed to SL
                                           self.detect45_now_heading, # real time compass measurement used to determine how far off of the target heading robot is...
                                           self.detect45_delta_heading, # calculated delta of how far off target heading robot is.
                                           self.very_first_calculated_target_heading,
                                           "Real Time:",
                                           self.first_straightline_flag,
                                           self.target_heading, # atan2 calculated heading
                                           self.snapshot_target_heading_corrected, # target heading corrected with correction file
                                           self.current_atan2_heading_after_motion,
                                           self.distance_traveled_after_motion,
                                           self.real_time_compass_correction,
                                           self.target_heading_corrected, # target heading corrected with file & real time correction
                                           # self.time_stamp,
                                           # time(),
                                           ">>>Total:",
                                           self.time_navp2p_loop_measured_total,
                                           "pre: " + str(self.time_navp2p_loop_measured_preSL),
                                           "SL: " + str(self.time_navp2p_loop_measured_SL),
                                           "post: " + str(self.time_navp2p_loop_measured_postSL),
                                           "GPS Br: " + str(self.time_navp2p_loop_GPS_read),
                                            "Compass: " + str(self.time_navp2p_loop_compass_read),
                                            "Final A: " + str(self.time_navp2p_loop_final_approach),
                                            "Position checks: " + str(self.time_navp2p_loop_position_checks),
                                            "Spin: " + str(self.time_navp2p_loop_spin))
                # log data end
                self.last_count = self.count  # keep track of gps count number for previous gps broadcast read

        except KeyboardInterrupt:  # exit program when keyboard interrupt
            print("navigate_point2point exception detected")
            print("about to execute QUIT")
            quit()

    def ramp_up(self, topspeed, ramp_step_time):
        # start ramp up
        print("Ramp up...")
        for i in range(topspeed):
            self.p1.start(i)  # incremental set speed for M1 to topspeed
            self.p2.start(i)  # incremental set speed for M2 to topspeed
            sleep(ramp_step_time)  # momentary delay in each step
        # end ramp-up

    def ramp_down(self, topspeed, ramp_step_time, compass_turn_ramp_down):
        # start ramp down
        print("Ramp down...")
        print("ramp_step_time:", ramp_step_time)
        if compass_turn_ramp_down == 1:  # 8.5.22 changed this from no ramp to a gradual end ramp
            topspeed = int(.50 * topspeed)  # 8.11.22 uturn and turnto end at 50%, ramp down has to start at 50%
        for i in reversed(range(topspeed)):
            self.p1.start(i)  # decremental set speed for M1 from topspeed
            self.p2.start(i)  # decremental set speed for M2 from topspeed
            sleep(ramp_step_time)  # momentary delay in each step
        # stop ramp down

    def recursiveStopMotors(self):  # send rapid 5 stop motor commands
        for recursive_count in (range(5)):
            self.p1.start(0)  # set speed to 0
            self.p2.start(0)  # set speed to 0
            print("STOP! ", recursive_count + 1)
            sleep(.1)  # 5 stops will be executed in 1/2 seconds
        print("Recursive Stop Motor 5 commands in 1/2 second")

    def turnOffMotors(self):
        self.p1.start(0)  # set speed to 0
        self.p2.start(0)  # set speed to 0
        print("Cytron Turn off Motors executed")

    def rockmeloose(self, spin_direction):  # spin_direction refers to direction of spin that initiated this rockmeloose
        # determine direction of initial rocking motion and set Cytron
        if spin_direction.lower() == "spinright":
            self.rockme_spin_flag = 1
        else:
            if spin_direction.lower() == "spinleft":
                self.rockme_spin_flag = 0
            else:
                print("Cytronclass.rockmeloose() error, improper command:", spin_direction)
                print("Cytronclass.rockmeloose() recursive stop motors and quit()")
                self.recursiveStopMotors()
                quit()
        # start rocking motion
        try:
            print("Starting rockmeloose")
            self.rock_count = 0
            while self.rock_count < 6:  # do 6 iterations of rocking
                # set Cytron for rocking direction
                # print("Rockme Spin Flag:",self.rockme_spin_flag)
                if self.rockme_spin_flag == 1:
                    self.dig1_control = GPIO.HIGH  # spin right commands initiated by a spin right calling rockmeloose
                    self.dig2_control = GPIO.LOW  # spin right commands initiated by a spin right calling rockmeloose
                if self.rockme_spin_flag == 0:
                    self.dig1_control = GPIO.LOW  # spin left commands initiated by a spin left calling rockmeloose
                    self.dig2_control = GPIO.HIGH  # spin left commands initiated by a spin left calling rockmeloose
                GPIO.output(self.DIG1, self.dig1_control)  # set DIG1 according to rockme_spin_flag
                GPIO.output(self.DIG2, self.dig2_control)  # set DIG2 according to rockme_spin_flag
                # start ramp up
                for i in range(0, 76, 5):
                    # print ("ramp up iteration :", i)
                    self.p1.start(i)  # incremental set speed for M1 to topspeed
                    self.p2.start(i)  # incremental set speed for M2 to topspeed
                    sleep(0.01)  # momentary delay in each step
                # start ramp down
                for i in reversed(range(0, 76, 5)):
                    # print ("ramp down iteration :", i)
                    self.p1.start(i)  # decremental set speed for M1 from topspeed
                    self.p2.start(i)  # decremental set speed for M2 from topspeed
                    sleep(0.01)  # momentary delay in each step
                # increment count
                self.rock_count = self.rock_count + 1
                # reverse rocking move_direction
                if self.rockme_spin_flag == 1:
                    self.rockme_spin_flag = 0
                else:
                    self.rockme_spin_flag = 1
            print("Ending rockmeloose")
        except:
            print("Cytronclass2.rockmeloose() exception detected")
            print("Recursive Motor Stop:")
            self.recursiveStopMotors()
            print("about to execute QUIT")
            quit()

    # end rockmeloose

    def read_gps_correction_file(self, correction_file_name):

        # reading in correction file
        self.gps_correction_list = [0]
        self.gps_correction_delta_list = [0]
        self.count = 0
        # load correction_list with 361 zeros to initialize list size (0-360 elements)
        while self.count < 360:  # initializing list to 361 elements (0-360)
            self.gps_correction_list.append(0)
            self.gps_correction_delta_list.append(0)
            self.count = self.count + 1

        self.read_file_handle = open(correction_file_name, 'r')
        print("About to enter read Correction File data loop")
        for self.read_iteration_variable in self.read_file_handle:
            self.temp_list = self.read_iteration_variable.split(",")
            # print("temp_list data read from correction file:", temp_list)
            if self.temp_list[0] != "atan2":
                # print("temp_list[0]", temp_list[0])
                # print("Correction list index about to be used:", int(temp_list[0]))
                self.gps_correction_list[int(self.temp_list[0])] = self.temp_list[1]
                self.gps_correction_delta_list[int(self.temp_list[0])] = self.temp_list[2]  # delta correction amount
                # this loop reads the 0-360 data which becomes index for correction_list[]
                # for each index, an element of the list is assigned
                # correction_list(x}=y, x is atan2 calculated heading, y is the equivalent compass heading
        return self.gps_correction_list, self.gps_correction_delta_list

    def map_traverse(self, map_filename, end_waypoint, gps_correction_list):
    # 5.13.23 def map_traverse(self, map_filename, end_waypoint, gps_correction_list, control_parameters_list):

        self.sensor_gps = SparkfungpsClass41.Gpsclass()  # execute SparkfungpsClass __init__

        # initiate parameters
        self.map_file_row_count = 0
        self.map_matrix_index_first = 0
        self.found_end_waypoint_in_map_file = 0
        self.skipped_first_waypoint_flag = 0

        # (0) START Read Map file into a matrix
        # determine number of rows in the map
        self.temp_file_handle = open(map_filename)  # file handle
        # The following for loop counts all the rows in the file
        for self.temp_iteration_variable in self.temp_file_handle:
            self.map_file_row_count = self.map_file_row_count + 1
        print(map_filename, "has", self.map_file_row_count, "rows.")

        # initiating map matrix
        self.map_matrix = [0, 0, 0, 0]
        self.count = 0
        # load map_matrix with three zeros per row
        for x in range(0, self.map_file_row_count, 1):  # initializing matrix from 1 to row_count, step=1
            self.map_matrix.append([0, 0, 0, 0])

        # Open map file .csv and read into map_matrix
        self.map_file_handle = open(map_filename)
        # The following for loop will iterate through all lines of the file creating the matrix
        for self.map_file_iteration_variable in self.map_file_handle:
            self.map_list = self.map_file_iteration_variable.rstrip('\n')  # first, strip off new line \n
            self.map_list = self.map_list.split(',')  # split into a list
            self.map_matrix[self.map_matrix_index_first] = self.map_list
            # print(self.map_list)
            # print(self.map_matrix[self.map_matrix_index_first])
            self.map_matrix_index_first = self.map_matrix_index_first + 1
        print(map_filename, " has been read into map_traverse...")

        # print out the map matrix
        print("Now printing Matrix:")
        for self.count in range(0, self.map_file_row_count, 1):
            print(self.map_matrix[self.count])
        print("Target End Waypoint:", end_waypoint)
        # (0) END Read Map file into a matrix

        # 5.13.23 future patrol() code
        # # start read control parameters
        # # this code looks wrong.....
        #
        #
        # for self.control_parameter in control_parameters_list
        #
        # read parameters included with a flag
        #   if self.next_element_is_flag = 1:
        #        if self.next_element_is = "patrol_pause_time"
        #                 self.patrol_pause_time = float(self.control_parameter)
        #                 self.next_element_flag_is_flag = 0 # could still be 1 if another parameter is needed
        #   elif: # whatever next parameter search is ......

        # read flags
        #   if control_parameter == '-p'
        #       self.patrol_map_function = 1
        #       self.next_element_is = "patrol_pause_time"
        #       self.next_element_is_flag = 1 # tells the for loop that the next element is already identified
        #   elif: # whatever next flag search is....


        try:
            # (1) Where am I now?
            self.now_coordinate_x, self.now_coordinate_y, self.time_stamp, self.x, self.y, self.hacc, self.hacc_status, self.count = self.sensor_gps.read_gps_broadcast()
            #
            # (2) START Scan for closest waypoint and end_waypoint sequence number in the map matrix
            #    calculate distance to all of the path way-points.  find point with shortest distance....this becomes
            #    point that is the closest waypoint and becomes the starting point where the robot starts to traverse the path.
            self.closest_distance = 10000
            self.closest_waypoint_sequence_number = 0
            for x in range(0, self.map_file_row_count, 1):  # step through all points to find closest
                print("Scanning for closest Waypoint....index:", x)
                print(self.map_matrix[x][0])
                print(self.map_matrix[x][1])
                print(self.map_matrix[x][2])
                print(self.map_matrix[x][3])

                self.how_close = self.sensor_gps.get_distance_to_next_coordinate(self.now_coordinate_x,
                                                                                 self.now_coordinate_y,
                                                                                 float(self.map_matrix[x][2]),
                                                                                 float(self.map_matrix[x][3]))
                print("The distance to this point is:", self.how_close)
                print("DEBUG map_matrix[x]:[1]", self.map_matrix[x][1], "end_waypoint:", end_waypoint)
                if self.map_matrix[x][1] == end_waypoint:  # find sequence number of the end_waypoint
                    self.end_waypoint_sequence_number = int(self.map_matrix[x][0])
                    print("End waypoint sequence number is:", self.end_waypoint_sequence_number)
                    self.found_end_waypoint_in_map_file = 1
                if self.how_close < self.closest_distance:
                    self.closest_distance = self.how_close
                    self.closest_waypoint_sequence_number = int(self.map_matrix[x][0])
                    self.closest_waypoint = self.map_matrix[x][1]
                    self.closest_coordinate_x = float(self.map_matrix[x][2])
                    self.closest_coordinate_y = float(self.map_matrix[x][3])
            if self.found_end_waypoint_in_map_file == 0:
                print("End Waypoint could not be found in Map File.")
                print("Quitting program...")
                quit()
            print("The closest point in the map is sequence number:", self.closest_waypoint_sequence_number,
                  "which is Waypoint:", self.closest_waypoint)
            print("The distance of this point is:", self.closest_distance)

            # (3) Navigate p2p to closest point in map
            self.traverse_start_time = time()
            # following if cancels moving to closest coordinate if robot is already within .25m
            if self.closest_distance > 0.25:
                self.navigate_point2point(self.closest_coordinate_x, self.closest_coordinate_y, gps_correction_list)
            else:
                self.skipped_first_waypoint_flag = 1

            print("Arrived at Waypoint:", self.closest_waypoint)
            if self.closest_waypoint_sequence_number == self.end_waypoint_sequence_number:
                print("Closest Waypoint in the map AND the End Waypoint are the SAME")
                print("Robot has moved to the End Waypoint and will Quit() program!!")
                quit()

            # (4) determine direction to traverse map by figuring out if end_waypoint sequence number is higher or lower than the closest point
            print("DEBUG: Part(4):", self.closest_waypoint_sequence_number, self.end_waypoint_sequence_number)
            if self.closest_waypoint_sequence_number - self.end_waypoint_sequence_number < 0:
                self.increment_sequence_number_to_follow_path = 1
                self.next_sequence_number = self.closest_waypoint_sequence_number + 1  # increment sequence number
                print("DEBUG: Part(4) increment:", self.next_sequence_number, self.closest_waypoint_sequence_number)
            else:
                self.increment_sequence_number_to_follow_path = 0
                self.next_sequence_number = self.closest_waypoint_sequence_number - 1  # decrement sequence number
                print("DEBUG: Part(4) decrement:", self.next_sequence_number, self.closest_waypoint_sequence_number)

            # (5) navigate to next point
            while True:
                # read matrix for next waypoint information
                self.next_waypoint_sequence_number = int(self.map_matrix[self.next_sequence_number][0])
                self.next_waypoint = self.map_matrix[self.next_sequence_number][1]
                self.next_coordinate_x = self.map_matrix[self.next_sequence_number][2]
                self.next_coordinate_y = self.map_matrix[self.next_sequence_number][3]
                print("DEBUG: Next Waypoint Info:", self.next_waypoint_sequence_number, self.next_waypoint,
                      self.next_coordinate_x, self.next_coordinate_y)

                # move to next waypoint
                print("Moving to next waypoint:", self.next_waypoint, "Sequence Number:",
                      self.next_waypoint_sequence_number)
                self.navigate_point2point(self.next_coordinate_x, self.next_coordinate_y, gps_correction_list)
                print("Arrived at Waypoint:", self.next_waypoint, "Sequence Number:",
                      self.next_waypoint_sequence_number)

                # (6) arrived at end_waypoint?  If yes, quit() or break
                # Stop if reached end waypoint!
                if self.next_waypoint_sequence_number == self.end_waypoint_sequence_number:
                    print("Robot has moved to the End Waypoint and will Quit() program!!")
                    self.traverse_running_time_seconds = time() - self.traverse_start_time  # calculate number of hours from start
                    self.traverse_running_time_minutes = int((self.traverse_running_time_seconds / 60))
                    self.traverse_running_time_seconds = int(
                        ((self.traverse_running_time_seconds / 60) - self.traverse_running_time_minutes) * 60)
                    print("Total Map_Traverse time:", self.traverse_running_time_minutes, "Minutes,",
                          self.traverse_running_time_seconds, "Seconds.")
                    if self.skipped_first_waypoint_flag == 1:
                        print(">>>Skipped initial Waypoint:", self.closest_waypoint, "since it was less than .25M distant:", self.closest_distance)
                    quit()

                # (6a) (4.27.23) ERROR Condition: Arrived at map beginning (waypoint0) or end (waypoint-max#) without detecting end_waypoint.
                if self.next_waypoint_sequence_number == 0 or self.next_waypoint_sequence_number == self.map_matrix[self.map_file_row_count][0]:
                    print("****Error***")
                    print("Robot has reached the end or beginning of the map but NEVER detected the target Waypoint")
                    # stop motors
                    print("Recursive Motor Stop:")
                    self.recursiveStopMotors()  # Send rapid 5 stop motor commands
                    quit()

                # (7) increment or decrement sequence number and loop back to (5)
                if self.increment_sequence_number_to_follow_path == 1:
                    self.next_sequence_number = self.next_sequence_number + 1
                else:  # decrement sequence number
                    self.next_sequence_number = self.next_sequence_number - 1

        except KeyboardInterrupt:  # exit program when keyboard interrupt
            print("cytron.map_traverse.py exception detected")
            print("about to execute QUIT")
            quit()

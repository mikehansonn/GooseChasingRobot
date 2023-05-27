import math


def calculate_bearing(robot_latitude, robot_longitude, target_latitude, target_longitude):
    d_longitude = target_longitude - robot_longitude
    y = math.sin(math.radians(d_longitude)) * math.cos(math.radians(target_latitude))
    x = math.cos(math.radians(robot_latitude)) * math.sin(math.radians(target_latitude)) - math.sin(
        math.radians(robot_latitude)) * math.cos(math.radians(target_latitude)) * math.cos(math.radians(d_longitude))
    bearing = math.degrees(math.atan2(y, x))
    return (bearing + 360) % 360


def turn_towards_target(robot_bearing, target_bearing):
    turn_angle = target_bearing - robot_bearing
    if turn_angle > 180:
        turn_angle -= 360
    elif turn_angle < -180:
        turn_angle += 360
    return turn_angle


# Example usage
robot_latitude = 1  # Robot's current latitude
robot_longitude = 1  # Robot's current longitude
target_latitude = 0  # Target point latitude
target_longitude = 0  # Target point longitude

robot_bearing = calculate_bearing(robot_latitude, robot_longitude, target_latitude, target_longitude)

robot_direction = 90

turn_angle = turn_towards_target(robot_direction, robot_bearing)
print(f"Turn the robot by {turn_angle} degrees")


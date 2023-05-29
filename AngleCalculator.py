# Angle Calculator

import math

fromX = 0
fromY = 0

toX = 1
toY = 2

slope = math.atan2((toY - fromY), (toX - fromX))


slope = (slope * 180)/math.pi

if slope < 0:
    slope = slope + 360

print(slope)


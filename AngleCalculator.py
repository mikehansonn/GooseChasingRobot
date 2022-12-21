# Angle Calculator

import math

fromX = 41.6253675
fromY = 73.78445971

toX = 41.6253787075
toY = 73.784457625

slope = math.atan2((toY - fromY), (toX - fromX))


slope = (slope * 180)/math.pi

if slope < 0:
    slope = slope + 360

print(slope)


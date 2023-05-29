def is_within_range(angle1, angle2, range_deg):
    # Calculate the absolute difference between the angles
    diff = abs(angle1 - angle2)
    
    # Handle the wraparound case
    if diff > 180:
        diff = 360 - diff
    
    print(diff)
    if diff <= range_deg:
        return True
    else:
        return False

# Example usage
angle1 = 270  # First angle in degrees
angle2 = 1  # Second angle in degrees
range_deg = 15  # Range in degrees

if is_within_range(angle1, angle2, range_deg):
    print("The angles are within the desired range.")
else:
    print("The angles are not within the desired range.")

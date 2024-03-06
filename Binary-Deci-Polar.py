import math
import time

# Define the outer boundary and inner boundary of the dartboard
OUTER_BOUNDARY = 72
INNER_BOUNDARY = OUTER_BOUNDARY * 0.6

# Define the segments and their corresponding radial ranges, angular ranges, and points
SEGMENTS = {
    6: ((INNER_BOUNDARY, OUTER_BOUNDARY), (345, 15), 6),
    13: ((INNER_BOUNDARY, OUTER_BOUNDARY), (15, 45), 13),
    4: ((INNER_BOUNDARY, OUTER_BOUNDARY), (45, 75), 4),
    18: ((INNER_BOUNDARY, OUTER_BOUNDARY), (75, 105), 18),
    1: ((INNER_BOUNDARY, OUTER_BOUNDARY), (105, 135), 1),
    20: ((INNER_BOUNDARY, OUTER_BOUNDARY), (135, 165), 20),
    5: ((INNER_BOUNDARY, OUTER_BOUNDARY), (165, 195), 5),
    12: ((INNER_BOUNDARY, OUTER_BOUNDARY), (195, 225), 12),
    9: ((INNER_BOUNDARY, OUTER_BOUNDARY), (225, 255), 9),
    14: ((INNER_BOUNDARY, OUTER_BOUNDARY), (255, 285), 14),
    11: ((INNER_BOUNDARY, OUTER_BOUNDARY), (285, 315), 11),
    8: ((INNER_BOUNDARY, OUTER_BOUNDARY), (315, 345), 8),
}

# Function to determine the segment number and points based on the given (r, θ) coordinates
def get_segment_and_points(r, theta):
    for segment, ((r_min, r_max), (theta_start, theta_end), points) in SEGMENTS.items():
        if r_min <= r <= r_max and theta_start <= theta < theta_end:
            return segment, points
    return 0, 0  # Default to 0 segment number and points if the coordinates are not within any segment

# Function to convert binary coordinates to decimal
def binary_to_decimal(binary):
    try:
        return int(binary, 2)
    except ValueError:
        return None  # Return None for invalid binary inputs

# Function to convert rectangular coordinates to polar coordinates
def rectangular_to_polar(x, y):
    r = math.hypot(x, y)
    theta = math.degrees(math.atan2(y, x))  # Returns the angle in degrees
    # Ensure theta is in the range [0, 360)
    theta = (theta + 360) % 360
    return r, theta

# Main function for continuous operation
def main():
    try:
        while True:
            # Prompt the user for binary X and Y coordinates
            x_binary = input("Enter binary X coordinate (000000 to 111111): ")
            y_binary = input("Enter binary Y coordinate (000000 to 111111): ")

            # Convert binary coordinates to decimal
            x_decimal = binary_to_decimal(x_binary)
            y_decimal = binary_to_decimal(y_binary)

            if x_decimal is None or y_decimal is None:
                print("Invalid binary input. Please enter a valid binary number.")
                continue

            # Convert decimal coordinates to polar coordinates
            r, theta = rectangular_to_polar(x_decimal, y_decimal)

            # Get segment and points based on (r, θ) coordinates
            segment, points = get_segment_and_points(r, theta)

            # Print the dart throw information
            print(f"Dart thrown at rectangular coordinates ({x_decimal}, {y_decimal}) and polar coordinates ({r:.2f}, {theta:.2f}) with segment {segment} and {points} points.")

            time.sleep(0.1)  # Delay before next dart throw
    except KeyboardInterrupt:
        print("\nExiting...")
        time.sleep(1)

if __name__ == "__main__":
    main()

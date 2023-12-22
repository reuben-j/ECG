from PIL import Image


def is_color_in_range(color, target_color, tolerance):
    """
    Check if a color is within a tolerance range of a target color.
    """
    for c, target_c in zip(color, target_color):
        if abs(c - target_c) > tolerance:
            return False
    return True

# Open the original image
original_image = Image.open("IMG_0791.jpeg")

width, height = original_image.size

# Load the pixel data
original_pixels = original_image.load()

# Target color range and tolerance
target_color_boxes = (226,229,236)
tolerance_boxes = 20

target_color_rhythm = (38, 41, 50)
tolerance_rhythm = 100
# Adjust the tolerance based on your requirements

# Create a new image with the same size as the original
new_image = Image.new("RGB", (width, height))
new_pixels = new_image.load()

# Iterate through each pixel in the original image
for y in range(height):
    for x in range(width):
        r, g, b = original_pixels[x, y]

        # Check if the pixel color is within the target color range
        if is_color_in_range((r, g, b), target_color_rhythm, tolerance_rhythm):
            new_pixels[x, y] = (255, 72, 0)
        elif is_color_in_range((r, g, b), target_color_boxes, tolerance_boxes):
            new_pixels[x, y] = (0, 0, 0)
            
# Save the new image
new_image.save("output_image_range_check.jpeg")

# Optionally, display the new image
new_image.show()



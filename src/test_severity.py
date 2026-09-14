from severity import calculate_severity

def yolo_to_pixel_box(
    normalized_width,
    normalized_height,
    image_width,
    image_height
):

    box_width = normalized_width * image_width
    box_height = normalized_height * image_height

    return box_width, box_height
# Test 1: Small longitudinal crack
score, level = calculate_severity(
    "D00",
    0.95,
    50,
    20,
    1000,
    1000
)

print("Test 1")
print("Severity Score:", score)
print("Severity Level:", level)
print()


# Test 2: Large alligator crack
score, level = calculate_severity(
    "D20",
    0.90,
    500,
    400,
    1000,
    1000
)

print("Test 2")
print("Severity Score:", score)
print("Severity Level:", level)
print()


# Test 3: Small pothole
score, level = calculate_severity(
    "D40",
    0.95,
    100,
    100,
    1000,
    1000
)

print("Test 3")
print("Severity Score:", score)
print("Severity Level:", level)
print()


# Test 4: Large pothole with lower confidence
score, level = calculate_severity(
    "D40",
    0.60,
    600,
    500,
    1000,
    1000
)

print("Test 4")
print("Severity Score:", score)
print("Severity Level:", level)


# YOLO bounding box conversion test

box_width, box_height = yolo_to_pixel_box(
    0.20,
    0.15,
    1000,
    1000
)

print()
print("YOLO Box Conversion Test")
print("Pixel Width:", box_width)
print("Pixel Height:", box_height)
from severity import calculate_severity, yolo_to_pixel_box
from gps import create_location


# --------------------------------
# 1. Simulate YOLO detection
# --------------------------------

damage_type = "D40"
confidence = 0.92

normalized_width = 0.20
normalized_height = 0.15

image_width = 1000
image_height = 1000


# --------------------------------
# 2. Convert YOLO box to pixels
# --------------------------------

box_width, box_height = yolo_to_pixel_box(
    normalized_width,
    normalized_height,
    image_width,
    image_height
)


# --------------------------------
# 3. Calculate severity
# --------------------------------

severity_score, severity_level = calculate_severity(
    damage_type,
    confidence,
    box_width,
    box_height,
    image_width,
    image_height
)


# --------------------------------
# 4. Get GPS location
# --------------------------------

location = create_location(
    20.2961,
    85.8245
)


# --------------------------------
# 5. Display complete record
# --------------------------------

print("================================")
print("ROAD DAMAGE DETECTION RECORD")
print("================================")

print("Damage Type:", damage_type)
print("Confidence:", confidence)

print("Bounding Box Width:", box_width)
print("Bounding Box Height:", box_height)

print("Severity Score:", severity_score)
print("Severity Level:", severity_level)

print("Latitude:", location["latitude"])
print("Longitude:", location["longitude"])
print("Timestamp:", location["timestamp"])
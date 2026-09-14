from severity import calculate_severity, yolo_to_pixel_box
from gps import create_location
from priority import calculate_priority


# ==========================================
# 1. SIMULATE YOLO DETECTION
# ==========================================

damage_type = "D40"
confidence = 0.92

normalized_width = 0.20
normalized_height = 0.15

image_width = 1000
image_height = 1000


# ==========================================
# 2. CONVERT YOLO BOX TO PIXELS
# ==========================================

box_width, box_height = yolo_to_pixel_box(
    normalized_width,
    normalized_height,
    image_width,
    image_height
)


# ==========================================
# 3. CALCULATE SEVERITY
# ==========================================

severity_score, severity_level = calculate_severity(
    damage_type,
    confidence,
    box_width,
    box_height,
    image_width,
    image_height
)


# ==========================================
# 4. GET GPS LOCATION
# ==========================================

location = create_location(
    20.2961,
    85.8245
)


# ==========================================
# 5. ROAD INFORMATION
# ==========================================

road_importance = 90
traffic_level = 80
location_risk = 60


# ==========================================
# 6. CALCULATE MAINTENANCE PRIORITY
# ==========================================

priority_score, priority_level = calculate_priority(
    severity_score,
    road_importance,
    traffic_level,
    location_risk
)


# ==========================================
# 7. DISPLAY COMPLETE RECORD
# ==========================================

print("========================================")
print("COMPLETE ROAD DAMAGE RECORD")
print("========================================")

print("Damage Type:", damage_type)
print("Confidence:", confidence)

print("Bounding Box Width:", box_width)
print("Bounding Box Height:", box_height)

print("Severity Score:", round(severity_score, 2))
print("Severity Level:", severity_level)

print("Latitude:", location["latitude"])
print("Longitude:", location["longitude"])
print("Timestamp:", location["timestamp"])

print("Road Importance:", road_importance)
print("Traffic Level:", traffic_level)
print("Location Risk:", location_risk)

print("Priority Score:", round(priority_score, 2))
print("Priority Level:", priority_level)

print("========================================")
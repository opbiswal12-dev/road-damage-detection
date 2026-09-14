# Severity estimation for road damage


# Base severity score for each damage type
DAMAGE_TYPE_SCORES = {
    "D00": 25,   # Longitudinal crack
    "D10": 35,   # Transverse crack
    "D20": 60,   # Alligator crack
    "D40": 65    # Pothole
}


def calculate_size_score(area_ratio):
    """
    Convert the percentage of the image occupied by
    damage into a size score from 0 to 100.
    """

    if area_ratio < 0.01:
        return 10

    elif area_ratio < 0.05:
        return 25

    elif area_ratio < 0.10:
        return 50

    elif area_ratio < 0.20:
        return 75

    else:
        return 100


def calculate_severity(
    damage_type,
    confidence,
    box_width,
    box_height,
    image_width,
    image_height
):
    """
    Calculate severity score and severity level.
    """

    # Check whether the damage type exists
    if damage_type not in DAMAGE_TYPE_SCORES:
        raise ValueError("Unknown damage type")

    # Calculate bounding-box area
    damage_area = box_width * box_height

    # Calculate complete image area
    image_area = image_width * image_height

    # Calculate how much of the image is occupied by damage
    area_ratio = damage_area / image_area

    # Get damage-type score
    type_score = DAMAGE_TYPE_SCORES[damage_type]

    # Calculate size score
    size_score = calculate_size_score(area_ratio)

    # Convert confidence from 0–1 to 0–100
    confidence_score = confidence * 100

    # Final severity formula
    severity_score = (
        0.40 * type_score
        + 0.40 * size_score
        + 0.20 * confidence_score
    )

    # Determine severity level
    if severity_score <= 25:
        severity_level = "LOW"

    elif severity_score <= 50:
        severity_level = "MEDIUM"

    elif severity_score <= 75:
        severity_level = "HIGH"

    else:
        severity_level = "CRITICAL"

    return severity_score, severity_level


# --------------------------------
# YOLO bounding box conversion
# --------------------------------

def yolo_to_pixel_box(
    normalized_width,
    normalized_height,
    image_width,
    image_height
):

    box_width = normalized_width * image_width
    box_height = normalized_height * image_height

    return box_width, box_height



# Test the severity function

score, level = calculate_severity(
    "D40",       # Pothole
    0.92,        # 92% confidence
    200,         # bounding box width
    150,         # bounding box height
    1000,        # image width
    1000         # image height
)

print("Severity Score:", score)
print("Severity Level:", level)



# Complete YOLO + Severity Test

damage_type = "D40"
confidence = 0.92

normalized_width = 0.20
normalized_height = 0.15

image_width = 1000
image_height = 1000


# Convert YOLO normalized values to pixels
box_width, box_height = yolo_to_pixel_box(
    normalized_width,
    normalized_height,
    image_width,
    image_height
)


# Calculate severity
score, level = calculate_severity(
    damage_type,
    confidence,
    box_width,
    box_height,
    image_width,
    image_height
)


print()
print("Complete YOLO + Severity Test")
print("Damage Type:", damage_type)
print("Confidence:", confidence)
print("Normalized Width:", normalized_width)
print("Normalized Height:", normalized_height)
print("Pixel Width:", box_width)
print("Pixel Height:", box_height)
print("Severity Score:", score)
print("Severity Level:", level)
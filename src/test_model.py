from ultralytics import YOLO
import os
from severity import calculate_severity
from priority import calculate_priority
from database import insert_damage_record
from gps import create_location

CLASS_TO_DAMAGE = {
    0: "D00",
    1: "D10",
    2: "D20",
    3: "D40"
}

# Load our trained road damage model
model = YOLO("models/best.pt")

# Find an image that has a damage label
images_path = "dataset/train/images"
labels_path = "dataset/train/labels"

image_path = None

for label_file in os.listdir(labels_path):

    label_full_path = os.path.join(labels_path, label_file)

    # Check whether the label file contains a damage annotation
    with open(label_full_path, "r") as file:
        content = file.read().strip()

    if content:
        image_name = os.path.splitext(label_file)[0]

        # Try common image extensions
        for extension in [".jpg", ".jpeg", ".png"]:

            possible_image = os.path.join(
                images_path,
                image_name + extension
            )

            if os.path.exists(possible_image):
                image_path = possible_image
                break

    if image_path:
        break


# Check if we found an image
if image_path is None:

    print("Could not find a labeled image.")

else:

    print("Testing image:")
    print(image_path)

    # Run YOLO detection
    results = model(image_path, conf=0.05)
    print("\nDetection Results:")

    for result in results:

        if len(result.boxes) == 0:

            print("No damage detected.")

        else:

            for box in result.boxes:

                



                class_id = int(box.cls[0])
                confidence = float(box.conf[0])

                print("Class ID:", class_id)
                print("Confidence:", round(confidence, 2))

                    # Get image dimensions
    image_height, image_width = result.orig_shape

    # Get bounding box coordinates
    x1, y1, x2, y2 = box.xyxy[0]

    # Calculate bounding box width and height
    box_width = float(x2 - x1)
    box_height = float(y2 - y1)

    print("Image width:", image_width)
    print("Image height:", image_height)
    print("Box width:", round(box_width, 2))
    print("Box height:", round(box_height, 2))

    damage_type = CLASS_TO_DAMAGE[class_id]

severity_score, severity_level = calculate_severity(
    damage_type,
    confidence,
    box_width,
    box_height,
    image_width,
    image_height
)

print("Damage Type:", damage_type)
print("Severity Score:", round(severity_score, 2))
print("Severity Level:", severity_level)

# Test values for road conditions
road_importance = 90
traffic_level = 80
location_risk = 60

# Calculate maintenance priority
priority_score, priority_level = calculate_priority(
    severity_score,
    road_importance,
    traffic_level,
    location_risk
)

print("Priority Score:", round(priority_score, 2))
print("Priority Level:", priority_level)

# Create GPS location
location = create_location(20.2961, 85.8245)

# Save detection in database
insert_damage_record(
    damage_type,
    confidence,
    severity_score,
    severity_level,
    location["latitude"],
    location["longitude"],
    location["timestamp"],
    road_importance,
    traffic_level,
    location_risk,
    priority_score,
    priority_level
)

print("Detection saved to database!")



# Save the prediction image with bounding boxes
for result in results:
    result.save(filename="prediction.jpg")

print("Prediction image saved as prediction.jpg")     
from ultralytics import YOLO

# Load our trained road damage model
model = YOLO("models/best.pt")

print("Road damage model loaded successfully!")

# Image we want to analyze
image_path = "dataset/train/images/China_Drone_000000.jpg"

# Run the image through the model
results = model(image_path)

print("Image analyzed successfully!")

# Get the first result
result = results[0]

# Check how many objects were detected
print("Number of detections:", len(result.boxes))

# Go through every detected damage
for box in result.boxes:

    # Get the class ID
    class_id = int(box.cls[0])

    # Get the confidence score
    confidence = float(box.conf[0])

    print("Class ID:", class_id)
    print("Confidence:", round(confidence, 2))

    # Get the bounding box coordinates
    x1, y1, x2, y2 = box.xyxy[0]

    # Calculate width and height in pixels
    box_width = float(x2 - x1)
    box_height = float(y2 - y1)

    print("Box width:", round(box_width, 2))
    print("Box height:", round(box_height, 2))    
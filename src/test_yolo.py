from ultralytics import YOLO


# Load pre-trained YOLO model
model = YOLO("yolo11n.pt")


# Road image from RDD2022 dataset
image_path = "dataset/train/images/China_Drone_000000.jpg"


# Run YOLO detection
results = model(image_path)


# Display results
for result in results:

    print("Detection Results:")

    if len(result.boxes) == 0:
        print("No objects detected.")

    else:
        for box in result.boxes:

            class_id = int(box.cls[0])
            confidence = float(box.conf[0])

            print("Class ID:", class_id)
            print("Confidence:", round(confidence, 2))
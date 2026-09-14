from ultralytics import YOLO


# Load the pre-trained YOLO11n model
model = YOLO("yolo11n.pt")


# Train the model on RDD2022
model.train(
    data="dataset/data.yaml",
    epochs=10,
    imgsz=640,
    batch=4,
    device="cpu",
    project="runs/detect",
    name="road_damage"
)
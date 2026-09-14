from ultralytics import YOLO


# Load the pre-trained YOLO model
model = YOLO("yolo11n.pt")


# Start a small training test
model.train(
    data="dataset/data.yaml",
    epochs=1,
    imgsz=320,
    batch=4,
    device="cpu"
)
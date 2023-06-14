from ultralytics import YOLO
model = YOLO("models/yolov8m.pt")
model.train(data='dataset.yaml', imgsz=518, batch=8, task='detect', device=0, epochs=20)
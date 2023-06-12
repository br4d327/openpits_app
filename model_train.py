from ultralytics import YOLO
model = YOLO("yolov8m.pt")
model.train(data='dataset.yaml', imgsz=518, batch=16, task='detect', device=0, epochs=20)
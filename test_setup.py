import cv2
import numpy as np
from ultralytics import YOLO

print("OpenCV version:", cv2.__version__)
print("NumPy version:", np.__version__)

model = YOLO("yolov8n.pt")
print("YOLO loaded successfully")
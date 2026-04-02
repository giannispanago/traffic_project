import cv2
from ultralytics import YOLO

model = YOLO("yolov8n.pt")

CONF_THRESHOLD = 0.50
video_path = "output/clips/clip_000.mp4"
cap = cv2.VideoCapture(video_path)

if not cap.isOpened():
    print("Δεν άνοιξε το clip")
    exit()

LINE_Y1 = 350
LINE_Y2 = 420

X1_TOP = 70
X2_TOP = 1110

X1_BOTTOM = 40
X2_BOTTOM = 1160

vehicle_classes = {"car", "truck", "bus", "motorcycle"}

while True:
    ret, frame = cap.read()
    if not ret:
        break

    results = model(frame, verbose=False)

    cv2.line(frame, (X1_TOP, LINE_Y1), (X2_TOP, LINE_Y1), (0, 255, 0), 4)
    cv2.line(frame, (X1_BOTTOM, LINE_Y2), (X2_BOTTOM, LINE_Y2), (0, 255, 0), 4)

    for result in results:
        for box in result.boxes:
            cls_id = int(box.cls[0].item())
            class_name = model.names[cls_id]

            if class_name not in vehicle_classes:
                continue

            x1, y1, x2, y2 = map(int, box.xyxy[0].tolist())
            conf = float(box.conf[0].item())

            if conf < CONF_THRESHOLD:
                continue

            label = f"{class_name} {conf:.2f}"

            cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
            cv2.putText(
                frame,
                label,
                (x1, max(30, y1 - 10)),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.5,
                (0, 255, 0),
                2
            )

    cv2.imshow("YOLO Detection with Lines", frame)

    if cv2.waitKey(25) & 0xFF == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()
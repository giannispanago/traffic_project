import cv2

video_path = "input/video.mp4"
cap = cv2.VideoCapture(video_path)

if not cap.isOpened():
    print("Δεν άνοιξε το βίντεο")
    exit()

fps = cap.get(cv2.CAP_PROP_FPS)
frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
duration_sec = frame_count / fps if fps > 0 else 0

print("FPS:", fps)
print("Frames:", frame_count)
print("Duration (sec):", round(duration_sec, 2))

while True:
    ret, frame = cap.read()
    if not ret:
        break

    cv2.imshow("Video", frame)

    if cv2.waitKey(25) & 0xFF == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()
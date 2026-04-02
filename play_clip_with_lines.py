import cv2

video_path = "output/clips/clip_000.mp4"
cap = cv2.VideoCapture(video_path)

if not cap.isOpened():
    print("Δεν άνοιξε το clip")
    exit()

LINE_Y1 = 335
LINE_Y2 = 430

X1_TOP = 70
X2_TOP = 1110

X1_BOTTOM = 40
X2_BOTTOM = 1160

while True:
    ret, frame = cap.read()
    if not ret:
        break

    cv2.line(frame, (X1_TOP, LINE_Y1), (X2_TOP, LINE_Y1), (0, 255, 0), 4)
    cv2.line(frame, (X1_BOTTOM, LINE_Y2), (X2_BOTTOM, LINE_Y2), (0, 255, 0), 4)

    cv2.imshow("Clip with reference lines", frame)

    if cv2.waitKey(25) & 0xFF == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()
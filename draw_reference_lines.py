import cv2

video_path = "output/clips/clip_000.mp4"
cap = cv2.VideoCapture(video_path)

if not cap.isOpened():
    print("Δεν άνοιξε το clip")
    exit()

ret, frame = cap.read()
cap.release()

if not ret:
    print("Δεν μπόρεσα να διαβάσω το πρώτο frame")
    exit()

height, width = frame.shape[:2]
print("Width:", width)
print("Height:", height)


LINE_Y1 = 335
LINE_Y2 = 430


X1_TOP = 90
X2_TOP = 1050

X1_BOTTOM = 60
X2_BOTTOM = 1070

cv2.line(frame, (X1_TOP, LINE_Y1), (X2_TOP, LINE_Y1), (0, 255, 0), 4)
cv2.line(frame, (X1_BOTTOM, LINE_Y2), (X2_BOTTOM, LINE_Y2), (0, 255, 0), 4)

cv2.imshow("Reference lines", frame)
cv2.waitKey(0)
cv2.destroyAllWindows()
exit()
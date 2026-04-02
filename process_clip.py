import cv2
import csv
import argparse
from pathlib import Path
from ultralytics import YOLO


LINE_Y1 = 350
LINE_Y2 = 420

X1_TOP = 70
X2_TOP = 1110

X1_BOTTOM = 40
X2_BOTTOM = 1160

CONF_THRESHOLD = 0.50
FPS = 25
DISTANCE_METERS = 17.0

MODEL_PATH = "yolov8n.pt"
TRACKER_CONFIG = "bytetrack.yaml"

VEHICLE_CLASSES = {"car", "truck", "bus", "motorcycle"}


def create_vehicle_record(class_name):
    return {
        "class_name": class_name,
        "line1_frame": None,
        "line2_frame": None,
        "crossing_frame": None,
        "time_sec": None,
        "window_5min": None,
        "direction": None,
        "speed_kmh": None
    }


def save_results(output_csv, vehicles):
    output_path = Path(output_csv)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    with open(output_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f, delimiter=";")
        writer.writerow([
            "track_id",
            "class_name",
            "line1_frame",
            "line2_frame",
            "crossing_frame",
            "time_sec",
            "window_5min",
            "direction",
            "speed_kmh"
        ])

        for track_id, data in vehicles.items():
            writer.writerow([
                track_id,
                data["class_name"],
                data["line1_frame"],
                data["line2_frame"],
                data["crossing_frame"],
                data["time_sec"],
                data["window_5min"],
                data["direction"],
                data["speed_kmh"]
            ])

    print(f"Saved results to {output_path}")


def process_clip(video_path, output_csv, clip_offset_sec=0, show=False):
    model = YOLO(MODEL_PATH)

    results = model.track(
        source=video_path,
        stream=True,
        persist=True,
        tracker=TRACKER_CONFIG,
        conf=CONF_THRESHOLD,
        verbose=False
    )

    display_ids = {}
    next_display_id = 1
    vehicles = {}
    frame_count = 0

    for result in results:
        frame_count += 1
        frame = result.orig_img.copy()

        if show:
            cv2.line(frame, (X1_TOP, LINE_Y1), (X2_TOP, LINE_Y1), (0, 255, 0), 4)
            cv2.line(frame, (X1_BOTTOM, LINE_Y2), (X2_BOTTOM, LINE_Y2), (0, 255, 0), 4)

        boxes = result.boxes

        if boxes is None or boxes.id is None:
            if show:
                cv2.imshow("Tracking + Crossing + Speed", frame)
                if cv2.waitKey(25) & 0xFF == ord("q"):
                    break
            continue

        track_ids = boxes.id.int().cpu().tolist()

        for box, track_id in zip(boxes, track_ids):
            cls_id = int(box.cls[0].item())
            class_name = model.names[cls_id]

            if class_name not in VEHICLE_CLASSES:
                continue

            x1, y1, x2, y2 = map(int, box.xyxy[0].tolist())
            conf = float(box.conf[0].item())

            if conf < CONF_THRESHOLD:
                continue

            if track_id not in display_ids:
                display_ids[track_id] = next_display_id
                next_display_id += 1

            display_id = display_ids[track_id]
            cx = int((x1 + x2) / 2)
            cy = int(y2 - 5)

            if track_id not in vehicles:
                vehicles[track_id] = create_vehicle_record(class_name)

            if (
                vehicles[track_id]["line1_frame"] is None
                and X1_TOP <= cx <= X2_TOP
                and abs(cy - LINE_Y1) <= 12
            ):
                vehicles[track_id]["line1_frame"] = frame_count
                print(f"Vehicle {display_id} crossed line 1 at frame {frame_count}")

            if (
                vehicles[track_id]["line2_frame"] is None
                and X1_BOTTOM <= cx <= X2_BOTTOM
                and abs(cy - LINE_Y2) <= 12
            ):
                vehicles[track_id]["line2_frame"] = frame_count
                print(f"Vehicle {display_id} crossed line 2 at frame {frame_count}")

            line1 = vehicles[track_id]["line1_frame"]
            line2 = vehicles[track_id]["line2_frame"]

            if line1 is not None and line2 is not None and vehicles[track_id]["speed_kmh"] is None:
                frame_diff = abs(line2 - line1)
                time_sec = frame_diff / FPS

                if time_sec > 0:
                    speed_mps = DISTANCE_METERS / time_sec
                    speed_kmh = int(round(speed_mps * 3.6))

                    if line1 < line2:
                        direction = "inbound"
                        crossing_frame = line2
                    else:
                        direction = "outbound"
                        crossing_frame = line1

                    local_crossing_time_sec = crossing_frame / FPS
                    global_crossing_time_sec = clip_offset_sec + local_crossing_time_sec
                    window_5min = int(global_crossing_time_sec // 300) + 1

                    vehicles[track_id]["speed_kmh"] = speed_kmh
                    vehicles[track_id]["direction"] = direction
                    vehicles[track_id]["crossing_frame"] = crossing_frame
                    vehicles[track_id]["time_sec"] = global_crossing_time_sec
                    vehicles[track_id]["window_5min"] = window_5min

                    print(
                        f"Vehicle {display_id} speed = {speed_kmh} km/h | "
                        f"{direction} | window {window_5min} | "
                        f"global_time {global_crossing_time_sec:.2f}s"
                    )

            if show:
                speed_text = ""
                if vehicles[track_id]["speed_kmh"] is not None:
                    speed_text = f" | {vehicles[track_id]['speed_kmh']} km/h"

                label = f"ID {display_id} | {class_name} | {conf:.2f}{speed_text}"

                cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
                cv2.circle(frame, (cx, cy), 4, (0, 0, 255), -1)
                cv2.putText(
                    frame,
                    label,
                    (x1, max(30, y1 - 10)),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.5,
                    (0, 255, 0),
                    2
                )

        if show:
            cv2.imshow("Tracking + Crossing + Speed", frame)
            if cv2.waitKey(25) & 0xFF == ord("q"):
                break

    if show:
        cv2.destroyAllWindows()

    save_results(output_csv, vehicles)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", required=True)
    parser.add_argument("--output", required=True)
    parser.add_argument("--clip-offset-sec", type=float, default=0)
    parser.add_argument("--show", action="store_true")
    args = parser.parse_args()

    process_clip(args.input, args.output, args.clip_offset_sec, args.show)


if __name__ == "__main__":
    main()
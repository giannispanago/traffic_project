import subprocess
import sys
from pathlib import Path


CLIPS_DIR = Path("output/clips")
RESULTS_DIR = Path("output/results")
PROCESS_SCRIPT = "process_clip.py"
CLIP_DURATION_SEC = 120


def get_clip_files():
    return sorted(
        f for f in CLIPS_DIR.glob("clip_*.mp4")
        if f.is_file()
    )


def process_all_clips():
    RESULTS_DIR.mkdir(parents=True, exist_ok=True)
    clip_files = get_clip_files()

    if not clip_files:
        print("Δεν βρέθηκαν clips.")
        raise SystemExit(1)

    print(f"Βρέθηκαν {len(clip_files)} clips.")

    for i, clip_file in enumerate(clip_files):
        output_csv = RESULTS_DIR / f"{clip_file.stem}_results.csv"
        clip_offset_sec = i * CLIP_DURATION_SEC

        cmd = [
            sys.executable,
            PROCESS_SCRIPT,
            "--input", str(clip_file),
            "--output", str(output_csv),
            "--clip-offset-sec", str(clip_offset_sec)
        ]

        print(f"Processing {clip_file.name}")
        result = subprocess.run(cmd)

        if result.returncode != 0:
            print(f"Failed processing {clip_file.name}")
            raise SystemExit(1)

    print("Ολοκληρώθηκε η επεξεργασία όλων των clips.")


def main():
    process_all_clips()


if __name__ == "__main__":
    main()
import subprocess
import sys
from pathlib import Path

CLIPS_DIR = Path("output/clips")
RESULTS_DIR = Path("output/results")
PROCESS_SCRIPT = "process_clip.py"



RESULTS_DIR.mkdir(parents=True, exist_ok=True)

clip_files = sorted(
    f for f in CLIPS_DIR.glob("clip_*.mp4")
    if f.is_file()
)

if not clip_files:
    print("Δεν βρέθηκαν clips στο output/clips")
    raise SystemExit(1)

print(f"Βρέθηκαν {len(clip_files)} clips.\n")

for clip_file in clip_files:
    output_csv = RESULTS_DIR / f"{clip_file.stem}_results.csv"

    cmd = [
        sys.executable,
        PROCESS_SCRIPT,
        "--input", str(clip_file),
        "--output", str(output_csv),
    ]

    print(f"Processing: {clip_file.name}")
    print("Command:", " ".join(cmd))

    result = subprocess.run(cmd)

    if result.returncode != 0:
        print(f"Αποτυχία στο {clip_file.name}")
        raise SystemExit(result.returncode)

    print(f"Saved: {output_csv.name}\n")

print("Ολοκληρώθηκε η επεξεργασία όλων των clips.")
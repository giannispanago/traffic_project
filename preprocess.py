import subprocess
import sys
from pathlib import Path
import os
import imageio_ffmpeg

CHUNK_SECONDS = 120
INPUT_VIDEO = "input/video.mp4"
OUTPUT_DIR = "output/clips"


def split_video_to_chunks(video_path, output_dir, chunk_seconds):
    os.makedirs(output_dir, exist_ok=True)

    ffmpeg_exe = imageio_ffmpeg.get_ffmpeg_exe()
    output_pattern = os.path.join(output_dir, "clip_%03d.mp4")

    command = [
        ffmpeg_exe,
        "-i", video_path,
        "-c", "copy",
        "-map", "0",
        "-f", "segment",
        "-segment_time", str(chunk_seconds),
        "-reset_timestamps", "1",
        output_pattern
    ]

    print("Running FFmpeg...")
    result = subprocess.run(command, capture_output=True, text=True)

    if result.returncode != 0:
        print(result.stderr)
        raise SystemExit(1)

    print("Chunking completed successfully.")


def main():
    split_video_to_chunks(INPUT_VIDEO, OUTPUT_DIR, CHUNK_SECONDS)


if __name__ == "__main__":
    main()
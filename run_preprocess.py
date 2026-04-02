from preprocess import split_video_to_chunks

video_path = "input/video.mp4"
output_dir = "output/clips"

split_video_to_chunks(video_path, output_dir, chunk_seconds=120)
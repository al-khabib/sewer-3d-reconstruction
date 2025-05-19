import cv2
import os

video_path = "sewer_walk.mp4"
output_folder = "frames"
os.makedirs(output_folder, exist_ok=True)

cap = cv2.VideoCapture(video_path)
frame_count = 0
success, frame = cap.read()

while success:
    cv2.imwrite(f"{output_folder}/frame_{frame_count:04d}.png", frame)
    success, frame = cap.read()
    frame_count += 1

cap.release()
print(f"Extracted {frame_count} frames.")




#Convert colmap output to NeRF format
#python colmap2nerf.py --images frames --colmap_output_path output --out transforms.json
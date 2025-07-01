import os
import cv2
import numpy as np
import argparse

def preprocess_frame(frame):
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    denoised = cv2.fastNlMeansDenoising(gray, h=10)
    clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
    enhanced = clahe.apply(denoised)
    gamma = 1.2
    lut = np.array([((i / 255.0) ** (1.0 / gamma)) * 255 for i in np.arange(256)]).astype("uint8")
    gamma_corrected = cv2.LUT(enhanced, lut)
    edges = cv2.Laplacian(gamma_corrected, cv2.CV_64F)
    return cv2.convertScaleAbs(edges)

def main(args):
    image_path = os.path.join(args.workspace_path, "images")
    db_path = os.path.join(args.workspace_path, "database.db")
    sparse_path = os.path.join(args.workspace_path, "sparse")
    dense_path = os.path.join(args.workspace_path, "dense")

    for p in [args.workspace_path, image_path, sparse_path, dense_path]:
        os.makedirs(p, exist_ok=True)

    cap = cv2.VideoCapture(args.video_path)
    fps = cap.get(cv2.CAP_PROP_FPS)
    start_frame = int(args.start_time * fps)
    end_frame = int(args.end_time * fps)

    cap.set(cv2.CAP_PROP_POS_FRAMES, start_frame)
    frame_num = start_frame

    while frame_num <= end_frame:
        ret, frame = cap.read()
        if not ret:
            break

        processed_frame = preprocess_frame(frame)
        frame_filename = os.path.join(image_path, f"frame_{frame_num:05d}.png")
        cv2.imwrite(frame_filename, processed_frame)

        frame_num += args.frame_interval
        cap.set(cv2.CAP_PROP_POS_FRAMES, frame_num)

    cap.release()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Video Frame Preprocessing Script")
    parser.add_argument('--workspace_path', type=str, required=True, help='Path to workspace directory')
    parser.add_argument('--video_path', type=str, required=True, help='Path to input video file')
    parser.add_argument('--mask_path', type=str, help='Path to mask image (optional)')
    parser.add_argument('--start_time', type=float, default=0.0, help='Start time in seconds')
    parser.add_argument('--end_time', type=float, default=20.0, help='End time in seconds')
    parser.add_argument('--frame_interval', type=int, default=5, help='Interval between frames to process')

    args = parser.parse_args()
    main(args)

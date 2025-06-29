import cv2
import numpy as np
import os

# PARAMETERS
VIDEO_PATH = "3D_reconstruction/200S0264.mp4"
OUTPUT_DIR = "video_4/keyframes"
MASK_PATH = "video_4/mask/mask.png"  # Optional
MIN_FEATURES = 1000 # Minimum number of features to consider a frame
MIN_MOVEMENT = 20
FRAME_SKIP = 5

os.makedirs(OUTPUT_DIR, exist_ok=True)

# Load mask if it exists
if os.path.exists(MASK_PATH):
    mask = cv2.imread(MASK_PATH, cv2.IMREAD_GRAYSCALE)
    if mask is None:
        raise ValueError(f"Mask at {MASK_PATH} could not be loaded.")
    mask = (mask > 128).astype(np.uint8) * 255
    print("Mask loaded and applied.")
else:
    mask = None
    print("No mask applied.")

# Init video and SIFT
cap = cv2.VideoCapture(VIDEO_PATH)
sift = cv2.SIFT_create()
bf = cv2.BFMatcher(cv2.NORM_L2, crossCheck=True)

frame_id = 0
keyframe_id = 0
last_kp, last_desc = None, None

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    if frame_id % FRAME_SKIP != 0:
        frame_id += 1
        continue

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    if mask is not None and mask.shape != gray.shape:
        raise ValueError("Mask and video frame must have the same resolution.")

    kp, desc = sift.detectAndCompute(gray, mask)

    if desc is None or len(kp) < MIN_FEATURES:
        frame_id += 1
        continue

    if last_kp is None:
        cv2.imwrite(f"{OUTPUT_DIR}/keyframe_{keyframe_id:04d}.jpg", frame)
        last_kp, last_desc = kp, desc
        keyframe_id += 1
    else:
        matches = bf.match(desc, last_desc)
        if len(matches) == 0:
            frame_id += 1
            continue

        movement = np.mean([
            np.linalg.norm(np.array(kp[m.queryIdx].pt) - np.array(last_kp[m.trainIdx].pt))
            for m in matches
        ])

        if movement > MIN_MOVEMENT:
            cv2.imwrite(f"{OUTPUT_DIR}/keyframe_{keyframe_id:04d}.jpg", frame)
            last_kp, last_desc = kp, desc
            keyframe_id += 1

    frame_id += 1

cap.release()
print(f"Saved {keyframe_id} keyframes to {OUTPUT_DIR}")

import cv2
import os

input_dir = os.path.expanduser('~/sewer_reconstruction/images')
output_dir = os.path.expanduser('~/sewer_reconstruction/images_masked')

os.makedirs(output_dir, exist_ok=True)

for filename in os.listdir(input_dir):
    if filename.lower().endswith((".jpg", ".jpeg", ".png")):
        input_path = os.path.join(input_dir, filename)
        output_path = os.path.join(output_dir, filename)

        img = cv2.imread(input_path)
        if img is None:
            print(f"Failed to load {filename}")
            continue

        h, w = img.shape[:2]

        img[0:int(0.125*h), 0:int(0.3*w)] = 0   # Top-left
        img[int(0.875*h):h, 0:int(0.3*w)] = 0   # Bottom-left
        img[int(0.875*h):h, int(0.7*w):w] = 0   # Bottom-right

        cv2.imwrite(output_path, img)
        print(f"Masked images saved: {filename}")
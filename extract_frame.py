import cv2
import os

def extract_every_frame(video_path, output_folder):
    """
    Extract every frame from a video and save them as individual image files.
    
    Args:
        video_path (str): Path to the input video file.
        output_folder (str): Directory to save extracted frames.
    """
    os.makedirs(output_folder, exist_ok=True)
    
    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        print("Error: Could not open video.")
        return

    frame_index = 0

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        # Save current frame
        frame_filename = os.path.join(output_folder, f"frame_{frame_index:05d}.png")
        cv2.imwrite(frame_filename, frame)
        print(f"Extracted frame is saved to: {frame_filename}")
        frame_index += 1

    cap.release()
    print(f"✅ Done! Extracted {frame_index} frames to: {output_folder}")

# Example usage
extract_every_frame('data/10IHSW05_10IHSW5A.mp4', 'data/extracted_frames/10IHSW05_10IHSW5A')
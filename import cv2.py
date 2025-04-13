import cv2
import numpy as np
import matplotlib.pyplot as plt

# === CONFIGURATION ===
video_path = "C:/Users/wwwke/Downloads/40LP265.mp4"  # Replace with your video path
output_file = "C:/Users/wwwke/Downloads/Results.txt"  # Output file path

# === LOAD VIDEO ===
cap = cv2.VideoCapture(video_path)
if not cap.isOpened():
    raise Exception("❌ Cannot open video")

frame_rate = cap.get(cv2.CAP_PROP_FPS)
frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
duration = frame_count / frame_rate
resolution = f"{width}x{height}"

# === SAMPLE FRAMES FOR ANALYSIS ===
sample_indices = np.linspace(0, frame_count - 1, 5, dtype=int)
frames = []
for idx in sample_indices:
    cap.set(cv2.CAP_PROP_POS_FRAMES, idx)
    ret, frame = cap.read()
    if ret:
        frames.append((idx, frame))

# === METRIC FUNCTIONS ===
def estimate_brightness_contrast(frame):
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    return np.mean(gray), np.std(gray)

def estimate_sharpness(frame):
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    return cv2.Laplacian(gray, cv2.CV_64F).var()

def calculate_entropy(frame):
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    hist = cv2.calcHist([gray], [0], None, [256], [0, 256])
    hist /= hist.sum()
    # Fix: Use np.fromiter to convert the generator to an array before summing
    return -np.sum(np.fromiter((p * np.log2(p) for p in hist if p > 0), dtype=float))

def plot_histogram(frame):
    plt.figure(figsize=(10, 4))
    for i, col in enumerate(('b', 'g', 'r')):
        hist = cv2.calcHist([frame], [i], None, [256], [0, 256])
        plt.plot(hist, color=col)
    plt.title("Color Histogram")
    plt.xlabel("Pixel Intensity")
    plt.ylabel("Frequency")
    plt.grid()
    plt.tight_layout()
    plt.show()

# === OPEN FILE TO WRITE RESULTS WITH UTF-8 ENCODING ===
with open(output_file, "w", encoding="utf-8") as file:
    # Writing configuration
    file.write(f"🎥 Frame rate: {frame_rate:.2f} FPS\n")
    file.write(f"🖼️ Resolution: {resolution}\n")
    file.write(f"🎞️ Total frames: {frame_count}\n")
    file.write(f"⏱️ Duration: {duration:.2f} seconds\n\n")
    
    # === ANALYZE SAMPLE FRAME ===
    sample_idx, sample_frame = frames[0]
    brightness, contrast = estimate_brightness_contrast(sample_frame)
    sharpness = estimate_sharpness(sample_frame)
    texture = calculate_entropy(sample_frame)

    # Fix: Ensure texture is a scalar value for formatting
    texture = float(texture)

    file.write(f"📊 Frame Analysis (index: {sample_idx})\n")
    file.write(f"🔆 Brightness: {brightness:.2f}\n")
    file.write(f"🌗 Contrast: {contrast:.2f}\n")
    file.write(f"📏 Sharpness (Laplacian var): {sharpness:.2f}\n")
    file.write(f"🧵 Texture richness (entropy): {texture:.2f}\n\n")

    # === CHECK FOR MISSING/CORRUPT FRAMES ===
    file.write("🔎 Checking for corrupt/missing frames...\n")
    missing_frames = []
    for i in range(0, frame_count, int(frame_rate * 10)):
        cap.set(cv2.CAP_PROP_POS_FRAMES, i)
        ret, _ = cap.read()
        if not ret:
            missing_frames.append(i)

    cap.release()

    if missing_frames:
        file.write(f"⚠️ Missing/corrupt frames found at: {missing_frames}\n")
    else:
        file.write("✅ No corrupt frames detected in 10s intervals.\n")
    
    file.write("\n=== END OF REPORT ===")

print(f"📋 Results saved to {output_file}")
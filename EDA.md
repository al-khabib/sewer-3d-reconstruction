## Video `2380579a-c4b7-4feb-a48b-6d6c3f6bd615.mpg`
[Link to the notebook with EDA](https://colab.research.google.com/drive/1Tj9hjJVhdz6N5SaAJEAjKE3Qpmr7wIiT?usp=sharing)

Section `DataFrame with some metadata` produces `sewer_video_metadata.csv` & uses `easyocr` to extract the following info from the frames:
- frame's number
- timestamp
- FZ (Focal zone)
- LZ1 (Covered distance)
- Velocity

Section `Brightness & Sharpness` produces `brightness_sharpness.csv` with the following features:
- frame's number
- timestamp
- mean brightness
- [perceived luminance](https://en.wikipedia.org/wiki/Relative_luminance)
- [sharpness](https://medium.com/@sagardhungel/laplacian-and-its-use-in-blur-detection-fbac689f0f88)
- normalized sharpness

# 3D Sewer Pipeline Reconstruction using NeRFmm

### Overview

This is the pipeline process for 3D reconstruction of a sewer pipeline using the **NeRFmm** model, which is a variant of Neural Radiance Fields (NeRF).  
There are two options for training the model depending on your workflow:

1. **Quick testing using the NeRFmm Colab notebook**  
2. **Full training using the official NeRFmm GitHub repository**

---

### Option 1: Using `nerfmm_pipeline.ipynb`

This approach is suitable for quick testing. The notebook handles preprocessing, training, and postprocessing in a streamlined pipeline.

To use it:

- Run `nerfmm_pipeline.ipynb` along with the image path.
- The notebook will generate a `.ply` point cloud file.
- You can then construct the 3D surface using the `surface_construction.ipynb` notebook, providing the generated point cloud as input.

---

### Option 2: Using the NeRFmm GitHub Repository

#### Installation

1. Clone the NeRFmm repository and create a Conda environment:

```bash
git clone https://github.com/ActiveVisionLab/nerfmm.git
cd nerfmm
conda env create -f environment.yml
```

Or follow the official installation guide:  
https://github.com/ActiveVisionLab/nerfmm

---

#### Dataset Preparation

No manual dataset preparation is required. NeRFmm learns both **intrinsic** and **extrinsic** camera parameters during training, which makes it suitable for uncalibrated image sets.

---

#### Model Training

Train the model using the following command:

```bash
python tasks/any_folder/train.py --base_dir={Path_to_the_image_folder} --scene_name={image_folder_name}
```

Replace `{Path_to_the_image_folder}` with the full path to your images, and `{image_folder_name}` with the name of your dataset folder.

---

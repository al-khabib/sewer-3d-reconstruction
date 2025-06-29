# 3D Sewer Pipeline Reconstruction using Nerfacto (NeRFstudio)

### Overview

This is the pipeline process for 3D reconstruction of a sewer pipeline using the **Nerfacto** model from **NeRFstudio**.

---

### Installation

Create a conda environment and install necessary libraries:

```bash
conda env create -f nerfstudio_environment.yml
conda activate nerfstudio
```

Alternatively, you can follow the Nerfstudio official installation guide:  
https://docs.nerf.studio/quickstart/installation.html

---

### Dataset Preparation

1. Prepare the dataset from scratch using Nerfstudio's default processing pipeline:

```bash
ns-process-data {images, video} --data {DATA_PATH} --output-dir {PROCESSED_DATA_DIR}
```

After dataset preprocessing, a file named `sparse_pc.ply` will be available in the output directory.  
You can use the **`surface_construction.ipynb`** for surface construction.

---

### Model Training

Train the model with the following command:

```bash
ns-train nerfacto --pipeline.model.predict-normals True
```

---

### Model Exporting

During training, you can monitor progress using the local GUI at:  
`http://127.0.0.1:7007`

Use the following commands to export the results:

**Export Point Cloud:**

```bash
ns-export pointcloud --load-config {CONFIG.yml} --output-dir {OUTPUT_DIR} --num-points 1000000 --remove-outliers True --normal-method open3d --save-world-frame False
```

**Export Mesh (Poisson Reconstruction):**

```bash
ns-export poisson --load-config {CONFIG.yml} --output-dir {OUTPUT_DIR} --target-num-faces 50000 --num-pixels-per-side 2048 --num-points 1000000 --remove-outliers True --normal-method open3d
```

---

### Surface Construction

After exporting the point cloud, run `surface_construction.ipynb` with the appropriate point cloud directory.  
This notebook will generate the final 3D surface reconstruction result.

- To include **color** information, you can export as `.mtl` format for mesh construction.
- To view the mesh in third-party apps (e.g., CloudCompare), `.obj` format is recommended for compatibility.

---

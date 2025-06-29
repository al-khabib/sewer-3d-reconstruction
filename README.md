# SfM Experimental Branch

This branch contains exploratory notebooks and scripts for testing Structure-from-Motion (SfM) pipelines for 3D reconstruction of sewer systems from inspection videos. It includes exploratory data analysis, various preprocessing methods, feature extraction, sparse and dense reconstruction techniques, and visualizations.

## Files:

* **EDA.ipynb:** Computes and visualizes frame-wise metrics (brightness, sharpness, noise, contrast, entropy, motion) to identify problematic frames.

* **EDA\_and\_SIFT.ipynb:** Extracts visual metrics, samples frames, and tests sparse 3D reconstruction with SIFT features, fundamental matrix estimation, triangulation, and sparse point cloud visualization.

* **Preprocessing\_Sparse\_Reconstruction\_Experiments.ipynb:** Performs manual and COLMAP-based sparse 3D reconstruction, preprocessing experiments, camera pose estimation, and point cloud visualization.

* **Sparse\_Reconstruction.ipynb:** Demonstrates running COLMAP sparse reconstruction on a video segment in Google Colab. It includes frame preprocessing, feature extraction using SIFT, and sparse reconstruction steps.

* **colmap\_script.sh:** Automates COLMAP 3D reconstruction pipeline (feature extraction, sparse/dense reconstruction, depth fusion, Poisson meshing).

* **extract\_keyframes.py:** Extracts keyframes from video based on SIFT features and visual change (motion), with optional masking.

* **main\_steps\_colmap.ipynb:** Step-by-step COLMAP pipeline covering feature extraction, matching, sparse/dense reconstruction, stereo fusion, and Poisson meshing for sewer scenes.

* **masking.py:** Applies a mask to images, removing irrelevant corner areas before reconstruction.

* **openSfm\_tryout.ipynb:** Installs and configures OpenSfM in Colab for experimental reconstruction.

* **sfm.ipynb:** Demonstrates basic SfM pipeline: frame extraction, SIFT feature detection, matching, and visualization.

* **sfm\_colmap.ipynb:** Implements COLMAP-based SfM pipeline in Colab, including frame extraction, sparse reconstruction, and point cloud export.

* **sfm\_first\_steps.ipynb:** Basic SfM pipeline including masking, SIFT feature matching, essential-matrix camera pose estimation, triangulation, and point cloud visualization.

* sfm\_openMVG.ipynb: Sets up OpenMVG-based SfM pipeline within Colab.

## Data Folder:

Contains visualizations for SfM notebooks.

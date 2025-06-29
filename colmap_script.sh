#!/bin/bash

# CHECK INPUT
if [ $# -lt 1 ]; then
    echo "Usage: $0 <image_folder> [project_name]"
    exit 1
fi

IMAGE_FOLDER="$1"
PROJECT_NAME="${2:-colmap_project}"  # Optional second argument, defaults to "colmap_project"

# AUTOMATIC PATHS
DB_PATH="${PROJECT_NAME}/database.db"
SPARSE_PATH="${PROJECT_NAME}/sparse"
DENSE_PATH="${PROJECT_NAME}/dense"
IMAGE_PATH="${PROJECT_NAME}/images"
MODEL_PATH="${SPARSE_PATH}/0"

# CREATE PROJECT STRUCTURE
echo "[1/9] Setting up project structure..."
mkdir -p "$PROJECT_NAME"
cp -r "$IMAGE_FOLDER" "$IMAGE_PATH"

# FEATURE EXTRACTION
echo "[2/9] Extracting features..."
colmap feature_extractor \
    --database_path "$DB_PATH" \
    --image_path "$IMAGE_PATH" \
    --ImageReader.single_camera 1

# EXHAUSTIVE MATCHING
echo "[3/9] Matching features..."
colmap exhaustive_matcher \
    --database_path "$DB_PATH" \
    --SiftMatching.use_gpu 1

# SPARSE RECONSTRUCTION
echo "[4/9] Running sparse mapping..."
colmap mapper \
    --database_path "$DB_PATH" \
    --image_path "$IMAGE_PATH" \
    --output_path "$SPARSE_PATH" \
    --Mapper.num_threads 8

# IMAGE UNDISTORTION
echo "[5/9] Undistorting images..."
colmap image_undistorter \
    --image_path "$IMAGE_PATH" \
    --input_path "$MODEL_PATH" \
    --output_path "$DENSE_PATH" \
    --output_type COLMAP

# DENSE: PATCH MATCH STEREO
echo "[6/9] Estimating depth maps..."
colmap patch_match_stereo \
    --workspace_path "$DENSE_PATH" \
    --workspace_format COLMAP \
    --PatchMatchStereo.geom_consistency true

# DENSE: FUSION
echo "[7/9] Fusing depth maps..."
colmap stereo_fusion \
    --workspace_path "$DENSE_PATH" \
    --workspace_format COLMAP \
    --input_type geometric \
    --output_path "$DENSE_PATH/fused.ply"

# DENSE: POISSON MESH
echo "[8/9] Generating mesh..."
colmap poisson_mesher \
    --input_path "$DENSE_PATH/fused.ply" \
    --output_path "$DENSE_PATH/poisson_mesh.ply"

# DONE
echo "[9/9] Reconstruction complete. Project saved in '$PROJECT_NAME'"

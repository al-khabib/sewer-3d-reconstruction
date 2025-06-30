#!/bin/bash

# Default paths
default_images_path="/workspace/images"
default_output_path="/workspace/output"

# OpenMVG binary path
OPENMVG_SFM_BIN="/home/dll1004/sewer_reconstruction/openMVG_workspace/openMVG_Build/Linux-x86_64-Release"

# Input parameters with fallback to defaults
IMAGES_PATH="${1:-$default_images_path}"
OUTPUT_PATH="${2:-$default_output_path}"
MATCHES_PATH="$OUTPUT_PATH/matches"
RECONSTRUCTION_PATH="$OUTPUT_PATH/reconstruction_sequential"

# Create required directories
mkdir -p "$MATCHES_PATH"
mkdir -p "$RECONSTRUCTION_PATH"
mkdir -p "$OUTPUT_PATH/openMVS"

echo "Images: $IMAGES_PATH"
echo "Output: $OUTPUT_PATH"

# Step 1: Image Listing
$OPENMVG_SFM_BIN/openMVG_main_SfMInit_ImageListing \
    -i "$IMAGES_PATH" \
    -o "$MATCHES_PATH" \
    -f 2300 \
    -c 3

# Step 2: Feature Extraction
$OPENMVG_SFM_BIN/openMVG_main_ComputeFeatures \
    -i "$MATCHES_PATH/sfm_data.json" \
    -o "$MATCHES_PATH" \
    -m SIFT \
    -f 1

# Step 3: Feature Matching
$OPENMVG_SFM_BIN/openMVG_main_ComputeMatches \
    -i "$MATCHES_PATH/sfm_data.json" \
    -o "$MATCHES_PATH/matches.putative.bin" \
    -f 1 \
    -n AUTO

# Step 4: Geometric Filtering
$OPENMVG_SFM_BIN/openMVG_main_GeometricFilter \
    -i "$MATCHES_PATH/sfm_data.json" \
    -m "$MATCHES_PATH/matches.putative.bin" \
    -g f \
    -o "$MATCHES_PATH/matches.f.bin"

# Step 5: SfM Reconstruction
$OPENMVG_SFM_BIN/openMVG_main_SfM \
    --sfm_engine INCREMENTAL \
    --input_file "$MATCHES_PATH/sfm_data.json" \
    --match_dir "$MATCHES_PATH" \
    --output_dir "$RECONSTRUCTION_PATH"

# Step 6: Colorize Point Cloud
$OPENMVG_SFM_BIN/openMVG_main_ComputeSfM_DataColor \
    -i "$RECONSTRUCTION_PATH/sfm_data.bin" \
    -o "$RECONSTRUCTION_PATH/colorized.ply"

# Step 7: Structure from Known Poses
$OPENMVG_SFM_BIN/openMVG_main_ComputeStructureFromKnownPoses \
    -i "$RECONSTRUCTION_PATH/sfm_data.bin" \
    -m "$MATCHES_PATH" \
    -o "$RECONSTRUCTION_PATH/robust.ply"

# Step 8: Convert to openMVS
$OPENMVG_SFM_BIN/openMVG_main_openMVG2openMVS \
    -i "$RECONSTRUCTION_PATH/sfm_data.bin" \
    -o "$OUTPUT_PATH/openMVS/scene.mvs" \
    -d "$IMAGES_PATH"

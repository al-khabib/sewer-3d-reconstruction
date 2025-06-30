# Instant neural graphics primitives for sewer pipes reconstruction

## Useful links
- [Paper](https://arxiv.org/abs/2201.05989)
- [GitHub repo](https://github.com/NVlabs/instant-ngp)

## Intro
We would like to present 2 methods of how you can use Instant NGP for 3D reconstruction of the sewer systems. In short, the first one requires the minimum number of actions and possesses a limited flexibility, whereas the second one comes with a necessity to work in your terminal but is rather flexible.

## Prerequisites 
Both methods require the following:
- [Python](https://www.python.org/)
- [FFmpeg](https://ffmpeg.org/download.html)
- [COLMAP](https://colmap.github.io/install.html)
- [Instant NGP](https://github.com/NVlabs/instant-ngp) - there is an **Installation** section in `README` for various GPUs

## Reconstruction examples
Check `reconstruction_examples/` in this directory to see our reconstruction. Note that we have done some preprocessing including converting to greyscale. So far this is the most stable reconstruction.

## Preprocessing
It's up to you but we recommend working on the blur of the videos to improve the final results. It's possible to skip this step, although it affects the output (not critically).

You can check our blur analysis in `EDA/Blur_Analysis_Mitigation.ipynb`. You can also find the very first EDA we did in `EDA/EDA_3D_reconstruction.ipynb`

## Method 1 (the simple one)
1) Download `colmap2nerf.py` file from the Instant NGP repo in `scripts/`

2) Place the downloaded script to the folder containing your video

3) Navigate to this folder and run `python colmap2nerf.py --video_in your_video_file --video_fps your_desired_fps --run_colmap --aabb_scale 16` - Don't forget to set your video's name and fps

You will need to give a few permissions to run COLMAP. Eventually, you'll have `images/` with extracted frames & `transforms.json` - they are exactly what you need to start training the model.

You can train the model locally, but we'll show how to do it remotely:

4) Open [the authors' notebook](https://github.com/NVlabs/instant-ngp/blob/master/notebooks/instant_ngp.ipynb) in [Google Colab](https://colab.google/)

5) Set the GPU Runtime by *Runtime Tab* -> *Change Runtime* -> *T4 GPU*

6) Set `compute_capability = 75` in section **3. Set compute capability**

7) Specify the folder path with the uploaded `images/` & `transforms.json` in `scene_path` variable, **8. Train a model on your scene**. Note that you have to upload your scene file in advance to your Drive.

8) Run all sections except for the 9th one.

You will see `2000.ingp` in your Drive folder with `images/` & `transforms.json` if everything went well. Download this file.

9) Navigate to the folder containing Instant NGP that you downloaded from [Prerequisites](#prerequisites)

10) Run `.\instant-ngp.exe "full_path_to_ingp_file_folder/2000.ingp" --no-train`

That will load the Instant NGP app with your reconstruction.

## Method 2 (the flexible one)

The commands below work with the video called `extracted_30s.mp4` - change the name to your video before running them.

Feel free to read the [FFmpeg](https://ffmpeg.org/ffmpeg.html) & [COLMAP](https://colmap.github.io/cli.html) docs, as we believe there might be even a better parameters' configuration.

1) Start a video preprocessing step by running this in your terminal
```bash
ffmpeg -i ../extracted_30s.mp4 \
  -vf "unsharp=5:5:1.0:5:5:0.0,eq=contrast=1.2:brightness=0.05" \
  -c:v libx264 -crf 18 \
  preprocessed_video.mp4
```

2) Extract the frames by running this in the terminal
```bash
mkdir images

ffmpeg -i preprocessed_video.mp4 -r 9 -q:v 1 images/frame_%04d.jpg
```
Here we extracted frames at 9 FPS - you might want to change this.

3) Run custom-set COLMAP feature extraction
```bash
colmap feature_extractor \
    --database_path pipe_reconstruction.db \
    --image_path images \
    --ImageReader.camera_model OPENCV \
    --ImageReader.single_camera 1 \
    --SiftExtraction.domain_size_pooling 1 \
    --SiftExtraction.estimate_affine_shape 1 \
    --SiftExtraction.peak_threshold 0.004 \
    --SiftExtraction.edge_threshold 5 \
    --SiftExtraction.max_num_features 16384 \
    --SiftExtraction.octave_resolution 4
```

4) Run custom-set sequential matcher
```bash
colmap sequential_matcher \
    --database_path pipe_reconstruction.db \
    --SequentialMatching.overlap 15 \
    --SequentialMatching.loop_detection 1 \
    --SiftMatching.guided_matching 1 \
    --SiftMatching.max_ratio 0.75 \
    --SiftMatching.cross_check 1 \
    --SiftMatching.max_distance 0.65
```

5) Create sparse reconstruction
```bash
mkdir sparse

colmap mapper \
    --database_path pipe_reconstruction.db \
    --image_path images \
    --output_path sparse \
    --Mapper.tri_min_angle 1.0 \
    --Mapper.tri_ignore_two_view_tracks 0 \
    --Mapper.tri_complete_max_reproj_error 3 \
    --Mapper.ba_global_images_freq 250
```

6) Convert binary COLMAP output to text format
```bash
colmap model_converter --input_path sparse/0 --output_path sparse/0 --output_type TXT
```
This will create the required `cameras.txt`, `images.txt`, `points3D.txt` files.

7) Convert your prelimanary outputs to Instant NGP format
```bash
python your_path_to_colmap2nerf_file\colmap2nerf.py \
    --images images --text sparse/0 \
    --aabb_scale 64 \
    --keep_colmap_coords \
    --out pipe_ngp_dataset
```

8) Rename `pipe_ngp_dataset` to `transforms.json`. You will need to use this file & `images/` to train the model.

9) Continue with `transforms.json` & `images/` as in [4) in Method 1 (the simple one)](#method-1-the-simple-one)

## ADDITIONAL METHOD (DEMO PURPOSES 3*)
Although this approach does not deal with inspection videos, it focuses on understanding the potential of InstantNGP in similar scenarios. It will be executed using self-collected data which additional (not available in provided videos) features and benefits. We wHill utilize ARKit-Based Precision using Record3D which provides superior data quality foundation. Record3D offers an alternative approach that leverages Apple's ARKit technology for camera pose estimation, potentially providing more robust tracking in challenging environments.

Additional Prerequisites:
- iPhone 12 Pro or newer with LiDAR capability
- Record3D app installed on iPhone
- All standard prerequisites from Methods 1 and 2

Setup does not require additional attention. You can manually select higher FPS, Higher-quality LiDAR recording (720x960 vs 1440x1920)

- Record the demo footage in your desired demo environment
- Export using "Shareable/Internal format (.r3d)"
- Transfer the exported data to your computer
- Rename the .r3d extension to .zip and extract

Convert Record3D data to Instant NGP format

``` bash
python scripts/record3d2nerf.py --scene path/to/data
```
If you capture the scene in the landscape orientation, add --rotate.

This will create:
- transforms.json - Main file for instant-ngp training
- arkit_transforms/ folder - Contains original ARKit data (backup only)
- images/ folder - Extracted RGB frames

For instant-ngp training, use the main transforms.json file in the root of your data directory, not the one inside the arkit_transforms folder. The main transforms.json has been converted by the record3d2nerf.py script to use instant-ngp's expected coordinate system and format, while the arkit_transforms/transforms.json contains the original ARKit data before conversion and is kept as a backup but isn't used for training.

Loading the snapshot as well as saving the model is exectly the same as for approaches before.

Launch instant ngp training:
```bash
 ./instant-ngp path/to/data
```

Training parameters: Use conservative settings initially due to challenging lighting conditions. You can try to use custom config file for the training process (need to put the 'high_quality.json' file in the cofigs/nerf folder first. 
``` bash
./instant-ngp path/to/data --config configs/nerf/high_quality.json --width 1280 --height 720
```
Note: Unfortunately the capabilities of our GPU were not enought to squeeze out absolute maximum of InstantNGP using our custom data. To compare the results we need to configure better rendering settings (in GUI directly), however we get less than 1fps of rendering far from reaching the best settings. 

Saving: In the Instant NGP GUI, navigate to the "Snapshot" section. Click "Save" to create a "base.ingp" file

You can launch the training which will also save the results automatically: 
``` bash
python scripts/run.py --scene path/to/data --save_snapshot path/to/data/model.ingp --n_steps 5000
```

Loading: 
Run `.\instant-ngp.exe "full_path_to_ingp_file_folder/2000.ingp" --no-train`

That will load the Instant NGP app with your reconstruction.






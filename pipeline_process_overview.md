### Overview 

This is the pipeline process of 3D reconstruction of sewer pipeline using Nerfacto model from NeRFstudio. 

##### Installation 
	1. Create a conda environment and install necessary libaries 
		conda env create -f environment.yml
		conda activate nerfstudio
		
	Alteratively,
	You can follow the nerfstudio official installation guide 
		https://docs.nerf.studio/quickstart/installation.html 
		
##### Dataset preparation 
	1. Prepare the dataset from Scratch using Nerfstudio default process pipeline
		ns-process-data {images, video} --data {DATA_PATH} --output-dir {PROCESSED_DATA_DIR}

	After dataset preprocessing is done, sparse_pc.ply will be available in the output directory. You can directly construct the surface construction using that 
	colmap result pointcloud. 
	
##### Model training 
		ns-train nerfacto --pipeline.model.predict-normals True
		
#### Model Exporting 
	While training the model you can access the training GUI through localhost - 127.0.0.1:7007
	
	There is a command generator for the exporting pointcloud and mesh 
	eg. for exporting pointcloud 
	ns-export pointcloud --load-config {CONFIG.yml} --output-dir {OUTPUT_DIR} --num-points 1000000 --remove-outliers True --normal-method open3d --save-world-frame False 
	
	eg.  for exporting mesh 
	ns-export poisson --load-config {CONFIG.yml} --output-dir {OUTPUT_DIR} --target-num-faces 50000 --num-pixels-per-side 2048 --num-points 1000000 --remove-outliers True --normal-method open3d
	
#### Surface construction 
	After getting the pointcloud, run the surface_construction.ipynb with the pointcloud directory. Then, you will get the final 3D surface reconstructed result. 
	If you want the mesh with the color variant, use .mtl format for the construction, otherwise use the .obj format which can be easily opened by the thirdparty app like cloudcompare.
	
# Tinkering With Point Cloud

This project explores various operations and algorithms on point clouds using Python and Open3D.

## Project Overview
The project includes functionality for detecting planes in point clouds, reorienting these planes, and smoothing the point clouds using Poisson surface reconstruction. It aims to provide a comprehensive set of tools for point cloud manipulation and analysis.

Plane Detector
The code of this section can be found in the plane_detector.py file
Refer to Floor Detection subsection in Playground.ipynb
For plane detection I experimented with three different approaches -

RANSAC (Random Sample Consensus): Iteratively selects a random subset of points, fits a model (plane), and evaluates the fit by counting inliers within a distance threshold.

<img width="623" height="625" alt="image" src="https://github.com/user-attachments/assets/ea2d4a4d-74b1-4da0-9561-eb109f5dc117" />

# Playing With Point Cloud
This project explores various operations and algorithms on point clouds using Python and Open3D.

## Project Overview
The project includes functionality for detecting planes in point clouds, reorienting these planes, and smoothing the point clouds using Poisson surface reconstruction. It aims to provide a comprehensive set of tools for point cloud manipulation and analysis.

### Plane Detector
* The code of this section can be found in the [plane_detector.py](point_cloud_playground/plane_detector.py) file
* Refer to Floor Detection subsection in [Playground.ipynb](./Playground.ipynb)

For plane detection I experimented with three different approaches - 
* RANSAC (Random Sample Consensus): Iteratively selects a random subset of points, fits a model (plane), and evaluates the fit by counting inliers within a distance threshold.
<p align="center">
  <img src="images/RANSAC_shoe.png" width="90%" alt="Image 1 Caption">
</p>


* Convex Hull:  Computes the smallest convex polygon that can enclose all points in the point cloud.
<p align="center">
  <img src="images/ConvexHull_1.png" width="90%" alt="Image 1 Caption">
</p>

* PCA (Priniciple Component Analysis): Uses eigenvalue decomposition of the covariance matrix of the points to find the main directions of variation. The normal to the plane is given by the eigenvector corresponding to the smallest eigenvalue.
<p align="center">
  <img src="images/PCA_shoe2_pc.png" width="90%" alt="Image 1 Caption">
</p>

#### RANSAC (Random Sample Consensus): The winning algorithm
Since the given data was noisy and outlier rich I reasoned that RANSAC will be the better approach compared to the other two approaches and verified it experimentally.

<p align="center">
  <img src="images/ConvexHull_glove_pc.png" width="30%" alt="Plane Estimation using convex Hull">
  <img src="images/PCA_glove_pc.png" width="30%" alt="Plane Estimation using PCA">
  <img src="images/RANSAC_glove_pc.png" width="30%" alt="Plane Estimation Using RANSAC">
</p>

<p align="center">
  <span style="display:inline-block; width:30%; text-align:center;">Plane Estimation using convex Hull</span>
  <span style="display:inline-block; width:30%; text-align:center;">Plane Estimation using PCA</span>
  <span style="display:inline-block; width:30%; text-align:center;">Plane Estimation Using RANSAC</span>
</p>

As can be observed from the above cases whenever there are enough inlier points available this approach works extremely well.

However there are three specific cases where this approach fails, 
* Insufficient Inliers: RANSAC relies on finding a sufficient number of inliers that support the proposed plane model. If the actual number of inliers (points that lie on the plane) is too low compared to the total number of points, RANSAC might fail to find the correct plane.

<p align="center">
  <img src="images/LowInlierRANSAC.png" width="90%" alt="Image 1 Caption">
</p>

* Multiple Planes: If the point cloud contains multiple planes or other geometric structures, RANSAC might not be able to distinguish between them effectively. It could end up fitting a plane that is an average of several planes or fitting the wrong plane entirely.
  
<p align="center">
  <img src="images/Multiple_planes_RANSAC.png" width="90%" alt="Image 1 Caption">
</p>

* High Noise Levels: If the point cloud has a high level of noise, the random sampling process may frequently select noisy points, leading to incorrect plane models.
  
<p align="center">
  <img src="images/HighNOiseRANSAC.png" width="90%" alt="Image 1 Caption">
</p>

#### Future modification that can address the issues

To address the limitations of RANSAC in plane detection within point clouds, we can consider a modified approach that combines RANSAC with additional techniques. Specifically, we can enhance the robustness of RANSAC by incorporating hierarchical clustering and adaptive parameter tuning. Here's a detailed approach to tackle the mentioned issues:

- Preprocessing with Clustering:
        Hierarchical Clustering: Perform hierarchical clustering on the point cloud to segment it into smaller clusters that are more likely to represent individual planes or simpler geometric structures. This step helps to isolate different planes, making it easier for RANSAC to fit a plane model to each cluster.

- Adaptive RANSAC:
        Adaptive Parameters: Instead of using fixed parameters for RANSAC, adaptively tune the parameters (e.g., distance threshold, number of iterations) based on the characteristics of each cluster. This allows RANSAC to be more flexible and responsive to the specific properties of different regions of the point cloud.

- Post-Processing and Validation:
        Plane Validation: After RANSAC detects a plane, validate the plane by checking the density and distribution of inliers. Planes with insufficient inliers can be discarded, and multiple planes detected within the same cluster can be further analyzed to distinguish between them.

### Plane Reorientation
* The code for this section is in [utils.py](point_cloud_playground/utils.py)
This is done by simply calculating the transformation matrix from the plane equation to Y-Z plane. And then applying the transformation to the pointcloud.
Refer to Floor Reorientation subsection in [Playground.ipynb](./Playground.ipynb)


### Point Cloud Smoother
For smoothing of the point cloud, the Point Cloud Smoother class uses Poisson surface reconstruction. This method is widely used for creating a smooth, watertight surface from a noisy point cloud. Here is a brief overview of the process and its benefits:

#### Poisson Surface Reconstruction

Poisson surface reconstruction is a method that takes a set of oriented points (point cloud with normals) and produces a smooth surface that approximates the points. This method formulates the reconstruction as a spatial Poisson problem, which seeks to find a scalar field whose gradient best matches the input normals. The key steps in Poisson surface reconstruction are as follows:

- Normal Estimation: Estimating normals for the point cloud, which is a prerequisite for Poisson reconstruction.
- Reconstruction: Using the Poisson algorithm to reconstruct the surface from the oriented point cloud.
- Post-processing: Optionally, further processing the reconstructed mesh to remove noise and improve quality.

Usage in the Project

In this project, the PointCloudSmoother class encapsulates the functionality of Poisson surface reconstruction. The main method poisson_surface_reconstruction performs the reconstruction and returns the smoothed mesh. 

<p align="center">
  <img src="images/pc_with_normals_smooth.png" width="50%" alt="Point Cloud with Normals Pre Smoothing">
  <img src="images/smooth_mesh.png" width="50%" alt="Point Cloud Post Smoothing">
</p>




## Dependencies
Make sure you have the following dependencies installed:

- Python 3.9
- Open3D
- NumPy

You can install the required dependencies using:

```sh
pip install -r requirements.txt

```
## Build and Run

To build and run the project, follow these steps:
1. Clone the Repository:
```sh
git clone <repository-url>
cd Playing_With_Point_Cloud
```
2. Install dependencies:
```sh
pip install -r requirements.txt
```
3. Run the main script:
```sh
python point_cloud_playground/main.py
```

## Detailed Walkthrough
For a more detailed walkthrough of the code, check out the [Playground.ipynb](Playground.ipynb) notebook. It provides a step-by-step guide and explanations of the various functionalities implemented in this project.

## Contribution
Contributions are welcome! Feel free to open issues or pull requests to suggest improvements or report bugs.

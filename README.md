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


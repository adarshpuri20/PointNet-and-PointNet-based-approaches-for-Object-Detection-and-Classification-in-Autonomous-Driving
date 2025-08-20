from point_cloud_playground.plane_detector import PlaneDetectorRANSAC, PlaneDetectorConvexHull, PlaneDetectorPCA
import open3d as o3d
import numpy as np
import unittest

class TestPlaneDetectors(unittest.TestCase):
    def setUp(self):
        # Generate random point cloud data
        np.random.seed(0)
        num_points = 100
        points = np.random.rand(num_points, 3)
        self.point_cloud = o3d.geometry.PointCloud()
        self.point_cloud.points = o3d.utility.Vector3dVector(points)

    def test_plane_detection_ransac(self):
        # Apply random transformations to the point cloud
        self.point_cloud.transform(np.random.rand(4, 4))

        # Create PlaneDetectorRANSAC object
        plane_detector = PlaneDetectorRANSAC(self.point_cloud)

        # Detect plane
        floor_equation = plane_detector.detect_plane()

        # Assert that the equation is a tuple with length 4
        self.assertIsInstance(floor_equation, tuple)
        self.assertEqual(len(floor_equation), 4)

    def test_plane_detection_pca(self):
        # Apply random transformations to the point cloud
        self.point_cloud.transform(np.random.rand(4, 4))

        # Create PlaneDetectorPCA object
        plane_detector = PlaneDetectorPCA(self.point_cloud)

        # Detect plane
        floor_equation = plane_detector.detect_plane()

        # Assert that the equation is a tuple with length 4
        self.assertIsInstance(floor_equation, tuple)
        self.assertEqual(len(floor_equation), 4)

    def test_plane_detection_convex_hull(self):
        # Apply random transformations to the point cloud
        self.point_cloud.transform(np.random.rand(4, 4))

        # Create PlaneDetectorConvexHull object
        plane_detector = PlaneDetectorConvexHull(self.point_cloud)

        # Detect plane
        floor_equation = plane_detector.detect_plane()

        # Assert that the equation is a tuple with length 4
        self.assertIsInstance(floor_equation, tuple)
        self.assertEqual(len(floor_equation), 4)

if __name__ == '__main__':
    unittest.main()
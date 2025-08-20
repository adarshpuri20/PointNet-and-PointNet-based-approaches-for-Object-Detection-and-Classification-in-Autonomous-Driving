import os
import sys
sys.path.append("/home/abhishek/dev/Projects/Playing_With_Point_Cloud/")

import point_cloud_playground
import open3d as o3d
from point_cloud_playground import utils


def load_data(data_folder = './data'):
    files = os.listdir(data_folder)
    point_cloud_files = [file for file in files if file.endswith(('.ply'))]
    point_clouds = []
    for file in point_cloud_files:
        file_path = os.path.join(data_folder,file)
        point_cloud = o3d.io.read_point_cloud(file_path)
        point_clouds.append(point_cloud)
    return point_clouds

def main():
    point_clouds = load_data()
    pcd = point_clouds[0]
    plane_detector = point_cloud_playground.plane_detector.PlaneDetectorRANSAC(pcd)
    floor_equation = plane_detector.detect_plane()
    reorient = plane_detector.reorient_plane()
    plane_equation = (1,0,0,0)
    mesh = utils.create_plane_from_equation(plane_equation,plane_size=2)
    smoother = point_cloud_playground.point_cloud_smoother.PointCloudSmoother(plane_detector.point_cloud)
    pcd = smoother.poisson_surface_reconstruction()
    o3d.visualization.draw_geometries(
                                        [mesh,plane_detector.point_cloud],
                                        window_name="Open3D Visualization",
                                        width=800,
                                        height=600,
                                        left=50,
                                        top=50,
                                        point_show_normal=True
                                    )
if __name__ == "__main__":
    main()

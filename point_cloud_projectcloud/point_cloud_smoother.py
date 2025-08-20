import open3d as o3d

class PointCloudSmoother:
    """
    A class for smoothing point clouds using different methods.
    """

    def __init__(self, point_cloud):
        """
        Parameters:
        - point_cloud: a point cloud of type o3d.geometry.PointCloud()
        """
        self.point_cloud = point_cloud

    
    def poisson_surface_reconstruction(self,depth=9):
        """
        Returns:
        - mesh (open3d.geometry.TriangleMesh): Reconstructed surface mesh.
        """
        self.point_cloud.estimate_normals()
        mesh, densities = o3d.geometry.TriangleMesh.create_from_point_cloud_poisson(self.point_cloud,depth=depth)
        return mesh

   

def main():
    # Load point cloud data
    file_path = "data/shoe_pc.ply"

    # Create PointCloudSmoother object
    smoother = PointCloudSmoother(file_path)

    # Poisson surface reconstruction
    mesh_poisson = smoother.poisson_surface_reconstruction()

    # Visualize results
    o3d.visualization.draw_geometries([mesh_poisson])

if __name__ == "__main__":
    main()
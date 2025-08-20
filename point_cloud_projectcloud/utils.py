import numpy as np
import open3d as o3d

def compute_rotation_matrix(normal_vector):
    x_axis = np.array([1, 0, 0])
    normal_vector = normal_vector / np.linalg.norm(normal_vector)
    
    # Compute the axis of rotation (cross product)
    axis = np.cross(normal_vector, x_axis)
    axis_norm = np.linalg.norm(axis)
    
    if axis_norm != 0:
        axis = axis / axis_norm
        # Compute the angle of rotation (dot product)
        angle = np.arccos(np.dot(normal_vector, x_axis))
        
        # Compute the skew-symmetric cross-product matrix of the axis
        K = np.array([[0, -axis[2], axis[1]],
                      [axis[2], 0, -axis[0]],
                      [-axis[1], axis[0], 0]])
        
        # Compute the rotation matrix using Rodrigues' rotation formula
        rotation_matrix = np.eye(3) + np.sin(angle) * K + (1 - np.cos(angle)) * np.dot(K, K)
    else:
        # If the axis norm is 0, the normal vector is already aligned with the x_axis
        rotation_matrix = np.eye(3)
    
    return rotation_matrix

def calculate_reorientation_matrix(floor_equation):
    if len(floor_equation) != 4:
        raise ValueError("floor_equation must be a tuple of size 4")
    
    a, b, c, d = floor_equation
    
    # Compute the normal vector of the plane
    normal_vector = np.array([a, b, c])
    
    # Compute the rotation matrix
    rotation_matrix = compute_rotation_matrix(normal_vector)
    
    # Compute the translation to move the plane to x = 0
    if a != 0:
        translation = np.array([-d / a, 0, 0])
    else:
        translation = np.array([0, 0, 0])
    
    # Create the transformation matrix
    transformation_matrix = np.eye(4)
    transformation_matrix[:3, :3] = rotation_matrix
    transformation_matrix[:3, 3] = translation
    
    return transformation_matrix

def create_plane_from_equation(floor_equation, plane_size=5, color=[0.1, 0.9, 0.1]):
    """
    Create an Open3D mesh representing a plane from its equation ax + by + cz + d = 0.

    Args:
    - a, b, c, d (float): Coefficients of the plane equation ax + by + cz + d = 0.
    - plane_size (float): Size of the plane in each dimension.
    - color (list): RGB color values for the plane.

    Returns:
    - plane_mesh (o3d.geometry.TriangleMesh): Open3D mesh representing the plane.
    """
    # Define the dimensions of the floor plane mesh
    if len(floor_equation) != 4:
        raise ValueError("floor_equation must be a tuple of size 4")
    
    a, b, c, d = floor_equation
    mesh = o3d.geometry.TriangleMesh()

    if c != 0:
        # Create the vertices of the plane
        vertices = [
            [plane_size, plane_size, -(d + a * plane_size + b * plane_size) / c],
            [-plane_size, plane_size, -(d - a * plane_size + b * plane_size) / c],
            [-plane_size, -plane_size, -(d - a * plane_size - b * plane_size) / c],
            [plane_size, -plane_size, -(d + a * plane_size - b * plane_size) / c]
        ]
    else:
        # If c = 0, the plane is parallel to the XY plane
        # Set a fixed z coordinate
        z_coordinate = -d / b if b != 0 else 0

        # Create the vertices of the plane with a fixed z coordinate
        vertices = [
            [plane_size, plane_size, z_coordinate],
            [-plane_size, plane_size, z_coordinate],
            [-plane_size, -plane_size, z_coordinate],
            [plane_size, -plane_size, z_coordinate]
        ]

    # Create the triangles of the plane
    triangles = [[0, 1, 2], [0, 2, 3]]

    # Convert to Open3D format
    vertices = o3d.utility.Vector3dVector(vertices)
    triangles = o3d.utility.Vector3iVector(triangles)

    # Create the mesh
    mesh.vertices = vertices
    mesh.triangles = triangles

    # Optionally, set the color of the plane
    mesh.paint_uniform_color(color)

    return mesh
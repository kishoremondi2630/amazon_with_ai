import torch # type: ignore
import smplx # type: ignore
import numpy as np
import trimesh # type: ignore
import pyrender # type: ignore
from PIL import Image # type: ignore

def create_smplx_model(model_path, gender, height, weight, age, texture_path):
    # Load the SMPL-X model
    smplx_model = smplx.create(
        model_path=model_path,
        model_type="smplx",
        gender=gender,
        use_pca=False,
        batch_size=1
    )

    # Initialize betas
    betas = np.zeros(10)

    # Adjust betas based on height, weight, and age
    if age <= 5:
        height = max(80, height)
        betas[0] = (height - 80) / 10
        betas[1] = (weight - 5) / 5
    elif age <= 12:
        height = max(90, height)
        betas[0] = (height - 90) / 5
        betas[1] = (weight - 15) / 5
    elif age <= 19:
        height = max(150, height)
        betas[0] = (height - 150) / 10
        betas[1] = (weight - 40) / 10
    elif age <= 50:
        height = max(150, height)
        betas[0] = (height - 150) / 10
        betas[1] = (weight - 60) / 10
    else:
        height = max(140, height)
        betas[0] = (height - 140) / 10
        betas[1] = (weight - 50) / 10

    # Convert betas to tensor
    betas = torch.tensor(betas, dtype=torch.float32).unsqueeze(0)

    # Create dummy poses (neutral T-pose)
    body_pose = torch.zeros([1, 63], dtype=torch.float32)
    global_orient = torch.zeros([1, 3], dtype=torch.float32)
    left_hand_pose = torch.zeros([1, 45], dtype=torch.float32)
    right_hand_pose = torch.zeros([1, 45], dtype=torch.float32)
    jaw_pose = torch.zeros([1, 3], dtype=torch.float32)
    leye_pose = torch.zeros([1, 3], dtype=torch.float32)
    reye_pose = torch.zeros([1, 3], dtype=torch.float32)
    expression = torch.zeros([1, 10], dtype=torch.float32)

    # Generate the 3D model output
    output = smplx_model(
        global_orient=global_orient,
        body_pose=body_pose,
        left_hand_pose=left_hand_pose,
        right_hand_pose=right_hand_pose,
        jaw_pose=jaw_pose,
        leye_pose=leye_pose,
        reye_pose=reye_pose,
        expression=expression,
        betas=betas,
        return_verts=True
    )

    # Extract mesh vertices and faces
    vertices = output.vertices[0].detach().cpu().numpy()
    faces = smplx_model.faces

    # Create and center the mesh
    mesh = trimesh.Trimesh(vertices=vertices, faces=faces)
    center = mesh.centroid
    mesh.apply_translation(-center)

    # Define simple material color (you can use texture mapping here if needed)
    material = pyrender.MetallicRoughnessMaterial(baseColorFactor=[1.0, 0.8, 0.6, 1.0])
    render_mesh = pyrender.Mesh.from_trimesh(mesh, material=material)

    # Create scene and add mesh
    scene = pyrender.Scene()
    scene.add(render_mesh)

    # Add camera
    camera = pyrender.PerspectiveCamera(yfov=np.pi / 3.0)
    camera_pose = np.array([
        [1.0,  0.0,  0.0,  0.9],
        [0.0,  1.0,  0.0,  1.0],
        [0.0,  0.0,  1.0,  4.5],
        [0.0,  0.0,  0.0,  1.0]
    ])
    scene.add(camera, pose=camera_pose)

    # Add light
    light = pyrender.DirectionalLight(color=np.ones(3), intensity=2.0)
    scene.add(light, pose=camera_pose)

    # Render the scene
    pyrender.Viewer(scene, use_raymond_lighting=True)

    return output

# Define model and input parameters
model_path = "/Users/kishoremondi/kishore/models"
texture_path = "/Users/kishoremondi/amazon-ai-3d/textures/brown-skin.jpg"  # currently unused
gender = "male"
height = 178
weight = 83
age = 50

# Generate the 3D model
output = create_smplx_model(model_path, gender, height, weight, age, texture_path)


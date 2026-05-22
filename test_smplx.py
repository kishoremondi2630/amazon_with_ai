import os
import pyrender
import numpy as np
import smplx
import torch
import trimesh
import matplotlib.pyplot as plt

def generate_3d_model(front_path, height, weight, age, gender="male",shirt_path=None, pant_path=None):
    print("✅ Starting 3D model generation...")
    model_path = os.path.join(os.getcwd(), "models")

    smplx_model = smplx.create(
        model_path=model_path,
        model_type="smplx",
        gender=gender,
        use_pca=False,
        batch_size=1
    )

    # Betas based on body measurements
    betas = np.zeros(10)
    if age <= 19:
        betas[0] = (height - 150) / 10
        betas[1] = (weight - 40) / 10
    else:
        betas[0] = (height - 150) / 10
        betas[1] = (weight - 60) / 10
    betas = torch.tensor(betas, dtype=torch.float32).unsqueeze(0)

    # Dummy poses
    body_pose = torch.zeros([1, 63])
    global_orient = torch.zeros([1, 3])
    expression = torch.zeros([1, 10])
    left_hand_pose = torch.zeros([1, 45])
    right_hand_pose = torch.zeros([1, 45])
    jaw_pose = torch.zeros([1, 3])
    leye_pose = torch.zeros([1, 3])
    reye_pose = torch.zeros([1, 3])

    # Output model
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

    vertices = output.vertices[0].detach().cpu().numpy()
    faces = smplx_model.faces
    mesh = trimesh.Trimesh(vertices, faces)
    mesh.apply_translation(-mesh.centroid)

    # Rendering
    material = pyrender.MetallicRoughnessMaterial(baseColorFactor=[0.8, 0.5, 0.5, 1.0])
    render_mesh = pyrender.Mesh.from_trimesh(mesh, material=material)

    scene = pyrender.Scene()
    scene.add(render_mesh)

    camera = pyrender.PerspectiveCamera(yfov=np.pi / 3.0)
    cam_pose = np.array([
        [1, 0, 0, 0],
        [0, 1, 0, 1],
        [0, 0, 1, 4],
        [0, 0, 0, 1]
    ])
    scene.add(camera, pose=cam_pose)

    light = pyrender.DirectionalLight(color=np.ones(3), intensity=3.0)
    scene.add(light, pose=cam_pose)

    # Render to offscreen image
    renderer = pyrender.OffscreenRenderer(1280, 960)
    color, _ = renderer.render(scene)

    output_path = os.path.join("static", "uploads", "model_output.png")
    plt.imsave(output_path, color)
    renderer.delete()
    
    print("✅ Model image saved to:", output_path)
    return output_path

# Add test run
if __name__ == '__main__':
    front_image_path = os.path.join("static", "uploads", "front_image.jpg")  # Replace with actual image path if needed
    if not os.path.exists(front_image_path):
        print(f"⚠️ Image not found at {front_image_path}. Place a sample image there first.")
    else:
        output = generate_3d_model(front_image_path, height=170, weight=60, age=22)
        print("✅ Done. Output image:", output)

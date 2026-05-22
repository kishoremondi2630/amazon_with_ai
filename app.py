from flask import Flask, request, render_template, jsonify, send_from_directory
import os
from test_smplx import generate_3d_model

app = Flask(__name__, static_url_path='/static')
UPLOAD_FOLDER = os.path.join("static", "uploads")
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

CLOTHES_DIR = "/Users/kishoremondi/amazon-ai-3d/cloths"

@app.route('/')
def home():
    return render_template('details.html')

@app.route('/displaymodel')
def index():
    return render_template('details.html')


@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'),
                               'favicon.ico', mimetype='image/vnd.microsoft.icon')

# Serve .glb with correct MIME
@app.route('/static/uploads/<filename>')
def serve_glb_file(filename):
    if filename.endswith('.glb'):
        return send_from_directory(app.config['UPLOAD_FOLDER'], filename, mimetype='model/gltf-binary')
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)


@app.route('/generate-model', methods=['POST'])
def generate_model():
    try:
        # User body inputs
        height = int(request.form['height'])
        weight = int(request.form['weight'])
        age = int(request.form['age'])
        gender = request.form.get('gender', 'neutral').lower()

        # Clothing selection from frontend
        shirt_type = request.form.get("shirt", "tshirt")   # default
        pant_type = request.form.get("pant", "kids_pant")  # default

        # Clothing file maps
        shirt_map = {
            "shirt": "shirt_for_men.glb",
            "tshirt": "t_shirt.glb"
        }
        pant_map = {
            "kids_pant": "kids_pant_design.glb"
        }

        shirt_path = os.path.join(CLOTHES_DIR, shirt_map.get(shirt_type, "t_shirt.glb"))
        pant_path = os.path.join(CLOTHES_DIR, pant_map.get(pant_type, "kids_pant_design.glb"))

        # Save uploaded photos
        front_image = request.files['front_image']
        left_image = request.files['left_image']
        right_image = request.files['right_image']

        front_path = os.path.join(app.config['UPLOAD_FOLDER'], "front_image.jpg")
        left_path = os.path.join(app.config['UPLOAD_FOLDER'], "left_image.jpg")
        right_path = os.path.join(app.config['UPLOAD_FOLDER'], "right_image.jpg")

        front_image.save(front_path)
        left_image.save(left_path)
        right_image.save(right_path)

        # SMPL-X model selection
        model_file_map = {
            'male': 'SMPLX_MALE.npz',
            'female': 'SMPLX_FEMALE.npz',
            'neutral': 'SMPLX_NEUTRAL.npz'
        }

        model_filename = model_file_map.get(gender, 'SMPLX_NEUTRAL.npz')
        model_file_path = os.path.join("models", "smplx", model_filename)

        if not os.path.exists(model_file_path):
            raise FileNotFoundError(f"Model file not found at {model_file_path}")

        # ---- CALL DRESSED MODEL GENERATOR ----
        generated_model_path = generate_3d_model(
            front_path, height, weight, age, model_file_path,
            shirt_path, pant_path
        )
        # --------------------------------------

        if not os.path.exists(generated_model_path):
            raise FileNotFoundError(f"Model not found at {generated_model_path}")

        final_glb_path = os.path.join(app.config['UPLOAD_FOLDER'], "smplx_model.glb")
        os.replace(generated_model_path, final_glb_path)

        return jsonify({'model_path': "/static/uploads/smplx_model.glb"})

    except Exception as e:
        print(f"❌ Error occurred: {str(e)}")
        return jsonify({'error': str(e)}), 500


if __name__ == '__main__':
    print("🚀 Flask server starting...")
    app.run(debug=True, threaded=True)

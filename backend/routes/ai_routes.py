import os
from pathlib import Path
from flask import Blueprint, request, jsonify, current_app
from werkzeug.utils import secure_filename
from ultralytics import YOLO

ai_bp = Blueprint('ai', __name__)

# --- ROBUST MODEL LOADING ---
# We calculate the path relative to THIS file to be safe
BASE_DIR = Path(__file__).resolve().parents[2] # Points to CivicResolve/
MODEL_PATH = BASE_DIR / "ai_ml" / "models" / "best_civic_model.pt"

print(f"🔍 Looking for model at: {MODEL_PATH}")

model = None
try:
    if MODEL_PATH.exists():
        model = YOLO(str(MODEL_PATH))
        print("✅ AI Model Loaded Successfully")
    else:
        print("❌ Model file NOT found! Please run training first.")
except Exception as e:
    print(f"❌ CRITICAL ERROR LOADING MODEL: {e}")

@ai_bp.route('/predict', methods=['POST'])
def predict():
    print("⚡ Incoming Prediction Request...") # Debug Print

    if not model:
        print("⚠️ Prediction failed: Model not loaded.")
        return jsonify({'error': 'AI Model not ready'}), 503
        
    if 'image' not in request.files:
        print("⚠️ Prediction failed: No image in request.")
        return jsonify({'error': 'No image provided'}), 400

    file = request.files['image']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400

    try:
        # 1. Verify Upload Folder Exists
        upload_folder = current_app.config['UPLOAD_FOLDER']
        if not os.path.exists(upload_folder):
            os.makedirs(upload_folder)
            print(f"📂 Created missing upload folder: {upload_folder}")

        # 2. Save Temp File
        filename = secure_filename(f"temp_pred_{file.filename}")
        temp_path = os.path.join(upload_folder, filename)
        file.save(temp_path)
        print(f"💾 Saved temp image to: {temp_path}")

        # 3. Run Inference
        print("🧠 Running YOLO Inference...")
        results = model(temp_path, conf=0.25)
        
        detections = []
        for r in results:
            for box in r.boxes:
                cls_id = int(box.cls[0])
                conf = float(box.conf[0])
                name = model.names[cls_id]
                
                print(f"   ➤ Found: {name} ({conf:.2f})") # Debug Print
                
                detections.append({
                    'class': name,
                    'confidence': conf,
                    'box': box.xyxy[0].tolist()
                })
        
        # 4. Cleanup (Optional: remove temp file to save space)
        # os.remove(temp_path)
        
        print(f"✅ Success! Returning {len(detections)} detections.")
        return jsonify({'detections': detections, 'count': len(detections), 'predictions': detections}), 200

    except Exception as e:
        # THIS IS THE IMPORTANT PART: Print the specific error to terminal
        print(f"❌ PREDICTION CRASHED: {str(e)}")
        import traceback
        traceback.print_exc() # Print full error trace
        return jsonify({'error': str(e)}), 500
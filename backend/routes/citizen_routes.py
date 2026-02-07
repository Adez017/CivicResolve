from flask import Blueprint, request, jsonify, current_app
from werkzeug.utils import secure_filename
import os
import uuid
from backend.models import db, PotholeReport, GarbageReport
from backend.utils.issue_validator import get_validator

citizen_bp = Blueprint('citizen', __name__)

@citizen_bp.route('/report', methods=['POST'])
def submit_report():
    if 'image' not in request.files:
        return jsonify({'error': 'No image provided'}), 400
        
    file = request.files['image']
    issue_type = request.form.get('type')
    
    if issue_type not in ['pothole', 'garbage']:
        return jsonify({'error': 'Invalid issue type'}), 400

    ext = os.path.splitext(file.filename)[1]
    filename = secure_filename(f"{issue_type}_{uuid.uuid4().hex}{ext}")
    save_path = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
    file.save(save_path)
    
    # --- Issue Validation ---
    lat = request.form.get('lat', type=float)
    lng = request.form.get('lng', type=float)
    
    validator = get_validator()
    validation = validator.validate_report(save_path, lat, lng, issue_type)
    
    if validation['decision'] == 'rejected':
        os.remove(save_path)  # Cleanup rejected image
        return jsonify({
            'error': validation['message'],
            'trust_score': validation['score']
        }), 400
    
    new_report = None
    if issue_type == 'pothole':
        new_report = PotholeReport(
            image_filename=filename,
            severity=request.form.get('severity', 'medium'),
            latitude=lat,
            longitude=lng,
            address=request.form.get('address')
        )
    else:
        new_report = GarbageReport(
            image_filename=filename,
            garbage_type=request.form.get('garbage_type', 'mixed'),
            latitude=lat,
            longitude=lng,
            address=request.form.get('address')
        )
        
    db.session.add(new_report)
    db.session.commit()
    
    return jsonify({
        'message': 'Report saved',
        'id': new_report.id,
        'trust_score': validation['score'],
        'validation_status': validation['decision']
    }), 201
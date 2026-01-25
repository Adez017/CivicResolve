from flask import Blueprint, request, jsonify, current_app
from werkzeug.utils import secure_filename
import os
from backend.models import db, PotholeReport, GarbageReport

worker_bp = Blueprint('worker', __name__)

@worker_bp.route('/my-tasks/<worker_id>', methods=['GET'])
def get_worker_tasks(worker_id):
    p_tasks = PotholeReport.query.filter_by(assigned_worker_id=worker_id, status='assigned').all()
    g_tasks = GarbageReport.query.filter_by(assigned_worker_id=worker_id, status='assigned').all()
    
    tasks = [p.to_dict() for p in p_tasks] + [g.to_dict() for g in g_tasks]
    return jsonify(tasks), 200

@worker_bp.route('/complete', methods=['POST'])
def complete_task():
    file = request.files.get('image')
    rid = request.form.get('id')
    rtype = request.form.get('type')
    
    if not file or not rid or not rtype:
        return jsonify({'error': 'Missing data'}), 400

    filename = secure_filename(f"resolved_{rtype}_{rid}_{file.filename}")
    path = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
    file.save(path)
    
    report = None
    if rtype == 'pothole':
        report = PotholeReport.query.get(rid)
    elif rtype == 'garbage':
        report = GarbageReport.query.get(rid)
        
    if report:
        report.resolved_image = filename
        report.status = 'completed'
        db.session.commit()
        return jsonify({'message': 'Task marked completed'}), 200
        
    return jsonify({'error': 'Report not found'}), 404
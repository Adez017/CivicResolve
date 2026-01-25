from flask import Blueprint, request, jsonify
from backend.models import db, PotholeReport, GarbageReport

task_bp = Blueprint('tasks', __name__)

@task_bp.route('/assign', methods=['POST'])
def assign_task():
    data = request.json
    report_id = data.get('id')
    rtype = data.get('type')
    worker_id = data.get('worker_id')
    
    report = None
    if rtype == 'pothole':
        report = PotholeReport.query.get(report_id)
    elif rtype == 'garbage':
        report = GarbageReport.query.get(report_id)
        
    if not report:
        return jsonify({'error': 'Report not found'}), 404
        
    report.assigned_worker_id = worker_id
    report.status = 'assigned'
    db.session.commit()
    
    return jsonify({'message': 'Task assigned successfully'}), 200
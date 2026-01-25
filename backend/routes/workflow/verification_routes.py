from flask import Blueprint, request, jsonify
from backend.models import db, PotholeReport, GarbageReport

verify_bp = Blueprint('verification', __name__)

@verify_bp.route('/verify', methods=['POST'])
def verify_fix():
    data = request.json
    rid = data.get('id')
    rtype = data.get('type')
    decision = data.get('decision') # 'approve' or 'reject'
    notes = data.get('notes', '')
    
    report = None
    if rtype == 'pothole':
        report = PotholeReport.query.get(rid)
    elif rtype == 'garbage':
        report = GarbageReport.query.get(rid)
        
    if not report:
        return jsonify({'error': 'Report not found'}), 404
        
    if decision == 'approve':
        report.status = 'verified'
        report.verification_notes = notes
    else:
        report.status = 'assigned' # Send back to worker
        report.verification_notes = f"REJECTED: {notes}"
        
    db.session.commit()
    return jsonify({'message': f'Task {decision}d'}), 200
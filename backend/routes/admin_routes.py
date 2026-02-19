from flask import Blueprint, jsonify
from backend.models import PotholeReport, GarbageReport
from backend.utils.auth import role_required
from flask import request
from backend.models import db
from datetime import datetime

admin_bp = Blueprint('admin', __name__)

@admin_bp.route('/reports/<report_type>/<int:report_id>/status', methods=['PUT'])
@role_required("admin")
def update_report_status(report_type, report_id):

    if report_type == "pothole":
        report = PotholeReport.query.get(report_id)
    elif report_type == "garbage":
        report = GarbageReport.query.get(report_id)
    else:
        return jsonify({"error": "Invalid report type"}), 400

    if not report:
        return jsonify({"error": "Report not found"}), 404

    new_status = request.json.get("status")

    if new_status not in ["reported", "under_review", "in_progress", "resolved"]:
        return jsonify({"error": "Invalid status"}), 400

    report.status = new_status

    # 🔥 Timeline updates
    if new_status == "under_review":
        report.reviewed_at = datetime.utcnow()
    elif new_status == "in_progress":
        report.in_progress_at = datetime.utcnow()
    elif new_status == "resolved":
        report.resolved_at = datetime.utcnow()

    db.session.commit()

    return jsonify({"message": "Status updated successfully"}), 200


@admin_bp.route('/', methods=['GET'])
@role_required("admin")
def admin_index():

    """Fixes 404 on /api/admin"""
    return jsonify({
        'message': 'CivicResolve Admin API',
        'status': 'active',
        'endpoints': {
            'stats': '/api/admin/stats',
            'reports': '/api/admin/reports'
        }
    }), 200

@admin_bp.route('/reports', methods=['GET'])
@role_required("admin")
def get_all_reports():

    potholes = PotholeReport.query.all()
    garbage = GarbageReport.query.all()
    
    all_reports = [p.to_dict() for p in potholes] + [g.to_dict() for g in garbage]
    all_reports.sort(key=lambda x: x['created_at'], reverse=True)
    
    return jsonify(all_reports), 200

@admin_bp.route('/stats', methods=['GET'])
@role_required("admin")
def get_stats():

    p_count = PotholeReport.query.count()
    g_count = GarbageReport.query.count()
    
    return jsonify({
        'total': p_count + g_count,
        'potholes': p_count,
        'garbage': g_count
    }), 200
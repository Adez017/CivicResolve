from flask import Blueprint, jsonify
from backend.models import PotholeReport, GarbageReport

admin_bp = Blueprint('admin', __name__)

@admin_bp.route('/', methods=['GET'])
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
def get_all_reports():
    potholes = PotholeReport.query.all()
    garbage = GarbageReport.query.all()
    
    all_reports = [p.to_dict() for p in potholes] + [g.to_dict() for g in garbage]
    all_reports.sort(key=lambda x: x['created_at'], reverse=True)
    
    return jsonify(all_reports), 200

@admin_bp.route('/stats', methods=['GET'])
def get_stats():
    p_count = PotholeReport.query.count()
    g_count = GarbageReport.query.count()
    
    return jsonify({
        'total': p_count + g_count,
        'potholes': p_count,
        'garbage': g_count
    }), 200
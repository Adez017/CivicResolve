import os
import sys
from pathlib import Path

# Add project root to path BEFORE other backend imports
sys.path.append(str(Path(__file__).resolve().parent.parent))

import logging
import time
from flask import request
from flask import Flask, jsonify, send_from_directory
from flask_cors import CORS
from backend.config import config
from backend.models import db


def create_app(config_name='default'):
    app = Flask(__name__)
    
    # Load Config
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)
    CORS(app)
    db.init_app(app)
    logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler("logs/project.log"),
        logging.StreamHandler()
    ]
)


    # -----------------------------
    # Request Logging Middleware
    # -----------------------------

    @app.before_request
    def start_timer():
        request.start_time = time.time()

    @app.after_request
    def log_request(response):
        if not hasattr(request, "start_time"):
            return response

        duration = time.time() - request.start_time

        log_data = {
            "method": request.method,
            "path": request.path,
            "status": response.status_code,
            "duration_ms": round(duration * 1000, 2),
            "ip": request.remote_addr
        }

        app.logger.info(f"REQUEST_LOG: {log_data}")

        return response


    # --- 1. ROOT ROUTE (To fix 404 on home page) ---
    @app.route('/')
    def index():
        return jsonify({
            "message": "CivicResolve Backend is Running!",
            "status": "online"
        }), 200

    # --- 2. NEW: IMAGE SERVING ROUTE (Paste this INSIDE create_app) ---
    @app.route('/data/images/<path:filename>')
    def serve_image(filename):
        return send_from_directory(app.config['UPLOAD_FOLDER'], filename)
    # ------------------------------------------------------------------

    # Register Blueprints
    from backend.routes.citizen_routes import citizen_bp
    from backend.routes.admin_routes import admin_bp
    from backend.routes.ai_routes import ai_bp
    from backend.routes.workflow.task_routes import task_bp
    from backend.routes.workflow.worker_routes import worker_bp
    from backend.routes.workflow.verification_routes import verify_bp
    from backend.routes.auth_routes import auth_bp

    app.register_blueprint(auth_bp, url_prefix="/api/auth")
    app.register_blueprint(citizen_bp, url_prefix='/api/citizen')
    app.register_blueprint(admin_bp, url_prefix='/api/admin')
    app.register_blueprint(ai_bp, url_prefix='/api/ai')
    app.register_blueprint(task_bp, url_prefix='/api/workflow/tasks')
    app.register_blueprint(worker_bp, url_prefix='/api/workflow/worker')
    app.register_blueprint(verify_bp, url_prefix='/api/workflow/verify')


    # -----------------------------
    # Global Error Handlers
    # -----------------------------

    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({
            "success": False,
            "error": "Bad Request",
            "message": str(error)
        }), 400

    @app.errorhandler(401)
    def unauthorized(error):
        return jsonify({
            "success": False,
            "error": "Unauthorized",
            "message": "Authentication required"
        }), 401

    @app.errorhandler(403)
    def forbidden(error):
        return jsonify({
            "success": False,
            "error": "Forbidden",
            "message": "You do not have permission to access this resource"
        }), 403

    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
            "success": False,
            "error": "Not Found",
            "message": "The requested resource was not found"
        }), 404

    @app.errorhandler(500)
    def internal_error(error):
        app.logger.error(f"Server Error: {error}")
        return jsonify({
            "success": False,
            "error": "Internal Server Error",
            "message": "Something went wrong on the server"
        }), 500


    # Create Tables
    with app.app_context():
        db.create_all()

        
    from backend.models import User

    with app.app_context():
        db.create_all()

        if not User.query.filter_by(username="admin").first():
            db.session.add(User(username="admin", password="admin", role="admin"))
            db.session.commit()
        
    return app

# Create app instance for gunicorn
app = create_app()

if __name__ == '__main__':
    print("🚀 CivicResolve Server Running on http://0.0.0.0:5000")
    app.run(host='0.0.0.0', port=5000, debug=True)
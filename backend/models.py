from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class BaseReport(db.Model):
    """Abstract base class for common fields."""
    __abstract__ = True

    id = db.Column(db.Integer, primary_key=True)
    image_filename = db.Column(db.String(255), nullable=False)
    resolved_image = db.Column(db.String(255), nullable=True)
    
    # Location
    latitude = db.Column(db.Float)
    longitude = db.Column(db.Float)
    address = db.Column(db.String(255))
    
    # Workflow
    status = db.Column(db.String(20), default='pending') # pending, assigned, completed, verified
    assigned_worker_id = db.Column(db.String(50), nullable=True)
    verification_notes = db.Column(db.String(500), nullable=True)
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class PotholeReport(BaseReport):
    __tablename__ = 'potholes'
    severity = db.Column(db.String(20), default='medium') # low, medium, high

    def to_dict(self):
        return {
            'id': self.id,
            'type': 'pothole',
            'severity': self.severity,
            'status': self.status,
            'assigned_to': self.assigned_worker_id,
            'location': {'lat': self.latitude, 'lng': self.longitude, 'address': self.address},
            'images': {'original': self.image_filename, 'resolved': self.resolved_image},
            'created_at': self.created_at.isoformat()
        }

class GarbageReport(BaseReport):
    __tablename__ = 'garbage'
    garbage_type = db.Column(db.String(50), default='mixed') # plastic, organic

    def to_dict(self):
        return {
            'id': self.id,
            'type': 'garbage',
            'garbage_type': self.garbage_type,
            'status': self.status,
            'assigned_to': self.assigned_worker_id,
            'location': {'lat': self.latitude, 'lng': self.longitude, 'address': self.address},
            'images': {'original': self.image_filename, 'resolved': self.resolved_image},
            'created_at': self.created_at.isoformat()
        }
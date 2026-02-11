"""
Smart Issue Validator - Fake Report Detection
Validates civic issue reports for authenticity before processing.
"""

import os
import threading
from datetime import datetime, timedelta
from PIL import Image
from PIL.ExifTags import TAGS, GPSTAGS
from pathlib import Path
from math import radians, cos, sin, sqrt, atan2


class IssueValidator:
    """Validates civic issue reports and calculates trust scores."""
    
    # Scoring weights
    SCORE_GPS_MATCH = 20
    SCORE_RECENT_TIMESTAMP = 15
    SCORE_CIVIC_DETECTED = 25
    SCORE_CATEGORY_MATCH = 20
    SCORE_NOT_SCREENSHOT = 10
    SCORE_NORMAL_RATE = 10
    
    # Thresholds
    THRESHOLD_APPROVE = 80
    THRESHOLD_FLAG = 60
    MAX_GPS_DISTANCE_KM = 1.0  # 1km tolerance
    MAX_IMAGE_AGE_HOURS = 24
    
    def __init__(self, yolo_model=None):
        self.model = yolo_model
        self.checks = {}
        self.score = 100  # Start with full trust
        self.penalties = []
    
    def validate_report(self, image_path, claimed_lat=None, claimed_lng=None, 
                       issue_type=None, user_id=None):
        """
        Main validation method. Returns validation result.
        
        Returns:
            dict: {
                'score': int (0-100),
                'decision': 'approved' | 'flagged' | 'rejected',
                'message': str,
                'checks': dict of individual check results
            }
        """
        self.score = 100
        self.penalties = []
        self.checks = {}
        
        # Run all checks
        self._check_exif_data(image_path, claimed_lat, claimed_lng)
        self._detect_screenshot(image_path)
        self._verify_civic_content(image_path, issue_type)
        
        # Calculate final score (subtract penalties)
        final_score = max(0, min(100, self.score - sum(self.penalties)))
        
        # Determine decision
        if final_score >= self.THRESHOLD_APPROVE:
            decision = 'approved'
            message = "Report verified successfully."
        elif final_score >= self.THRESHOLD_FLAG:
            decision = 'flagged'
            message = "Your report is under review. We'll verify within 2 hours."
        else:
            decision = 'rejected'
            message = ("We couldn't verify this image. Please ensure your photo "
                      "shows an actual civic issue, was taken recently at the "
                      "reported location, and provides a clear view of the problem.")
        
        return {
            'score': final_score,
            'decision': decision,
            'message': message,
            'checks': self.checks
        }
    
    def _check_exif_data(self, image_path, claimed_lat=None, claimed_lng=None):
        """Extract and validate EXIF metadata."""
        try:
            img = Image.open(image_path)
            exif_data = img._getexif()
            
            if not exif_data:
                self.checks['exif'] = {'status': 'missing', 'note': 'No EXIF data found'}
                self.penalties.append(15)  # Suspicious but not fatal
                return
            
            # Parse EXIF tags
            exif = {}
            for tag_id, value in exif_data.items():
                tag = TAGS.get(tag_id, tag_id)
                exif[tag] = value
            
            # Check timestamp
            date_taken = exif.get('DateTimeOriginal') or exif.get('DateTime')
            if date_taken:
                try:
                    photo_time = datetime.strptime(date_taken, '%Y:%m:%d %H:%M:%S')
                    age_hours = (datetime.now() - photo_time).total_seconds() / 3600
                    
                    if age_hours > self.MAX_IMAGE_AGE_HOURS:
                        self.checks['timestamp'] = {'status': 'old', 'age_hours': age_hours}
                        self.penalties.append(20)
                    else:
                        self.checks['timestamp'] = {'status': 'recent', 'age_hours': age_hours}
                except (ValueError, TypeError):
                    self.checks['timestamp'] = {'status': 'parse_error'}
                    self.penalties.append(5)
            else:
                self.checks['timestamp'] = {'status': 'missing'}
                self.penalties.append(10)
            
            # Check GPS data
            gps_info = exif.get('GPSInfo')
            if gps_info and claimed_lat is not None and claimed_lng is not None:
                exif_lat, exif_lng = self._parse_gps(gps_info)
                if exif_lat is not None and exif_lng is not None:
                    distance = self._haversine(exif_lat, exif_lng, claimed_lat, claimed_lng)
                    if distance > self.MAX_GPS_DISTANCE_KM:
                        self.checks['gps'] = {'status': 'mismatch', 'distance_km': distance}
                        self.penalties.append(30)
                    else:
                        self.checks['gps'] = {'status': 'match', 'distance_km': distance}
            elif claimed_lat is not None and claimed_lng is not None:
                self.checks['gps'] = {'status': 'no_exif_gps'}
                self.penalties.append(10)
                
        except Exception as e:
            self.checks['exif'] = {'status': 'error', 'error': str(e)}
            self.penalties.append(5)
    
    def _parse_gps(self, gps_info):
        """Parse GPS coordinates from EXIF GPSInfo."""
        try:
            gps = {}
            for key in gps_info.keys():
                decode = GPSTAGS.get(key, key)
                gps[decode] = gps_info[key]

            def convert_to_degrees(value):
                d, m, s = value
                return d + (m / 60.0) + (s / 3600.0)

            lat_value = gps.get('GPSLatitude')
            lng_value = gps.get('GPSLongitude')

            # If either latitude or longitude is missing, GPS is unavailable
            if not lat_value or not lng_value:
                return None, None

            lat = convert_to_degrees(lat_value)
            lng = convert_to_degrees(lng_value)

            if gps.get('GPSLatitudeRef') == 'S':
                lat = -lat
            if gps.get('GPSLongitudeRef') == 'W':
                lng = -lng
            return lat, lng
        except Exception:
            return None, None
    
    def _haversine(self, lat1, lon1, lat2, lon2):
        """Calculate distance between two GPS coordinates in km."""
        R = 6371  # Earth's radius in km
        
        lat1, lon1, lat2, lon2 = map(radians, [lat1, lon1, lat2, lon2])
        dlat = lat2 - lat1
        dlon = lon2 - lon1
        
        a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
        c = 2 * atan2(sqrt(a), sqrt(1-a))
        
        return R * c
    
    def _detect_screenshot(self, image_path):
        """Detect if image is a screenshot."""
        try:
            img = Image.open(image_path)
            width, height = img.size
            
            # Common screenshot aspect ratios
            aspect = width / height if height else 0
            screenshot_aspects = [0.46, 0.56, 0.6, 1.78, 2.17]  # Phone screens
            
            is_screenshot = False
            
            # Check for exact phone resolutions
            phone_resolutions = [
                (1080, 2340), (1080, 2400), (1170, 2532),  # Modern phones
                (1125, 2436), (1440, 3200), (1284, 2778),
            ]
            if (width, height) in phone_resolutions or (height, width) in phone_resolutions:
                is_screenshot = True
            
            # Check for status bar indicators (top portion uniformity)
            if not is_screenshot:
                top_strip = img.crop((0, 0, width, min(50, height)))
                colors = top_strip.getcolors(maxcolors=100)
                if colors and len(colors) < 10:  # Very few colors = likely status bar
                    is_screenshot = True
            
            if is_screenshot:
                self.checks['screenshot'] = {'status': 'detected'}
                self.penalties.append(25)
            else:
                self.checks['screenshot'] = {'status': 'not_detected'}
                
        except Exception as e:
            self.checks['screenshot'] = {'status': 'error', 'error': str(e)}
    
    def _verify_civic_content(self, image_path, claimed_type=None):
        """Verify image contains civic infrastructure using YOLO model."""
        if not self.model:
            # Penalize when the AI model is not available so that missing
            # content verification does not silently result in a high score.
            self.checks['content'] = {
                'status': 'skipped',
                'note': 'No AI model loaded'
            }
            # Apply a penalty comparable to the "no civic detected" case.
            self.penalties.append(30)
            return
        
        try:
            results = self.model(image_path, conf=0.25, verbose=False)
            
            detections = []
            for r in results:
                for box in r.boxes:
                    cls_id = int(box.cls[0])
                    name = self.model.names[cls_id]
                    conf = float(box.conf[0])
                    detections.append({'class': name, 'confidence': conf})
            
            if not detections:
                self.checks['content'] = {'status': 'no_civic_detected'}
                self.penalties.append(30)
                return
            
            # Check if detection matches claimed type
            detected_classes = [d['class'].lower() for d in detections]
            
            if claimed_type:
                if claimed_type.lower() in detected_classes:
                    self.checks['content'] = {
                        'status': 'match',
                        'detected': detections,
                        'claimed': claimed_type
                    }
                else:
                    self.checks['content'] = {
                        'status': 'mismatch',
                        'detected': detections,
                        'claimed': claimed_type
                    }
                    self.penalties.append(20)
            else:
                self.checks['content'] = {
                    'status': 'detected',
                    'detected': detections
                }
                
        except Exception as e:
            self.checks['content'] = {'status': 'error', 'error': str(e)}


# Thread-safe singleton implementation
_validator_instance = None
_validator_lock = threading.Lock()


def get_validator(model=None):
    """
    Get or create a thread-safe singleton IssueValidator instance.
    
    Uses double-checked locking pattern to ensure thread safety while
    minimizing lock contention. This is critical for multi-threaded
    WSGI servers like gunicorn.
    
    Args:
        model: Optional YOLO model instance to use for content verification.
               If provided and the singleton doesn't have a model, it will be set.
    
    Returns:
        IssueValidator: The singleton validator instance.
    
    Thread Safety:
        This function is safe to call from multiple threads simultaneously.
        The first call creates the instance; subsequent calls return the
        existing instance without acquiring the lock (fast path).
    """
    global _validator_instance
    
    # Fast path: instance already exists (no lock needed)
    if _validator_instance is not None:
        # Update model if needed (atomic check-then-act requires lock)
        if model and _validator_instance.model is None:
            with _validator_lock:
                # Double-check after acquiring lock
                if _validator_instance.model is None:
                    _validator_instance.model = model
        return _validator_instance
    
    # Slow path: need to create instance (requires lock)
    with _validator_lock:
        # Double-check after acquiring lock (another thread may have created it)
        if _validator_instance is None:
            _validator_instance = IssueValidator(yolo_model=model)
    
    return _validator_instance


def reset_validator():
    """
    Reset the singleton instance. Useful for testing.
    
    Warning:
        This is NOT thread-safe during normal operation.
        Only use in test setup/teardown or application shutdown.
    """
    global _validator_instance
    with _validator_lock:
        _validator_instance = None

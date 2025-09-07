# CivicResolve: AI-Powered Civic Issue Management System

## Project Overview
CivicResolve implements a comprehensive workflow for civic issue detection, reporting, and resolution based on the flowchart specifications:

### Key Workflow Components:
1. **Proactive Detection**: City cameras with YOLO model detect issues automatically
2. **Citizen Reporting**: Mobile app for manual complaint submission  
3. **Intelligent Routing**: Automatic server-side processing and department assignment
4. **Worker Management**: Task assignment based on availability and location
5. **Severity Assessment**: AI-powered priority determination with time-based escalation
6. **Verification System**: YOLO-based task completion verification
7. **Anti-Fraud**: Detection of false reporting attempts

### Laptop Integration Features:
- Local PostgreSQL database setup
- Webcam integration for testing camera detection
- Simulated camera feeds for development
- Local server deployment without cloud dependencies

## File Structure Map to Workflow:
- `camera_integration/` → Handles camera feeds and real-time detection
- `workflow/` → Implements the complete issue lifecycle management
- `laptop_integration/` → Local deployment and testing utilities
- `ai_ml/` → YOLO models for detection and verification
- `backend/` → Flask API handling all server operations
- `frontend/` → React interfaces for citizens, workers, and admins

## Detailed File Structure & Developer Guide:

### **Root Files:**
- `app.py` → Main Flask application entry point and server startup
- `config.py` → PostgreSQL database and AI model configuration settings
- `requirements.txt` → Python dependencies for Flask, PostgreSQL, TensorFlow, OpenCV
- `setup.sh` → Automated environment setup script for development
- `run.sh` → Application startup script with database initialization
- `.env.example` → Environment variables template for local configuration

### **Backend (Flask API):**
- `backend/routes/citizen_routes.py` → API endpoints for complaint submission and tracking
- `backend/routes/admin_routes.py` → Dashboard management and analytics endpoints
- `backend/routes/ai_routes.py` → AI model integration and prediction endpoints
- `backend/routes/workflow/worker_routes.py` → Worker management and task assignment APIs
- `backend/routes/workflow/task_routes.py` → Task creation, updating, and status tracking
- `backend/routes/workflow/verification_routes.py` → YOLO-based task completion verification APIs

- `backend/models/complaint.py` → Database model for citizen complaints and issue data
- `backend/models/user.py` → User authentication and profile management model
- `backend/models/department.py` → Municipal department and routing information model
- `backend/models/worker.py` → Worker availability, skills, and assignment tracking
- `backend/models/task.py` → Task assignment, status, and completion tracking
- `backend/models/severity.py` → Issue severity levels and escalation rules
- `backend/models/detection.py` → AI detection history and accuracy tracking

- `backend/services/complaint_service.py` → Business logic for complaint processing and routing
- `backend/services/notification_service.py` → Push notifications and status update messaging
- `backend/services/routing_service.py` → Automated department assignment based on issue type
- `backend/services/workflow/worker_service.py` → Worker availability checking and optimal assignment
- `backend/services/workflow/severity_service.py` → AI-powered severity prediction and time-based escalation
- `backend/services/workflow/verification_service.py` → Task completion verification using computer vision

- `backend/utils/database.py` → PostgreSQL connection management and query utilities
- `backend/utils/auth.py` → JWT authentication and authorization helpers
- `backend/utils/postgresql_utils.py` → PostgreSQL-specific operations and PostGIS integration

### **AI/ML Components:**
- `ai_ml/models/yolo_detector.py` → YOLOv8 implementation for civic issue detection
- `ai_ml/models/issue_classifier.py` → Machine learning model for issue categorization
- `ai_ml/models/severity_predictor.py` → AI model for predicting issue severity and urgency
- `ai_ml/utils/image_processor.py` → Image preprocessing and enhancement for better detection
- `ai_ml/utils/model_utils.py` → Model loading, inference, and performance optimization
- `ai_ml/training/train_yolo.py` → Training scripts for custom YOLO model on civic issues
- `ai_ml/training/data_preparation.py` → Dataset preparation and augmentation for model training

### **Camera & Workflow Integration:**
- `camera_integration/camera_feed.py` → Laptop webcam/external camera feed management
- `camera_integration/detection_service.py` → Real-time frame processing and YOLO integration
- `workflow/issue_detection_workflow.py` → End-to-end flow from detection to server submission
- `workflow/severity_workflow.py` → Severity assessment and automatic escalation logic
- `workflow/worker_workflow.py` → Worker availability check and optimal task assignment
- `workflow/verification_workflow.py` → AI-powered task completion verification and fraud detection

### **Frontend (React):**
- `frontend/src/App.js` → Main React application component and routing setup
- `frontend/src/components/citizen/ComplaintForm.js` → User-friendly complaint submission interface
- `frontend/src/components/citizen/ComplaintTracker.js` → Real-time complaint status tracking display
- `frontend/src/components/admin/Dashboard.js` → Administrative overview with analytics and metrics
- `frontend/src/components/admin/MapView.js` → Interactive map showing all reported issues
- `frontend/src/components/admin/ComplaintManagement.js` → Complaint review, assignment, and resolution tools
- `frontend/src/components/admin/Analytics.js` → Data visualization and reporting dashboard
- `frontend/src/components/worker/WorkerDashboard.js` → Worker task list and completion interface
- `frontend/src/components/common/Header.js` → Navigation bar with user authentication
- `frontend/src/components/common/Footer.js` → Application footer with links and information

- `frontend/src/pages/Home.js` → Landing page with system overview and access points
- `frontend/src/pages/Login.js` → User authentication for citizens, workers, and admins
- `frontend/src/pages/CitizenDashboard.js` → Citizen interface for complaint management
- `frontend/src/pages/AdminDashboard.js` → Administrator control panel and system management
- `frontend/src/pages/WorkerDashboard.js` → Worker interface for task completion and updates

- `frontend/src/services/api.js` → HTTP client for backend API communication
- `frontend/src/services/auth.js` → Frontend authentication and session management

### **Database & Deployment:**
- `database/init.sql` → PostgreSQL schema creation with PostGIS for geospatial data
- `database/sample_data.sql` → Test data for departments, users, and sample complaints
- `laptop_integration/local_server.py` → Local deployment configuration without cloud dependencies
- `laptop_integration/camera_simulator.py` → Simulated camera feeds for testing without hardware
- `laptop_integration/dev_setup.py` → Development environment configuration and dependencies

### **Testing & Documentation:**
- `tests/test_backend.py` → Unit tests for Flask APIs and database operations
- `tests/test_ai_models.py` → AI model accuracy and performance testing
- `docs/API.md` → Complete API documentation with endpoints and examples
- `docs/SETUP.md` → Step-by-step installation and configuration guide
- `docs/DEPLOYMENT.md` → Production deployment instructions and best practices
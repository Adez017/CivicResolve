# CivicResolve
### AI-Powered Civic Issue Management System

CivicResolve is a full-stack platform that automates the detection, routing, and resolution of civic issues. City cameras and a mobile app feed reports into an AI-powered backend that assigns tasks to workers, tracks severity, and verifies completion — all deployable locally without cloud dependencies.

---

## How It Works

```
Camera / Citizen App → AI Detection → Server → Department Routing → Worker Assignment → Verification
```

1. **Detect** — City cameras run a YOLO model to identify issues automatically; citizens can also submit reports via the mobile app.
2. **Route** — The server classifies the issue, assigns a severity score, and routes it to the correct department.
3. **Assign** — Workers are matched to tasks based on availability and proximity.
4. **Escalate** — Unresolved issues are automatically re-prioritized over time.
5. **Verify** — Completed tasks are confirmed using computer vision before closing.
6. **Anti-Fraud** — False reporting attempts are flagged and filtered.

---

## Tech Stack

| Layer | Technology |
|---|---|
| Backend | Flask (Python) |
| Database | PostgreSQL + PostGIS |
| AI/ML | YOLOv8, TensorFlow |
| Computer Vision | OpenCV |
| Frontend | React |
| Auth | JWT |

---

## Quick Start

```bash
# 1. Clone and enter the repo
git clone https://github.com/Aditya20032004/CivicResolve && cd civicresolve

# 2. Set up environment variables
cp .env.example .env

# 3. Run automated setup
bash setup.sh

# 4. Start the application
bash run.sh
```

> **No hardware?** Use `laptop_integration/camera_simulator.py` to simulate camera feeds for local development and testing.

---

## Project Structure

```
civicresolve/
├── app.py                        # Flask entry point
├── config.py                     # DB and model config
├── requirements.txt
├── setup.sh / run.sh
│
├── backend/
│   ├── routes/
│   │   ├── citizen_routes.py     # Complaint submission & tracking
│   │   ├── admin_routes.py       # Dashboard & analytics
│   │   ├── ai_routes.py          # AI model endpoints
│   │   └── workflow/
│   │       ├── worker_routes.py  # Worker management
│   │       ├── task_routes.py    # Task lifecycle
│   │       └── verification_routes.py
│   ├── models/
│   │   ├── complaint.py
│   │   ├── user.py
│   │   ├── department.py
│   │   ├── worker.py
│   │   ├── task.py
│   │   ├── severity.py
│   │   └── detection.py
│   ├── services/
│   │   ├── complaint_service.py  # Core complaint processing logic
│   │   ├── notification_service.py
│   │   ├── routing_service.py    # Dept. assignment logic
│   │   └── workflow/
│   │       ├── worker_service.py
│   │       ├── severity_service.py
│   │       └── verification_service.py
│   └── utils/
│       ├── database.py
│       ├── auth.py
│       └── postgresql_utils.py   # PostGIS integration
│
├── ai_ml/
│   ├── models/
│   │   ├── yolo_detector.py      # YOLOv8 civic issue detection
│   │   ├── issue_classifier.py
│   │   └── severity_predictor.py
│   ├── utils/
│   │   ├── image_processor.py
│   │   └── model_utils.py
│   └── training/
│       ├── train_yolo.py
│       └── data_preparation.py
│
├── camera_integration/
│   ├── camera_feed.py            # Webcam / external camera input
│   └── detection_service.py      # Real-time YOLO frame processing
│
├── workflow/
│   ├── issue_detection_workflow.py
│   ├── severity_workflow.py
│   ├── worker_workflow.py
│   └── verification_workflow.py
│
├── frontend/
│   └── src/
│       ├── components/
│       │   ├── citizen/          # Complaint form & tracker
│       │   ├── admin/            # Dashboard, map, analytics
│       │   ├── worker/           # Task list & completion UI
│       │   └── common/           # Header, footer
│       ├── pages/                # Home, Login, role dashboards
│       └── services/             # API client & auth
│
├── database/
│   ├── init.sql                  # Schema + PostGIS setup
│   └── sample_data.sql           # Seed data for dev/testing
│
├── laptop_integration/
│   ├── local_server.py           # Cloud-free local deployment
│   ├── camera_simulator.py       # Simulated camera feeds
│   └── dev_setup.py
│
├── tests/
│   ├── test_backend.py
│   └── test_ai_models.py
│
└── docs/
    ├── API.md                    # Full endpoint reference
    ├── SETUP.md                  # Installation guide
    └── DEPLOYMENT.md             # Production deployment
```

---

## User Roles

| Role | Interface | Key Actions |
|---|---|---|
| **Citizen** | Mobile app / web | Submit & track complaints |
| **Worker** | Worker dashboard | View tasks, log completion |
| **Admin** | Admin dashboard | Monitor, assign, analyze |

---

## Documentation

- [API Reference](docs/API.md)
- [Setup Guide](docs/SETUP.md)
- [Deployment Guide](docs/DEPLOYMENT.md)

# CivicResolve API Reference

> **Base URL:** `http://localhost:5000` (development)

---

## Table of Contents

- [Root Endpoints](#root-endpoints)
- [Citizen Reporting API](#citizen-reporting-api)
- [Admin Dashboard API](#admin-dashboard-api)
- [AI Detection API](#ai-detection-api)
- [Workflow Management API](#workflow-management-api)

---

## Root Endpoints

### Health Check

**`GET /`**

Returns server status.

**Response:**
```json
{
  "message": "CivicResolve Backend is Running!",
  "status": "online"
}
```

---

### Serve Image

**`GET /data/images/<filename>`**

Serves uploaded images from the storage directory.

| Parameter  | Location | Type   | Description           |
|------------|----------|--------|-----------------------|
| `filename` | Path     | string | Name of the image file |

---

## Citizen Reporting API

**Prefix:** `/api/citizen`

### Submit Report

**`POST /api/citizen/report`**

Submit a new civic issue report (pothole or garbage) with image and location.

| Parameter      | Location | Type   | Required | Description                              |
|----------------|----------|--------|----------|------------------------------------------|
| `image`        | Form     | file   | ✅       | Image file of the issue                  |
| `type`         | Form     | string | ✅       | Issue type: `pothole` or `garbage`       |
| `lat`          | Form     | float  | Optional | Latitude coordinate                      |
| `lng`          | Form     | float  | Optional | Longitude coordinate                     |
| `address`      | Form     | string | Optional | Human-readable address                   |
| `severity`     | Form     | string | Optional | Severity level (pothole only): `low`, `medium`, `high` |
| `garbage_type` | Form     | string | Optional | Type of garbage (garbage only): `mixed`, etc. |

**Success Response (201):**
```json
{
  "message": "Report saved",
  "id": 42,
  "trust_score": 0.85,
  "validation_status": "approved"
}
```

**Error Response (400):**
```json
{
  "error": "Invalid issue type"
}
```

---

## Admin Dashboard API

**Prefix:** `/api/admin`

### Admin Index

**`GET /api/admin/`**

Returns available admin endpoints.

**Response:**
```json
{
  "message": "CivicResolve Admin API",
  "status": "active",
  "endpoints": {
    "stats": "/api/admin/stats",
    "reports": "/api/admin/reports"
  }
}
```

---

### Get All Reports

**`GET /api/admin/reports`**

Retrieves all submitted reports (potholes and garbage) sorted by creation date.

**Response:**
```json
[
  {
    "id": 1,
    "type": "pothole",
    "image_filename": "pothole_abc123.jpg",
    "severity": "high",
    "latitude": 28.6139,
    "longitude": 77.2090,
    "address": "123 Main St",
    "status": "pending",
    "created_at": "2026-02-09T14:30:00Z"
  }
]
```

---

### Get Statistics

**`GET /api/admin/stats`**

Returns total report counts by category.

**Response:**
```json
{
  "total": 156,
  "potholes": 89,
  "garbage": 67
}
```

---

## AI Detection API

**Prefix:** `/api/ai`

### Predict Issues in Image

**`POST /api/ai/predict`**

Runs YOLO-based AI model to detect civic issues in uploaded images.

| Parameter | Location | Type | Required | Description            |
|-----------|----------|------|----------|------------------------|
| `image`   | Form     | file | ✅       | Image to analyze       |

**Success Response (200):**
```json
{
  "count": 2,
  "detections": [
    {
      "class": "pothole",
      "confidence": 0.92,
      "box": [120.5, 340.2, 280.8, 520.6]
    },
    {
      "class": "garbage",
      "confidence": 0.78,
      "box": [50.1, 100.3, 150.7, 200.9]
    }
  ],
  "predictions": [...]
}
```

**Error Response (503):**
```json
{
  "error": "AI Model not ready"
}
```

---

## Workflow Management API

### Task Assignment

**Prefix:** `/api/workflow/tasks`

#### Assign Task to Worker

**`POST /api/workflow/tasks/assign`**

Assigns a report to a field worker.

| Parameter   | Location | Type   | Required | Description                   |
|-------------|----------|--------|----------|-------------------------------|
| `id`        | JSON     | int    | ✅       | Report ID                     |
| `type`      | JSON     | string | ✅       | `pothole` or `garbage`        |
| `worker_id` | JSON     | string | ✅       | Worker identifier             |

**Request Body:**
```json
{
  "id": 42,
  "type": "pothole",
  "worker_id": "worker_001"
}
```

**Response:**
```json
{
  "message": "Task assigned successfully"
}
```

---

### Worker Routes

**Prefix:** `/api/workflow/worker`

#### Get Worker's Tasks

**`GET /api/workflow/worker/my-tasks/<worker_id>`**

Retrieves all tasks assigned to a specific worker.

| Parameter   | Location | Type   | Description       |
|-------------|----------|--------|-------------------|
| `worker_id` | Path     | string | Worker identifier |

**Response:**
```json
[
  {
    "id": 5,
    "type": "pothole",
    "status": "assigned",
    "address": "456 Oak Avenue"
  }
]
```

---

#### Mark Task Complete

**`POST /api/workflow/worker/complete`**

Worker uploads proof image to mark task as completed.

| Parameter | Location | Type   | Required | Description                |
|-----------|----------|--------|----------|----------------------------|
| `image`   | Form     | file   | ✅       | After-fix image            |
| `id`      | Form     | string | ✅       | Report ID                  |
| `type`    | Form     | string | ✅       | `pothole` or `garbage`     |

**Response:**
```json
{
  "message": "Task marked completed"
}
```

---

### Verification Routes

**Prefix:** `/api/workflow/verify`

#### Verify Task Completion

**`POST /api/workflow/verify/verify`**

Admin verifies or rejects a completed task.

| Parameter  | Location | Type   | Required | Description                       |
|------------|----------|--------|----------|-----------------------------------|
| `id`       | JSON     | int    | ✅       | Report ID                         |
| `type`     | JSON     | string | ✅       | `pothole` or `garbage`            |
| `decision` | JSON     | string | ✅       | `approve` or `reject`             |
| `notes`    | JSON     | string | Optional | Verification notes                |

**Request Body:**
```json
{
  "id": 42,
  "type": "pothole",
  "decision": "approve",
  "notes": "Issue resolved properly"
}
```

**Response:**
```json
{
  "message": "Task approved"
}
```

---

## Error Codes

| Code | Meaning                                      |
|------|----------------------------------------------|
| 200  | Success                                      |
| 201  | Created                                      |
| 400  | Bad Request (missing/invalid parameters)     |
| 404  | Resource Not Found                           |
| 500  | Internal Server Error                        |
| 503  | Service Unavailable (AI model not loaded)    |

# CivicResolve Deployment Guide

Deploy CivicResolve to production environments.

---

## Table of Contents

- [Production Server (Gunicorn)](#production-server-gunicorn)
- [Docker Deployment](#docker-deployment)
- [Render Deployment](#render-deployment)
- [Environment Configuration](#environment-configuration)

---

## Production Server (Gunicorn)

Never use Flask's development server in production. Use Gunicorn instead.

### Basic Command

```bash
gunicorn backend.app:app --bind 0.0.0.0:5000 --workers 2 --timeout 120
```

### Using the Startup Script

The repository includes a production-ready startup script:

```bash
chmod +x run.sh
./run.sh
```

**`run.sh` contents:**
```bash
#!/bin/bash
PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$PROJECT_ROOT"
export PYTHONPATH="$PROJECT_ROOT:$PYTHONPATH"
gunicorn backend.app:app --bind 0.0.0.0:${PORT:-5000} --workers 2 --timeout 120
```

### Recommended Gunicorn Options

| Option       | Value          | Description                              |
|--------------|----------------|------------------------------------------|
| `--workers`  | `2-4`          | Number of worker processes               |
| `--timeout`  | `120`          | Request timeout (AI inference can be slow) |
| `--bind`     | `0.0.0.0:5000` | Host and port                            |
| `--access-logfile` | `-`     | Log to stdout                            |

---

## Docker Deployment

No Dockerfile exists in the repository. Use this template:

### Dockerfile

```dockerfile
# syntax=docker/dockerfile:1

FROM python:3.11-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PORT=5000

WORKDIR /app

# Install system dependencies for OpenCV and PyTorch
RUN apt-get update && apt-get install -y --no-install-recommends \
    libgl1-mesa-glx \
    libglib2.0-0 \
    libsm6 \
    libxext6 \
    libxrender-dev \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Create necessary directories
RUN mkdir -p database data/images logs

# Expose port
EXPOSE ${PORT}

# Run with Gunicorn
CMD ["sh", "-c", "gunicorn backend.app:app --bind 0.0.0.0:${PORT} --workers 2 --timeout 120"]
```

### Build and Run

```bash
# Build the image
docker build -t civicresolve:latest .

# Run the container
docker run -d \
  --name civicresolve \
  -p 5000:5000 \
  -v $(pwd)/data:/app/data \
  -v $(pwd)/database:/app/database \
  -e SECRET_KEY=your-production-secret \
  civicresolve:latest
```

### Docker Compose

```yaml
version: "3.8"

services:
  backend:
    build: .
    container_name: civicresolve-backend
    ports:
      - "5000:5000"
    volumes:
      - ./data:/app/data
      - ./database:/app/database
      - ./ai_ml/models:/app/ai_ml/models:ro
    environment:
      - SECRET_KEY=${SECRET_KEY:-dev-secret-key}
      - FLASK_ENV=production
    restart: unless-stopped
```

**Run with Docker Compose:**

```bash
docker compose up -d
```

---

## Render Deployment

The repository includes a `render.yaml` for one-click deployment to [Render](https://render.com).

### render.yaml

```yaml
services:
  - type: web
    name: civicresolve-backend
    env: python
    buildCommand: pip install -r requirements.txt
    startCommand: ./run.sh
    envVars:
      - key: PYTHON_VERSION
        value: 3.11.0
      - key: DATABASE_URL
        sync: false
      - key: FLASK_ENV
        value: production
```

### Deploy Steps

1. Push your code to GitHub
2. Connect your repository to Render
3. Render automatically detects `render.yaml`
4. Configure environment variables in the Render dashboard
5. Deploy

> [!IMPORTANT]
> Ensure `ai_ml/models/best_civic_model.pt` is included in your repository or use Git LFS for large files.

---

## Environment Configuration

### Production Variables

| Variable       | Description                     | Required |
|----------------|---------------------------------|----------|
| `SECRET_KEY`   | Flask secret (use strong key)   | ✅       |
| `FLASK_ENV`    | Set to `production`             | ✅       |
| `PORT`         | Server port                     | Optional |
| `DATABASE_URL` | PostgreSQL connection string    | Optional |

### Security Checklist

- [ ] Set a strong `SECRET_KEY` (generate with `python -c "import secrets; print(secrets.token_hex(32))"`)
- [ ] Use HTTPS in production (configure reverse proxy)
- [ ] Restrict `CORS_ORIGINS` in `backend/config.py`
- [ ] Enable database connection pooling for PostgreSQL
- [ ] Set up health monitoring

---

## Reverse Proxy (Nginx)

For production, place Nginx in front of Gunicorn:

```nginx
server {
    listen 80;
    server_name your-domain.com;

    client_max_body_size 16M;

    location / {
        proxy_pass http://127.0.0.1:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_read_timeout 120s;
    }

    location /data/images/ {
        alias /path/to/CivicResolve/data/images/;
        expires 30d;
    }
}
```

---

## Health Check Endpoint

Use the root endpoint for health monitoring:

```bash
curl http://localhost:5000/
```

Expected response:
```json
{
  "message": "CivicResolve Backend is Running!",
  "status": "online"
}
```

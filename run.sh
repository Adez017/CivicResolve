#!/bin/bash
# Application startup script for Render deployment

# Install Node.js dependencies
cd frontend && npm install && npm run build && cd ..

# Start Flask backend
gunicorn backend.app:app --bind 0.0.0.0:${PORT:-5000} --workers 2 --timeout 120

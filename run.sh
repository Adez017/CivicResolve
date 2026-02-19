#!/bin/bash
# Application startup script - Flask backend only

# Get the project root directory
PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$PROJECT_ROOT"

# Set Python path and start Flask backend
export PYTHONPATH="$PROJECT_ROOT:$PYTHONPATH"
gunicorn backend.app:app --bind 0.0.0.0:${PORT:-5000} --workers 2 --timeout 120

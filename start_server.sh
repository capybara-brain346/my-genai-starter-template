#!/usr/bin/bash

echo "Starting FastAPI server on port 8080..."
fastapi dev src/main.py --host 0.0.0.0 --port 8080
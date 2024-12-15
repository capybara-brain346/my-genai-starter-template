#!/usr/bin/bash

echo "Installing dependencies..."
pip install -r requirements.txt

echo "Creating .env file..."
"GOOGLE_API_KEY=Add your Google API key" > .env

echo "Build script completed successfully!"
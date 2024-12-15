#!/usr/bin/bash

# Install dependencies
echo "Installing dependencies..."
pip install -r requirements.txt

# Create .env file
echo "Creating .env file..."
echo "GOOGLE_API_KEY=" > .env

echo "Build script completed successfully!"
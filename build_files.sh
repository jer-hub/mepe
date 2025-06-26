#!/bin/bash

# Build the project
echo "Creating virtual environment..."
python3.9 -m venv python3-virtualenv
source python3-virtualenv/bin/activate

echo "Installing dependencies..."
pip install --upgrade pip
pip install -r requirements.txt

echo "Creating staticfiles_build directory..."
mkdir -p staticfiles_build

echo "Collecting static files..."
python manage.py collectstatic --noinput --clear

echo "Build completed successfully!"

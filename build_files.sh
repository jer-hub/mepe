#!/bin/bash

# Build the project
echo "Installing uv..."
pip install uv

echo "Syncing dependencies with uv (using uv.lock)..."
uv sync

echo "Creating staticfiles_build directory..."
mkdir -p staticfiles_build

echo "Collecting static files..."
uv run python manage.py collectstatic --noinput --clear

echo "Build completed successfully!"

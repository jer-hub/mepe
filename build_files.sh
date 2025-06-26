#!/bin/bash

# Build the project
echo "Installing uv..."
curl -LsSf https://astral.sh/uv/install.sh | sh
export PATH="$HOME/.cargo/bin:$PATH"

echo "Syncing dependencies with uv (using uv.lock)..."
uv sync

echo "Creating staticfiles_build directory..."
mkdir -p staticfiles_build

echo "Collecting static files..."
uv run python manage.py collectstatic --noinput --clear

echo "Build completed successfully!"

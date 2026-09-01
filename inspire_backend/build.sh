#!/usr/bin/env bash
# Exit immediately if a command exits with a non-zero status
set -o errexit

echo "Installing Python dependencies..."
pip install -r requirements.txt

echo "Collecting static assets with WhiteNoise..."
python manage.py collectstatic --no-input

echo "Applying database migrations..."
python manage.py migrate

echo "Seeding Inspire 2026 squads and competition tracks..."
python manage.py seed_inspire_data

echo "Render Build Complete!"

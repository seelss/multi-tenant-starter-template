#!/bin/bash

# Create logs directory if it doesn't exist
mkdir -p logs

echo "Applying database migrations..."
python manage.py migrate > logs/migrations.log 2>&1

echo "Starting Redis..."
redis-server --daemonize yes > logs/redis.log 2>&1

echo "Starting Celery worker..."
celery -A core worker -l info --logfile=logs/celery.log --detach

echo "Starting Celery beat..."
celery -A core beat -l info --scheduler django_celery_beat.schedulers:DatabaseScheduler --logfile=logs/celery_beat.log --detach

echo "Setting up Celery tasks for device detection..."
python manage.py setup_celery_tasks --interval 1

echo "Starting Daphne ASGI server with WebSocket support..."
daphne -b 0.0.0.0 -p 8002 core.asgi:application
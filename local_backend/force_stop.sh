#!/bin/bash

echo "Finding and forcibly terminating all Celery and Redis processes..."

# Find and kill all celery processes
ps aux | grep celery | grep -v grep | awk '{print $2}' | xargs kill -9 2>/dev/null || echo "No Celery processes found"

# Find and kill all redis-server processes
ps aux | grep redis-server | grep -v grep | awk '{print $2}' | xargs kill -9 2>/dev/null || echo "No Redis processes found"

# Kill specific Django processes related to our project
ps aux | grep "runserver 0.0.0.0:8002" | grep -v grep | awk '{print $2}' | xargs kill -9 2>/dev/null || echo "No Django processes found"

echo "All processes have been forcibly terminated."

# Verify no processes are left
echo "Verifying all processes were terminated:"
ps aux | grep -E 'celery|redis-server|runserver 0.0.0.0:8002' | grep -v grep || echo "All processes successfully terminated!" 
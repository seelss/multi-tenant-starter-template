# Device Polling with Celery

This application uses Celery for continuous device polling, which provides better reliability and integration with Django.

## Setup Instructions

### 1. Install Requirements

```bash
pip install -r requirements.txt
```

### 2. Install Redis

Redis is used as the message broker for Celery.

**macOS (using Homebrew):**
```bash
brew install redis
brew services start redis
```

**Linux (Ubuntu/Debian):**
```bash
sudo apt-get update
sudo apt-get install redis-server
sudo systemctl start redis-server
```

### 3. Set Up the Periodic Task

```bash
python manage.py migrate  # Make sure django_celery_beat tables are created
python manage.py setup_celery_tasks --interval=1
```

This sets up a periodic task to run every 1 second. You can adjust the interval as needed.

### 4. Start Celery Workers

In one terminal window, start the Celery worker:

```bash
celery -A device_manager worker --loglevel=info
```

In another terminal window, start the Celery beat scheduler:

```bash
celery -A device_manager beat --loglevel=info
```

## How It Works

1. The Celery beat scheduler triggers the `poll_for_devices` task at the specified interval
2. The task calls `DeviceDetector.scan_devices()` to check for connected devices
3. Results are logged and returned to Celery for monitoring

## Benefits Over Previous Approach

1. **Non-blocking**: Runs in separate worker processes
2. **Reliability**: Automatic retries, error handling
3. **Integration**: Better Django integration
4. **Observability**: Task results can be monitored
5. **Scalability**: Can distribute across multiple workers

## Monitoring

You can view task results in the Django admin interface by installing `django-celery-results` and adding it to your `INSTALLED_APPS`. 
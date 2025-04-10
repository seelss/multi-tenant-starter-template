# Phone Diagnostic Tool - Local Backend

This is the local backend component of the Phone Diagnostic Tool, responsible for device connectivity detection and management.

## Features

- Automatic detection of connected devices (especially iPhones)
- Captures device information (manufacturer, name, port location)
- Tracks connection status and history
- REST API for device information
- Admin interface for device management

## Requirements

- Python 3.6+
- Django 3.2+
- pyUSB 1.2+

## Installation

1. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```

2. Apply database migrations:
   ```
   python manage.py migrate
   ```

3. Create a superuser (for admin access):
   ```
   python manage.py createsuperuser
   ```

## Usage

### Running the Server

Start the Django development server:
```
python manage.py runserver
```

The server will be available at http://127.0.0.1:8000/

### Polling for Device Connections

To start the device polling service:
```
python manage.py poll_devices
```

Options:
- `--interval`: Polling interval in seconds (default: 5)

### API Endpoints

- `/api/devices/`: List all devices
- `/api/devices/connected/`: List currently connected devices
- `/api/devices/scan/`: Trigger a device scan and return results

### Admin Interface

The admin interface is available at http://127.0.0.1:8000/admin/

## Next Steps

- Implement device-specific diagnostic features
- Add cloud backend synchronization
- Package as a desktop application 
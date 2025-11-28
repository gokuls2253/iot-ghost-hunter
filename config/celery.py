import os
from celery import Celery
from celery.schedules import crontab

# Set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

# Create the application instance
app = Celery('iot_ghost_hunter')

# Load task modules from all registered Django app configs.
# namespace='CELERY' means all celery-related config keys in settings.py
# must start with 'CELERY_' (e.g., CELERY_BROKER_URL).
app.config_from_object('django.conf:settings', namespace='CELERY')

# Auto-discover tasks in all installed apps (like network/tasks.py)
app.autodiscover_tasks()

# === NEW: The Schedule ===
app.conf.beat_schedule = {
    'scan-every-5-minutes': {
        'task': 'network.tasks.scan_network',
        'schedule': 120.0,  # Run every 300 seconds (5 minutes) but now set to 120 for testing
        # Or use crontab for specific times:
        # 'schedule': crontab(minute='*/5'), 
    },
}

@app.task(bind=True)
def debug_task(self):
    print(f'Request: {self.request!r}')
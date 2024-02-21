from __future__ import absolute_import, unicode_literals
import os
from celery import Celery

# Create a Celery instance
app = Celery('api')

# Set the Django settings module
os.environ['DJANGO_SETTINGS_MODULE'] = 'backend.settings'  # Replace 'myproject' with your project name

# Load configuration from Django settings
app.config_from_object('django.conf:settings', namespace='CELERY')

# Auto-discover and register tasks
app.autodiscover_tasks()

if __name__ == '__main__':
    app.start()
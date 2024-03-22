from __future__ import absolute_import, unicode_literals
import os
from celery import Celery
from django.conf import settings

# Create a Celery instance

# Set the Django settings module
os.environ['DJANGO_SETTINGS_MODULE'] = 'backend.settings'  # Replace 'myproject' with your project name

# Load configuration from Django settings
app = Celery('backend')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.conf.enable_utc = False

app.conf.update(timezone = 'Asia/Kolkata')

app.config_from_object(settings, namespace='CELERY')
# Auto-discover and register tasks
app.autodiscover_tasks()


@app.task(bind=True)
def debug_task(self):
    print(f'Request: {self.request!r}')


if __name__ == '__main__':
    app.start()
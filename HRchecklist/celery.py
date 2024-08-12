from __future__ import absolute_import, unicode_literals
import os
from celery import Celery
from celery.schedules import crontab


# Set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'HRchecklist.settings')

app = Celery('HRchecklist')

# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
app.config_from_object('django.conf:settings', namespace='CELERY')

# Load task modules from all registered Django app configs.
app.autodiscover_tasks()

# Define periodic tasks
app.conf.beat_schedule = {
    'send-expiration-reminders-every-day': {
        'task': 'HRoperations.tasks.send_expiration_reminders',
        'schedule': crontab(hour=0, minute=0),
    },
    'send-email-to-even-id-employees-every-10-seconds': {
        'task': 'HRoperations.tasks.send_email_to_even_numbered_employees',
        'schedule': 10.0,
    },
}

@app.task(bind=True)
def debug_task(self):
    print('Request: {0!r}'.format(self.request))

from __future__ import absolute_import, unicode_literals
import os
from celery import Celery
from celery.schedules import crontab


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'your_project.settings')
app = Celery('HRoperations')

app.config_from_object('django.conf:settings', namespace='CELERY')

app.autodiscover_tasks()


app.conf.beat_schedule = {
    'send-expiration-reminders-every-day': {
        'task': 'app.tasks.send_expiration_reminders',
        'schedule': crontab(hour=0, minute=0),
    },
}
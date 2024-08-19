# myproject/celery.py
from __future__ import absolute_import, unicode_literals
import os
from celery import Celery
import ssl
from celery.schedules import crontab
from django.conf import settings
# Set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.base')

app = Celery('recipe-api')
app.conf.broker_url = settings.CELERY_BROKER_URL
app.conf.result_backend = settings.CELERY_RESULT_BACKEND
app.conf.update(
    task_serializer='json',
    result_serializer='json',
    accept_content=['json'],
    timezone='Asia/Kolkata',
    broker_use_ssl={
        'ssl_cert_reqs': ssl.CERT_NONE  # or ssl.CERT_REQUIRED if you have CA certificates
    },
    result_backend_use_ssl={
        'ssl_cert_reqs': ssl.CERT_NONE  # or ssl.CERT_REQUIRED if you have CA certificates
    }
)

app.conf.beat_schedule = {
    'send-daily-notifications': {
        'task': 'recipe.tasks.send_daily_notifications',
        'schedule': crontab(hour=1, minute=10),  
    },
}


app.config_from_object('django.conf:settings', namespace='CELERY')

# Load task modules from all registered Django app configs.
app.autodiscover_tasks()

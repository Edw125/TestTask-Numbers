import os

from celery import Celery
from celery.schedules import crontab


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'TestTask.settings')

app = Celery('TestTask')

app.config_from_object('django.conf:settings', namespace='CELERY')

app.autodiscover_tasks()

app.conf.update(result_expires=3600,
                enable_utc=True,
                timezone='Europe/Moscow', )

app.conf.beat_schedule = {
    'run-every-5-min': {
        'task': 'TestTask.celery.update_gsheet',
        'schedule': crontab(minute='*/5'),
    }
}

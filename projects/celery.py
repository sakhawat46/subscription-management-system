import os
from celery import Celery
from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'projects.settings')
app = Celery('projects')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()

app.conf.beat_schedule = {
    'fetch-usd-bdt-every-hour': {
        'task': 'apps.subscription.tasks.fetch_usd_to_bdt_rate',
        'schedule': crontab(minute=0, hour='*'),
        # 'schedule': 60.0,
    },
}

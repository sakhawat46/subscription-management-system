# import os
# from celery import Celery

# os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'projects.settings')

# app = Celery('projects')
# app.config_from_object('django.conf:settings', namespace='CELERY')
# app.autodiscover_tasks()

import os
from celery import Celery
from celery.schedules import crontab

# Django settings file এর path
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'subscription_project.settings')

# Celery app instance তৈরি
app = Celery('subscription_project')

# Django settings থেকে Celery config লোড করা
app.config_from_object('django.conf:settings', namespace='CELERY')

# Django apps থেকে স্বয়ংক্রিয়ভাবে task খুঁজে বের করা
app.autodiscover_tasks()

# Optional: Periodic task schedule (celery-beat)
app.conf.beat_schedule = {
    'fetch-usd-bdt-every-hour': {
        'task': 'core.tasks.fetch_usd_to_bdt_rate',
        'schedule': crontab(minute=0, hour='*'),  # প্রতি ঘণ্টায় একবার চালাবে
    },
}

# Optional: Timezone
# app.conf.timezone = 'Asia/Dhaka'  # তুমি চাইলে UTC ও রাখতে পারো

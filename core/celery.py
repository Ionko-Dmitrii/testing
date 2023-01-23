import os
from celery import Celery
from celery.schedules import crontab

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "core.settings")

app = Celery('core')
app.config_from_object('django.conf:settings')
app.conf.enable_utc = True

app.autodiscover_tasks()

app.conf.beat_schedule = {
    'save-questions-twice_a_minute': {
        'task': 'apps.common.tasks.save_questions',
        'schedule': crontab(minute='*', hour='*', day_of_week="*"),
    },
}

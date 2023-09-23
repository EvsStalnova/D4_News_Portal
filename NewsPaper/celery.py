import os
from celery import Celery
from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'NewsPaper.settings')

app = Celery('NewsPaper')
app.config_from_object('django.conf:settings', namespace='CELERY')

app.autodiscover_tasks()

app.conf.beat_schedule = {
    'action_every_monday_8am': {
        'task': 'News.tasks.weekly_send_email_task',
        'schedule': crontab(hour=8, minute=0, day_of_week='monday'),
        'args': ()
    },
    'action_new_post': {
        'task': 'News.tasks.new_post_send(post_id)',
        'schedule': crontab(),
        'args': ()
    },
}
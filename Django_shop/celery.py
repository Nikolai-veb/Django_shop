import os
from celery import Celery
from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODEL', 'Django_shop.settings')

app = Celery('Django_shop')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()
#
# app.conf.beat_schedule = {
#     'send-spam-every-1-minute': {
#         'task': 'orders.tasks.send_much_letters',
#         'schedule': crontab(minute='*/1'),
#     },
# }

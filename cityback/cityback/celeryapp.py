"""Celery inside django task manager."""
from __future__ import absolute_import, unicode_literals
import os
from celery import Celery
import datetime

# set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'cityback.settings')

app = Celery('cityback')

# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.
app.config_from_object('django.conf:settings', namespace='CELERY')

# Load task modules from all registered Django app configs.
app.autodiscover_tasks()
# from celery.signals import celeryd_init

# @celeryd_init.connect(sender='worker12@example.com')
# def configure_worker12(conf=None, **kwargs):

app.conf.update(
    CELERYBEAT_SCHEDULE={
        'update_stations-every-30-seconds': {
            'task': 'cityback.storage.tasks.periodic_station_update',
            'schedule': datetime.timedelta(seconds=30),
            'args': ()
        },
        'run-random-number-generator-every-1-second': {
            'task': 'cityback.dashboard.helpers.get_data',
            'schedule': datetime.timedelta(seconds=1),
            'args': ()
        }
    }
)


@app.task(bind=True)
def debug_task(self):
    """Print debug task."""
    print('Request: {0!r}'.format(self.request))

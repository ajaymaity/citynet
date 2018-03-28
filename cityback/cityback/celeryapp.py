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


app.conf.update(
    CELERYBEAT_SCHEDULE={
        'update_stations-every-60-seconds': {
            'task': 'cityback.storage.tasks.periodic_station_update',
            'schedule': datetime.timedelta(seconds=60),
            'args': ()
        },
        'realtime-demo-every-3-seconds': {
            'task':
                'cityback.dashboard.tasks.periodic_send_handler',
            'schedule': datetime.timedelta(seconds=3),
            'args': ()
        }
    }
)


@app.task(bind=True)
def debug_task(self):
    """Print debug task."""
    print('Request: {0!r}'.format(self.request))

"""Celery inside django task manager."""
from __future__ import absolute_import, unicode_literals
import os
from celery import Celery
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

# @app.on_after_configure.connect
# def setup_periodic_tasks(sender, **kwargs):
#    # Calls test('hello') every 30 seconds.
#
#    from .tasks import update_stations
#    pass
#    sender.add_periodic_task(30.0, update_stations.s(),
#                             name='Update bikes stations every 30')


@app.task(bind=True)
def debug_task(self):
    """Print debug task."""
    print('Request: {0!r}'.format(self.request))

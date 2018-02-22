import random
import json
from channels import Group

from celery import Celery
import datetime

CELERY_TIMEZONE = 'UTC'
CELERY_ENABLE_UTC = True

app = Celery('data_scheduler', broker='amqp://guest@localhost//')

@app.task
def get_data():
    a = random.randint(1, 100)
    Group("Test").send({"text": str(a)})
    print("sending data2 {}".format(a))
    return str(a)

app.conf.update(
    CELERYBEAT_SCHEDULE={
        'display-every-1-seconds': {
            'task': 'cityback.dashboard.helpers.get_data',
            'schedule': datetime.timedelta(seconds=1),
            'args': ()
        }
    }
)
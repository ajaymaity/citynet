from celery import Celery
# from celery.schedules import crontab
import datetime
CELERY_TIMEZONE = 'UTC'
CELERY_ENABLE_UTC = True
app = Celery('data_scheduler', broker='amqp://guest@localhost//')

@app.task
def test(arg):
    print("inside task", arg)
    return arg

app.conf.update(
    CELERY_BEAT_SCHEDULE={
        'display-every-3-seconds': {
            'task': 'data_scheduler.test',
            'schedule': datetime.timedelta(seconds=3),
            'args': ('hello_world', )
        }
    }
)

# @app.on_after_configure.connect
# def setup_periodic_tasks(sender, **kwargs):
#
#     # Calls test('hello') every 10 seconds.
#     sender.add_periodic_task(2.0, test.s('hello'), name='add every 2')
#
#     # Calls test('world') every 30 seconds
#     sender.add_periodic_task(3.0, test.s('world'), expires=10)
#
#     # # Executes every Monday morning at 7:30 a.m.
#     # sender.add_periodic_task(
#     #     crontab(hour=7, minute=30, day_of_week=1),
#     #     test.s('Happy Mondays!'),
#     # )
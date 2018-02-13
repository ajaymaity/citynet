from celery import Celery

app = Celery('data_preprocessing', broker='amqp://guest@localhost')

@app.task
def add(x, y):
    return x + y

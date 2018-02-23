"""All the celery tasks are defined here."""
from __future__ import absolute_import, unicode_literals

from celery import shared_task
import random
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from cityback.dashboard.models import SocketClient
from celery.signals import celeryd_init


@celeryd_init.connect(sender="celery@cityback_dev")
def reset_client_list(sender=None, conf=None, **kwargs):
    print("REMOVING ALL CLIENTS")
    SocketClient.objects.all().delete()


@shared_task
def send_random(channel_name):
    a = random.randint(1, 100)
    print("sending {}".format(a))
    # Channel(channel_name).send({"text": str(a)})


@shared_task
def periodic_send_handler():
    clients = SocketClient.objects.all()

    if len(clients) == 0:
        print("Waiting for clients")
        return

    channel_layer = get_channel_layer()
    print("sending 3 msgs")
    for i in range(3):
        a = random.randint(1, 100)
        async_to_sync(channel_layer.group_send)(
            "bike_group", {
                "type": "group.send",
                "text": str(a)}
        )
    print("done 3")

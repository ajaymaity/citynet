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
    """Run at the start of the workers to remove all clients."""
    print("REMOVING ALL CLIENTS")
    SocketClient.objects.all().delete()


@shared_task
def periodic_send_handler():
    """Send periodic data to grou bike_group."""
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

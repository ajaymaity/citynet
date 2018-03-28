"""All the celery tasks are defined here."""
from __future__ import absolute_import, unicode_literals

import asyncio
import random

import os
from asgiref.sync import async_to_sync
from celery import shared_task
from celery.signals import celeryd_init
from channels.layers import get_channel_layer


# @celeryd_init.connect("worker1@cityback_dev")
# noinspection PyUnusedLocal
@celeryd_init.connect
def reset_client_list(sender=None, conf=None, **kwargs):
    """
    Run at the start of the worker1 to remove all previous clients.

    The worker need to be called worker1 at startup
    for example: celery multi start worker1 -A cityback --beat
    """
    print("sender={}:REMOVING ALL CLIENTS, flushing redis".format(
        sender))
    # SocketClient.objects.all().delete()
    # manually remove all previous clients connected to a group.
    channel_layer = get_channel_layer()
    loop = asyncio.get_event_loop()
    loop.run_until_complete(channel_layer.flush())


@shared_task(ignore_result=True)
def periodic_send_handler():
    """Send periodic data to group bike_group."""
    channel_layer = get_channel_layer()
    text = "{}-random={}".format(
        os.environ.get("HOSTNAME", "None"),
        random.randint(1, 100))
    async_to_sync(channel_layer.group_send)(
        "bike_group", {"type": "group.send",
                       "text": text})
    print("done sending group msg {}".format(text))

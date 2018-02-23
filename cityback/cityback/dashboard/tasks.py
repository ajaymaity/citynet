"""All the celery tasks are defined here."""
from __future__ import absolute_import, unicode_literals

from celery import shared_task
import random
from channels import Channel
from channels import Group
from .models import SocketClient


@shared_task
def send_random(channel_name):
    a = random.randint(1, 100)
    print("sending {}".format(a))
    Channel(channel_name).send({"text": str(a)})


@shared_task
def periodic_send_handler():
    clients = SocketClient.objects.all()
    for client in clients:
        for i in range(100):
            a = random.randint(1, 100)
            try:
                print("sending {} to {}".format(a, client.channel_name ))
                chan = Channel(client.channel_name)
                chan.send({"text": str(a)})
                print("sent ", a)
            except:
                print("Channel full, stopping:",
                      client.channel_name)
                break
            # Group('default').discard(chan)
    if len(clients) == 0:
        print("Waiting for clients")
    # else:
    #     a = random.randint(1, 100)
    #     cl = Group("Test").channel_layer
    # print("cl=", cl)
    # if cl is None:
    #     print("Wainting for clients")
    # else:
    #     a = random.randint(1, 100)
    #     print("sending {} to Group Test".format(a))
    #     Group("Test").send({"text": str(a)})

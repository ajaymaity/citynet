import json
from channels import Group
from .tasks import send_random
from .models import SocketClient
from django.core.exceptions import ObjectDoesNotExist


def ws_connect(message):
    print("connected to channel '{}'".format(message.reply_channel.name))

    Group("Test").add(message.reply_channel)
    # validate connection
    message.reply_channel.send({
        'accept': True
    })
    SocketClient.objects.get_or_create(
        channel_name=message.reply_channel.name
    )


def ws_receive(message):
    data = json.loads(message.content.get("text"))
    print("received data:", data.get("data"))
    #helpers.get_data()
    #val = str(helpers.get_data())
    # val = "42"
    # Group("Test").send({"text": val})
    # send_random.delay(message.reply_channel.name)
    return None


def ws_disconnect(message):
    """On closed, delete db object."""
    Group("Test").discard(message.reply_channel)
    try:
        client = SocketClient.objects.get(
            channel_name=message.reply_channel.name)
        client.delete()

    except ObjectDoesNotExist:
        pass

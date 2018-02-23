# import json
# from channels import Group
# from .tasks import send_random
from .models import SocketClient
from django.core.exceptions import ObjectDoesNotExist
from channels.generic.websocket import WebsocketConsumer
from asgiref.sync import async_to_sync


class ClientSocketConsumer(WebsocketConsumer):

    def connect(self):
        # Called on connection. Either call
        self.accept()
        # self.send({ "type": "websocket.accept", })
        async_to_sync(self.channel_layer.group_add)(
            "bike_group", self.channel_name)
        SocketClient.objects.get_or_create(channel_name=self.channel_name)

    def receive(self, text_data=None, bytes_data=None):
        print("received data:", text_data, bytes_data)
        # self.send(text_data="TOTO")
        # text_data = "Hello Group member!"
        # async_to_sync(self.channel_layer.group_send)(
        #     "bike_group",
        #     {
        #         "type": "group.send",
        #         "text": text_data,
        #     },
        # )

    def group_send(self, event):
        self.send(text_data=event["text"])

    def disconnect(self, close_code):
        # Called when the socket close
        async_to_sync(self.channel_layer.group_discard)(
            "bike_group", self.channel_name)
        try:
            client = SocketClient.objects.get(channel_name=self.channel_name)
            client.delete()
        except ObjectDoesNotExist:
            pass


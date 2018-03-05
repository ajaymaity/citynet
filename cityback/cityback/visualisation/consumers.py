"""Socket consumers."""
from channels.generic.websocket import WebsocketConsumer
from asgiref.sync import async_to_sync


class RTStationsConsumer(WebsocketConsumer):
    """Define the consumer for bikes clients."""

    def connect(self):
        """On connection, add to group."""
        # Called on connection. Either call
        self.accept()
        async_to_sync(self.channel_layer.group_add)(
            "stationUpdateGroup", self.channel_name)
        print("New client to RTstations")

    def receive(self, text_data=None, bytes_data=None):
        """On message reveice, display message."""
        print("received data:", text_data, bytes_data)
        pass

    def group_send(self, event):
        """
        Send group messages.

        A group send is handled by this functions for each
        client.
        """
        self.send(text_data=event["text"])

    def disconnect(self, close_code):
        """When the socket close."""
        async_to_sync(self.channel_layer.group_discard)(
            "stationUpdateGroup", self.channel_name)
        print("Disconnected Client to RTstations")

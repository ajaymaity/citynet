"""Socket consumers."""
import json

from channels.generic.websocket import WebsocketConsumer
from asgiref.sync import async_to_sync

from cityback.storage.apps import getBikesTimeRange
from cityback.visualisation.apps import getLatestStationJSON


class RTStationsConsumer(WebsocketConsumer):
    """Define the consumer for bikes clients."""

    def send_time_range(self, size=3600):
        """Send time range to the js client."""
        timeRange = getBikesTimeRange()
        number = int((timeRange[1] - timeRange[0]).total_seconds() / size)
        data = {"type": "timeRange",
                "begin": timeRange[0].strftime("%Y-%M-%d %H:%m:%S"),
                "end": timeRange[1].strftime("%Y-%M-%d %H:%m:%S"),
                'nbIntervals': number}
        self.send(text_data=json.dumps(data))

    def send_bikes_at_time(self, text_data):
        """Send the bikes at specific time to the js client."""
        dateTime = text_data.get("dateTime", None)
        if dateTime is None:
            return
        data = {"type": "mapAtTime",
                "value": dateTime}
        self.send(text_data=json.dumps(data))

    def connect(self):
        """On connection, add to group."""
        # Called on connection. Either call
        self.accept()
        async_to_sync(self.channel_layer.group_add)(
            "stationUpdateGroup", self.channel_name)

        self.send(text_data=getLatestStationJSON())
        print("New client to RTstations")

    def receive(self, text_data=None, bytes_data=None):
        """On message reveice, display message."""
        print("received data:", text_data, bytes_data)
        text_data = json.loads(text_data)
        if type(text_data) == dict:
            if "type" in text_data:
                if text_data['type'] == "getTimeRange":
                    self.send_time_range()
                if text_data['type'] == "getMapAtTime":
                    self.send_bikes_at_time(text_data)
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

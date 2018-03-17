"""Socket consumers."""
import json

from channels.generic.websocket import WebsocketConsumer
from asgiref.sync import async_to_sync

from cityback.storage.apps import getBikesTimeRange, getBikesAtTime, \
    getCompressedBikeUpdates
from cityback.visualisation.apps import getLatestStationJSON, convertToGeoJson
from datetime import timedelta
import datetime


class RTStationsConsumer(WebsocketConsumer):
    """Define the consumer for bikes clients."""

    format = "%Y-%m-%d %H:%M"

    def send_time_range(self, size=60):
        """Send time range to the js client."""
        start, end = getBikesTimeRange()
        if start is None or end is None:
            # TODO make a real log
            print("No data provided in Get time range")
            return
        number = int((end - start).total_seconds() / size)
        times = []
        for i in range(number - 1):
            times.append((start + timedelta(seconds=size * i)
                          ).strftime(self.format))
        times.append(end.strftime(self.format))

        data = {"type": "timeRange",
                'nbIntervals': number,
                'dateTimeOfIndex': times}
        self.send(text_data=json.dumps(data))
        # distinctTimes = getBikesDistinctTimes()

    def send_bikes_at_time(self, text_data):
        """Send the bikes at specific time to the js client."""
        dateTime = text_data.get("dateTime", None)
        if dateTime is None:
            return
        dateTime = datetime.datetime.strptime(
                dateTime, "%Y-%m-%d %H:%M").replace(
                tzinfo=datetime.timezone.utc)
        data = {"type": "mapAtTime",
                "value": convertToGeoJson(getBikesAtTime(dateTime))}
        self.send(text_data=json.dumps(data))

    def send_test_chart(self, time_delta_s=3600):
        """Tmp function to get first chart."""
        times, occupancy = getCompressedBikeUpdates(
            time_delta_s=time_delta_s)
        if len(times) == 0:
            return
        data = json.dumps({"type": "chart",
                           "labels": [t.strftime(self.format) for t in times],
                           "occupancy": occupancy.tolist(),
                           "time_delta_s": time_delta_s})
        print("Send chart data")
        self.send(text_data=data)

    def connect(self):
        """On connection, add to group."""
        # Called on connection. Either call
        self.accept()
        async_to_sync(self.channel_layer.group_add)(
            "stationUpdateGroup", self.channel_name)

        self.send(text_data=getLatestStationJSON())
        self.send_test_chart(300)
        print("New client to RTstations")

    def receive(self, text_data=None, bytes_data=None):
        """On message reveice, display message."""
        print("consumer received message:", text_data)
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

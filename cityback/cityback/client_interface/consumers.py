"""Socket consumers."""
import datetime
import json

from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer

from cityback.historical_analysis.apps import HistoricAnalysis
from cityback.client_interface.conversion import convertToGeoJson
from cityback.forecast_engine.apps import forecast_occupancy


class RTStationsConsumer(WebsocketConsumer):
    """Define the consumer for bikes clients."""

    format = "%Y-%m-%d %H:%M"

    def send_time_range(self, delta_s=60):
        """Send time range to the js client."""
        date_list = HistoricAnalysis.getBikesDistinctTimes(delta_s=delta_s)
        times = [d.strftime(self.format) for d in date_list]

        data = {"type": "timeRange",
                'nbIntervals': len(times),
                'dateTimeOfIndex': times}
        self.send(text_data=json.dumps(data))

    def send_bikes_at_time(self, text_data):
        """Send the bikes at specific time to the js client."""
        dateTime = text_data.get("dateTime", None)
        if dateTime is None:
            return
        delta_s = text_data.get("deltaS", None)
        if delta_s is None:
            return
        delta_s = int(delta_s)
        dateTime = HistoricAnalysis.floorTime(datetime.datetime.strptime(
                dateTime, "%Y-%m-%d %H:%M").replace(
                tzinfo=datetime.timezone.utc), delta_s)
        data = {"type": "mapAtTime",
                "value": convertToGeoJson(HistoricAnalysis.getBikesAtTime(
                    dateTime, delta_s))}
        self.send(text_data=json.dumps(data))

    def send_historic_chart(self, station_id, time_delta_s=3600):
        """Tmp function to get first chart."""
        times, occupancy = HistoricAnalysis.getCompressedBikeUpdates(
            stations=[station_id],
            time_delta_s=time_delta_s)
        print("len of times =", len(times))
        if not times or len(times) == 0:
            return
        data = json.dumps({"type": "chart",
                           "selectionType": "station",
                           "selectionId": station_id,
                           "labels": [t.strftime(self.format) for t in times],
                           # "station":
                           "occupancy": occupancy,
                           "time_delta_s": time_delta_s})
        print("Send chart data")
        self.send(text_data=data)

    def connect(self):
        """On connection, add to group."""
        # Called on connection. Either call
        self.accept()
        async_to_sync(self.channel_layer.group_add)(
            "stationUpdateGroup", self.channel_name)

        # TODO re enable periodic realtime data
        # TODO add a type to the message

        # self.send(text_data=getLatestStationJSON())
        # self.send_historic_chart(time_delta_s=5 * 60)
        print("New client to RTstations")

    def receive(self, text_data=None, bytes_data=None):
        """On message reveice, display message."""
        print("consumer received message:", text_data)
        text_data = json.loads(text_data)
        if type(text_data) == dict:
            if "type" in text_data:
                if text_data['type'] == "getTimeRange":
                    self.send_time_range(int(text_data['deltaS']))
                if text_data['type'] == "getMapAtTime":
                    self.send_bikes_at_time(text_data)
                if text_data['type'] == "getChartWithDelta":
                    self.send_historic_chart(
                        station_id=26,
                        time_delta_s=int(text_data['deltaS']))
                if text_data['type'] == "polygonData":
                    self.get_polygon_data(
                        text_data["selectedPolygon"],
                        int(text_data['deltaS']))
                if text_data['type'] == "stationSelect":
                    self.send_historic_chart(
                        int(text_data["stationId"]),
                        int(text_data['deltaS']))
                if text_data['type'] == "getForecast":
                    self.send_forecast_chart(
                        text_data["start"],
                        int(text_data['length']),
                        [int(s) for s in text_data['stations']])

    def get_polygon_data(self, polygon_dict, delta_s):
        """Get updated chart from selected polygon."""
        print("deltaS ", delta_s)
        stations_list = HistoricAnalysis.get_stations_from_polygon(
            polygon_dict['polygon'])
        times, occupancy = HistoricAnalysis.getCompressedBikeUpdates(
            stations=stations_list,
            time_delta_s=delta_s)
        if not times or len(times) == 0:
            data = {"type": "chart"}
            self.send(text_data=json.dumps(data))
            return
        data = json.dumps({"type": "chart",
                           "selectionType": "polygon",
                           "selectionId": polygon_dict['id'],
                           "labels": [t.strftime(self.format) for t in times],
                           "occupancy": occupancy,
                           "time_delta_s": delta_s})
        print("Send chart data")
        self.send(text_data=data)

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

    def send_forecast_chart(self, start, length, stations):
        """Send the bikes at specific time to the js client."""
        startTime = datetime.datetime.strptime(
            start, "%Y-%m-%d %H:%M").replace(
            tzinfo=datetime.timezone.utc)

        print("stations=", stations)
        stations_list, forecasts = forecast_occupancy(length, stations,
                                                      startTime)
        date_list = [startTime + datetime.timedelta(minutes=x + 1)
                     for x in range(length)]
        data = json.dumps({"type": "multichart",
                           "selectionType": "forecast",
                           "selectionsId": stations_list,
                           "labels": [t.strftime(self.format)
                                      for t in date_list],
                           # "station":
                           "occupancy": forecasts,
                           "time_delta_s": 60})
        print("Send forecast data")
        self.send(text_data=data)

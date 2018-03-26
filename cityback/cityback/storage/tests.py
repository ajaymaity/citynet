"""Tests related to the storage module."""
import datetime

from django.test import TestCase
import json
from cityback.storage.models import (
    DublinBikesStation, DublinBikesStationRealTimeUpdate)
from cityback.storage.apps import update_stations, getLatestStationsFromDB, \
    floorTime, get_stations_from_polygon
from cityback.storage.apps import getBikesTimeRange, getDateTimeFromTimeStampMS
import os


class BikeStationsTest(TestCase):
    """Test the Dublin bike stations access."""

    def setUp(self):
        """Fill db with test data."""
        self.stations = json.load(open(os.path.join(
            os.path.dirname(os.path.abspath(__file__)),
            "test_data.json")))
        self.stations_multiple = json.load(open(os.path.join(
            os.path.dirname(os.path.abspath(__file__)),
            "test_data_multiple.json")))


class CorrectUpdateTest(BikeStationsTest):
    """Testing correct static data update."""

    def runTest(self):
        """Correctly update values."""
        s1 = self.stations[0]
        update_stations(self.stations)
        s2 = DublinBikesStation.objects.get(station_number=s1["number"])
        self.assertEqual(s1['name'], s2.name)

        s1["address"] = "Test Road"
        update_stations([s1])
        s2 = DublinBikesStation.objects.get(station_number=s1["number"])
        self.assertEqual(s1['address'], s2.address)


class CorrectRealTimeInsertTest(BikeStationsTest):
    """Testing if realtime data is inserted correctly."""

    def runTest(self):
        """Correctly insert values."""
        s1 = self.stations[0]
        update_stations(self.stations)
        dublin_static_object = DublinBikesStation.objects.get(
            station_number=s1["number"])
        s2 = DublinBikesStationRealTimeUpdate.objects.get(
            parent_station=dublin_static_object)
        self.assertEqual(s2.station_last_update,
                         datetime.datetime.utcfromtimestamp(
                             s1['last_update']/1000).replace(
                             tzinfo=datetime.timezone.utc))
# DublinBikesStation.objects.all()


class InCorrectRealTimeUpdateTest(BikeStationsTest):
    """Testing new dynamic data with same timestamp and station=> no update."""

    def runTest(self):
        """Correctly check and not update values."""
        s1 = self.stations[0]
        timestamp = max(
            [getDateTimeFromTimeStampMS(station['last_update'])
             for station in self.stations])
        timestamp = floorTime(timestamp, 60)
        update_stations(self.stations[:10], timestamp)
        s1['status'] = 'Test'
        update_stations([s1], timestamp)
        dublin_static_object = DublinBikesStation.objects.get(
            station_number=s1["number"])
        s2 = DublinBikesStationRealTimeUpdate.objects.filter(
            parent_station=dublin_static_object,
            station_last_update=datetime.datetime.utcfromtimestamp
            (s1['last_update']/1000).replace(
                tzinfo=datetime.timezone.utc)).order_by('timestamp')[0]

        self.assertNotEqual(s2.status, 'Test')


class CorrectRealTimeUpdateTest(BikeStationsTest):
    """Testing new dynamic data with new timestamp and station.

    => insert the new data.
    """

    def runTest(self):
        """Correctly update the real time values."""
        s1 = self.stations[0]
        timestamp = floorTime(datetime.datetime.now(), 60)
        update_stations(self.stations[:10], timestamp)
        s1['status'] = 'Test'
        update_stations([s1], timestamp + datetime.timedelta(minutes=1))
        dublin_static_object = DublinBikesStation.objects.get(
            station_number=s1["number"])
        s2 = DublinBikesStationRealTimeUpdate.objects.filter(
            parent_station=dublin_static_object,
            station_last_update=datetime.datetime.utcfromtimestamp
            (s1['last_update']/1000).replace(
                tzinfo=datetime.timezone.utc)).order_by('-timestamp')[0]
        self.assertEqual(s2.status, 'Test')


class GetStations(BikeStationsTest):
    """Testing getting stations from DB."""

    def runTest(self):
        """Get dynamic and static data."""
        update_stations(self.stations[:10])
        # TODO: Implement!
        getLatestStationsFromDB()


class GetLattestStationsFromDBTest(BikeStationsTest):
    """Testing latest stations fetch from DB."""

    def runTest(self):
        """Test the retrieval of the latest stations."""
        update_stations([s for s in self.stations_multiple
                         if s['number'] in [1, 2, 3]])
        bikes_static = DublinBikesStation.objects.all()
        latest_bikes = []
        for bike_static in bikes_static:
            bikes_real = bike_static.dublinbikesstationrealtimeupdate_set.all()
            max_latest_update = datetime.datetime.utcfromtimestamp(0).replace(
                tzinfo=datetime.timezone.utc)
            latest_bikes_real = None
            for bike_real in bikes_real:
                if bike_real.station_last_update > max_latest_update:
                    max_latest_update = bike_real.station_last_update
                    latest_bikes_real = bike_real

            latest_bikes.append({
                "station_number": bike_static.station_number,
                "latitude": bike_static.position.coords[1],
                "longitude": bike_static.position.coords[0],
                "name": bike_static.name,
                "status": latest_bikes_real.status,
                "timestamp": latest_bikes_real.timestamp,
                "station_last_update":
                    latest_bikes_real.station_last_update.replace(
                        tzinfo=datetime.timezone.utc
                    ),
                "available_bikes": float(latest_bikes_real.available_bikes),
                "available_bike_stands":
                    float(latest_bikes_real.available_bike_stands),
                "bike_stands": float(latest_bikes_real.bike_stands)
            })

        ground_truth_bike = sorted(latest_bikes,
                                   key=lambda x: x["station_number"])
        ground_truth_bike = [
            d[k] for d in ground_truth_bike for k in sorted(d.keys())
        ]
        latest_bikes = sorted(getLatestStationsFromDB(),
                              key=lambda x: x["station_number"])
        latest_bikes = [
            d[k] for d in latest_bikes for k in sorted(d.keys())
        ]
        # print(latest_bikes)
        self.assertEqual(ground_truth_bike, latest_bikes)


class GetStationsTimeRange(BikeStationsTest):
    """Testing bikes time range."""

    def runTest(self):
        """Get dynamic and static data."""
        stations = self.stations_multiple[:100]
        for station in stations:
            timestamp = getDateTimeFromTimeStampMS(
                station['last_update'])
            update_stations([station], timestamp)
        range2 = getBikesTimeRange()
        times = [floorTime(getDateTimeFromTimeStampMS(s["last_update"]),
                           60).replace(tzinfo=datetime.timezone.utc)
                 for s in stations]
        range1 = (min(times), max(times))
        self.assertEqual(range1, range2)


class GetStationsFromPolygonTest(BikeStationsTest):
    """Station Ids from polygon testcase."""

    def runTest(self):
        """Test with dummy data."""
        update_stations(self.stations)

        dict_in = {"type": "polygonData",
                   "selectedPolygons":
                       {"bf886b5448015cccd9874e4c18ab8963":
                        "POLYGON((-6.250526108576906 53.34958844643552, "
                        "-6.237612656663856 53.349697785865345, "
                        "-6.237612656663856 53.344831909748194,"
                        "-6.248602828503806 53.34319160163423, "
                        "-6.250526108576906 53.34958844643552))"}}

        list_out = {64, 49, 8, 99, 65, 62, 48}
        test_out = get_stations_from_polygon(dict_in["selectedPolygons"])
        self.assertEqual(set(test_out), list_out)

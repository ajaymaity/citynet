"""Tests related to the storage module."""
import datetime

from django.test import TestCase
import json
from cityback.storage.models import (
    DublinBikesStation, DublinBikesStationRealTimeUpdate)
from cityback.storage.apps import update_stations, getLattestStationsFromDB
import cityback.storage.apps as apps
import os


class BikeStationsTest(TestCase):
    """Test the Dublin bike stations access."""

    def setUp(self):
        """Fill db with test data."""
        self.stations = json.load(open(os.path.join(
            os.path.dirname(os.path.abspath(__file__)),
            "test_data.json")))


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
        self.assertEqual(s2.last_update, datetime.datetime.utcfromtimestamp(
            s1['last_update']/1000).replace(
                    tzinfo=datetime.timezone.utc))
# DublinBikesStation.objects.all()


class InCorrectRealTimeUpdateTest(BikeStationsTest):
    """Testing new dynamic data with same timestamp and station=> no update."""

    def runTest(self):
        """Correctly check and not update values."""
        s1 = self.stations[0]
        update_stations(self.stations)
        s1['status'] = 'Test'
        update_stations([s1])
        dublin_static_object = DublinBikesStation.objects.get(
            station_number=s1["number"])
        s2 = DublinBikesStationRealTimeUpdate.objects.get(
            parent_station=dublin_static_object,
            last_update=datetime.datetime.utcfromtimestamp
            (s1['last_update']/1000).replace(
                    tzinfo=datetime.timezone.utc))
        self.assertNotEqual(s2.status, 'Test')


class CorrectRealTimeUpdateTest(BikeStationsTest):
    """Testing new dynamic data with new timestamp and station.

    => insert the new data.
    """

    def runTest(self):
        """Correctly update the real time values."""
        s1 = self.stations[0]
        update_stations(self.stations)
        s1['status'] = 'Test'
        s1['last_update'] = 1519141942000  # changed timestamp
        update_stations([s1])
        dublin_static_object = DublinBikesStation.objects.get(
            station_number=s1["number"])
        s2 = DublinBikesStationRealTimeUpdate.objects.get(
            parent_station=dublin_static_object,
            last_update=datetime.datetime.utcfromtimestamp
            (s1['last_update']/1000).replace(
                    tzinfo=datetime.timezone.utc))
        self.assertEqual(s2.status, 'Test')


class GetStations(BikeStationsTest):
    """Testing getting stations from DB."""

    def runTest(self):
        """Get dynamic and static data."""
        update_stations(self.stations)
        apps.getLattestStationsFromDB()


class GetLattestStationsFromDBTest(BikeStationsTest):
    """Testing latest stations fetch from DB."""

    def runTest(self):
        """
        Update the bike information in DB from json.

        First, update the list of existing stations
        then update the bike information for all stations.

        :param station_list: a list of stations dict
        :return:
        """
        update_stations(self.stations)
        bikes_static = DublinBikesStation.objects.all()
        latest_bikes = []
        for bike_static in bikes_static:
            # TODO: Change the way of getting the lattest station update
            bikes_real = bike_static.dublinbikesstationrealtimeupdate_set.all()
            max_latest_update = datetime.datetime.utcfromtimestamp(0).replace(
                tzinfo=datetime.timezone.utc)
            latest_bikes_real = None
            for bike_real in bikes_real:
                if (bike_real.last_update > max_latest_update):
                    max_latest_update = bike_real.last_update
                    latest_bikes_real = bike_real

            latest_bikes.append({
                "station_number": bike_static.station_number,
                "latitude": bike_static.latitude,
                "longitude": bike_static.longitude,
                "name": bike_static.name,
                "status": latest_bikes_real.status,
                "last_update": latest_bikes_real.last_update,
                "available_bikes": latest_bikes_real.available_bikes,
                "available_bike_stands": latest_bikes_real.
                available_bike_stands,
                "bike_stands": latest_bikes_real.bike_stands
            })

        ground_truth_bike = latest_bikes
        latest_bikes = getLattestStationsFromDB()
        # print(latest_bikes)
        self.assertEqual(ground_truth_bike, latest_bikes)

"""Tests related to the storage module."""

from django.test import TestCase
import json
from cityback.storage.models import (
    DublinBikesStation, DublinBikesStationRealTimeUpdate)
from cityback.storage.apps import update_stations
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
        self.assertEqual(s2.last_update, str(s1['last_update']))


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
            parent_station=dublin_static_object, last_update=s1['last_update'])
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
        s1['last_update'] = '1519141941001'  # changed timestamp
        update_stations([s1])
        dublin_static_object = DublinBikesStation.objects.get(
            station_number=s1["number"])
        s2 = DublinBikesStationRealTimeUpdate.objects.get(
            parent_station=dublin_static_object, last_update=s1['last_update'])
        self.assertEqual(s2.status, 'Test')


class GetStations(BikeStationsTest):
    """Testing getting stations from DB."""

    def runTest(self):
        """Get dynamic and static data."""
        update_stations(self.stations)
        apps.get_stations()

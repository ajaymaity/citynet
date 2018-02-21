"""Tests related to the storage module."""
from django.test import TestCase
import json
from cityback.storage.models import DublinBikesStation
from cityback.storage.apps import update_stations
import os


class BikeStationsTest(TestCase):
    """Test the Dublin bike stations access."""

    def setUp(self):
        """Fill db with test data."""
        self.stations = json.load(open(os.path.join(
            os.path.dirname(os.path.abspath(__file__)),
            "test_data.json")))
        for s1 in self.stations:
            DublinBikesStation.objects.create(
                station_number=s1["number"],
                latitude=s1['position']['lat'],
                longitude=s1['position']['lng'],
                name=s1['name'],
                address=s1['address'],
                bonus=s1['bonus'],
                contract_name=s1['contract_name'],
                banking=s1['banking']
            )

    def test_correct_update(self):
        """Correctly update values."""
        s1 = self.stations[0]
        s2 = DublinBikesStation.objects.get(station_number=s1["number"])
        self.assertEqual(s1['name'], s2.name)

        s1["address"] = "Test Road"
        update_stations([s1])
        s2 = DublinBikesStation.objects.get(station_number=s1["number"])
        self.assertEqual(s1['address'], s2.address)

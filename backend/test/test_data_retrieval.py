#!/usr/bin/python
# coding=utf-8
"""Test cases for the data retrieval part."""

import unittest
from cityback.data_retrieval import DataRetrieval


class TestDataRetrieval(unittest.TestCase):
    """Test the access key."""

    def test_api(self):
        """Check the connectivity using the Dublin bikes key."""
        dataRetrieval = DataRetrieval()
        self.assertTrue(dataRetrieval.get_apikey().endswith("47b20"))
        self.assertTrue(dataRetrieval.check_connectivity())

    def test_static_retrieval(self):
        """Check static data retrieval objects."""
        dataRetrieval = DataRetrieval()
        stationsInfo = dataRetrieval.get_static_data()
        keysList = ["number", "longitude", "address", "latitude", "name"]
        for stationInfo in stationsInfo:
            keys = stationInfo.keys()
            self.assertEqual(set(keys), set(keysList))

    def test_dynamic_retrieval(self):
        """Check dynamic data retrieval objects."""
        dataRetrieval = DataRetrieval()
        stationsData = dataRetrieval.get_dynamic_data()
        keysList = ["number", "last_update", "status", "banking", "available_bikes", "contract_name", "bonus", "available_bike_stands", "bike_stands"]
        for stationInfo in stationsData:
            keys = stationInfo.keys()
            self.assertEqual(set(keys), set(keysList))

if __name__ == '__main__':
    unittest.main()

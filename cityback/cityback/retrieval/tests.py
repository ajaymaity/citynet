"""Tests for Bikes Retrieval."""
from django.test import TestCase
from cityback.retrieval.data_retrieval import BikesRetrieval
from unittest import mock
from requests.models import Response
import json


def ordered(obj):
    """Order JSON objects."""
    if isinstance(obj, dict):
        return sorted((k, ordered(v)) for k, v in obj.items())
    if isinstance(obj, list):
        return sorted(ordered(x) for x in obj)
    else:
        return obj


def mocked_requests_get(*args, **kwargs):
    """Mock Requests GET operations."""
    response = Response()
    url = 'https://api.jcdecaux.com/vls/v1/stations?contract=Dublin&apiKey='
    if args[0].startswith(url):
        with open("cityback/storage/test_data.json", "r") as json_file:
            json_response = json.load(json_file)
        response._content = json.dumps(json_response).encode("utf-8")
        response.status_code = 200
        return response


class GetStationsListFromContractTest(TestCase):
    """Stations list from contract testcase."""

    @mock.patch('requests.get', side_effect=mocked_requests_get)
    def test_fetch(self, mock_get):
        """Test with dummy data."""
        contract_name = "Dublin"

        with open("cityback/storage/test_data.json", "r") as json_file:
            json_response = json.load(json_file)

        bikes_retrieval = BikesRetrieval()
        stations = bikes_retrieval.get_stations_list_from_contract(
            contract_name)

        self.assertEqual(ordered(stations), ordered(json_response))

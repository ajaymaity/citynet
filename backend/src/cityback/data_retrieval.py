"""Hello World file testing data retrieval for the Dublin bikes."""

import requests
import logging



__all__ = ["get_stations_list_from_contract", "get_apikey",
           "get_json_from_url", "get_contracts"]

class DataRetrieval:

    def __init__(self):

        # TODO move this API to a secure external configuration file
        self.dbikes_apikey = '3665c1ce997b7a7d4384ea241251b2f606647b20'

        self.BIKES_URL = dict(
            contracts="https://api.jcdecaux.com/vls/v1/contracts?apiKey={api_key:}",
            station_info=("https://api.jcdecaux.com/vls/v1/stations/{"
                          "station_number:}?"
                          "contract={:contract_name}&apiKey={api_key:}"),
            stations_list="https://api.jcdecaux.com/vls/v1/stations?apiKey={api_key:}",
            stations_from_contract="https://api.jcdecaux.com/vls/v1/stations?contract"
                                   "={contract_name:}&apiKey={api_key:}",
            static_stations_Dublin="https://developer.jcdecaux.com/rest/vls/stations"
                                   "/Dublin.json")

    def get_json_from_url(self, url):
        """Get the json response from a url, log if error."""
        response = requests.get(url)
        if response.status_code != 200:
            logging.error("Response {} from server when accessing url {}".format(
                response.status_code, url))
            return None
        return response.json(encoding='utf-8')


    def get_contracts(self):
        """Retrieve the list of contracts from the API."""
        url = self.BIKES_URL["contracts"].format(api_key=self.dbikes_apikey)
        return self.get_json_from_url(url)


    def get_stations_list_from_contract(self, contract):
        """Get the json of all the stations of a contract."""
        url = self.BIKES_URL["stations_from_contract"].format(
            contract_name=contract, api_key=self.dbikes_apikey)
        stations = self.get_json_from_url(url)
        return stations


    def check_connectivity(self):
        """Verify that the key is working by listing the station information."""
        contracts = self.get_contracts()
        if contracts is None:
            return False
        contracts = [c for c in contracts if c['name'] == "Dublin"]
        if len(contracts) == 0:
            return False

        stations = self.get_stations_list_from_contract(contracts[0]['name'])
        if stations is None:
            return False
        return True

    def get_static_data(self):
        """Get static Dublin Bikes data."""
        url = self.BIKES_URL["static_stations_Dublin"].format(api_key=self.dbikes_apikey)
        return self.get_json_from_url(url)

    def get_dynamic_data(self):
        """Get dynamic Dublin Bikes data."""
        contracts = self.get_contracts()
        contract = [c for c in contracts if c['name'] == "Dublin"]
        stations = self.get_stations_list_from_contract(contract[0]['name'])

        deleteList = ["position", "address", "name"]
        for station in stations:
            for d in deleteList:
                del station[d]
        return stations

    def get_apikey(self):
        """Return the api access key."""
        return self.dbikes_apikey
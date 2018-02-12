"""Hello World file testing data retrieval for the Dublin bikes."""

import requests
dbikes_apikey = '3665c1ce997b7a7d4384ea241251b2f606647b20'

__all__ = ["get_dbikes_stations", "get_apikey"]


def get_dbikes_stations():
    """Retrieve the raw json from the api."""
    url = ('https://api.jcdecaux.com/vls/v1/stations?contract=Dublin&apiKey={}'
           ''.format(dbikes_apikey))
    response = requests.get(url)
    dbikes_stations = response.json()
    return dbikes_stations


def get_apikey():
    """Return the api access key."""
    return dbikes_apikey


# DEBUGGING
if __name__ == '__main__':

    print(get_dbikes_stations())

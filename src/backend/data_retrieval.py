import requests

dbikes_apikey = '3665c1ce997b7a7d4384ea241251b2f606647b20'

def get_dbikes_stations():

    url = 'https://api.jcdecaux.com/vls/v1/stations?contract=Dublin&apiKey={}'.format(dbikes_apikey)
    response = requests.get(url)
    dbikes_stations = response.json()
    return dbikes_stations

# DEBUGGING
if __name__ == '__main__':

    print(get_dbikes_stations())
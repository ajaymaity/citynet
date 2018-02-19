"""All the celery tasks are defined here."""
from __future__ import absolute_import, unicode_literals

from cityback.retrieval.data_retrieval import BikesRetrieval
from .models_bikes import DublinBikesStation
from celery import shared_task


@shared_task
def test_task():
    """Print test."""
    print("TEST!")
    return 42


# @shared_task
def update_stations():
    """
    Update the bike information in DB from json.

    First, update the list of existing stations
    then update the bike information for all stations.

    :param station_json:
    :return:
    """
    # {'status': 'OPEN', 'bonus': False, 'address': 'Smithfield North',
    #  'banking': True, 'bike_stands': 30,
    # 'last_update': 1518777566000, 'available_bike_stands': 29,
    # 'contract_name': 'Dublin',
    # 'position': {'lat': 53.349562, 'lng': -6.278198},
    # 'number': 42, 'available_bikes': 1,
    # 'name': 'SMITHFIELD NORTH'}

    bikes = BikesRetrieval()
    stations = bikes.get_dynamic_data()
    for station in stations:
        station_number = station['number']
        latitude = station['position']['lat']
        longitude = station['position']['lng']
        name = station['name']
        address = station['address']
        # import ipdb; ipdb.set_trace()
        object, created = DublinBikesStation.objects.get_or_create(
            station_number=station_number,
            latitude=latitude,
            longitude=longitude,
            name=name,
            address=address,
            bonus=station['bonus']
        )
        print("object={}, created={}".format(object, created))
    return "Update_stations: {} stations updated!".format(len(stations))

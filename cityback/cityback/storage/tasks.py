"""All the celery tasks are defined here."""
from __future__ import absolute_import, unicode_literals
from cityback.retrieval.data_retrieval import BikesRetrieval
from .models import DublinBikesStation
from celery import shared_task


@shared_task
def test_task(param=""):
    """Print test."""
    print("TEST!" + param)
    return 42


@shared_task
def periodic_station_update():
    """Retreive station and update in db."""
    bikes = BikesRetrieval()
    stations = bikes.get_dynamic_data()
    update_stations(stations)


def update_stations(stations):
    """
    Update the bike information in DB from json.

    First, update the list of existing stations
    then update the bike information for all stations.

    :param station_list: a list of stations dict
    :return:
    """
    # {'status': 'OPEN', 'bonus': False, 'address': 'Smithfield North',
    #  'banking': True, 'bike_stands': 30,
    # 'last_update': 1518777566000, 'available_bike_stands': 29,
    # 'contract_name': 'Dublin',
    # 'position': {'lat': 53.349562, 'lng': -6.278198},
    # 'number': 42, 'available_bikes': 1,
    # 'name': 'SMITHFIELD NORTH'}

    for station in stations:
        object, created = DublinBikesStation.objects.update_or_create(
            station_number=station['number'],
            defaults=dict(
                latitude=station['position']['lat'],
                longitude=station['position']['lng'],
                name=station['name'],
                address=station['address'],
                bonus=station['bonus'],
                contract_name=station['contract_name'],
                banking=station['banking']
            ))

    return "Update_stations: {} stations updated!".format(len(stations))

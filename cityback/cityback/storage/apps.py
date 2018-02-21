"""TODO."""

from django.apps import AppConfig
from cityback.storage.models import (
    DublinBikesStation, DublinBikesStationRealTimeUpdate)


class StorageConfig(AppConfig):
    """TODO."""

    name = 'storage'


def update_stations(stations):
    """
    Update the bike information in DB from json.

    First, update the list of existing stations
    then update the bike information for all stations.

    :param station_list: a list of stations dict
    :return:
    """
    objects = {}

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
            )
        )
        objects[station['number']] = object

        # print("object={}, created={}".format(object, created))

    for station in stations:
        object, created = (
            DublinBikesStationRealTimeUpdate.objects.get_or_create(
                parent_station=objects[station['number']],
                last_update=station['last_update'],
                defaults=dict(
                    status=station['status'],
                    # last_update=station['position']['lng'],
                    available_bikes=station['available_bikes'],
                    available_bike_stands=station['available_bike_stands'],
                    bike_stands=station['bike_stands'],
                )
            ))

    return "Update_stations: {} stations updated!".format(len(stations))

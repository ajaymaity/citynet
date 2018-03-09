"""TODO."""
import datetime

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
                last_update=datetime.datetime.utcfromtimestamp(
                    float(station['last_update'])/1000.).replace(
                    tzinfo=datetime.timezone.utc),
                defaults=dict(
                    status=station['status'],
                    available_bikes=station['available_bikes'],
                    available_bike_stands=station['available_bike_stands'],
                    bike_stands=station['bike_stands'],
                )
            ))

    return "Update_stations: {} stations updated!".format(len(stations))


def getLattestStationsFromDB():
    """
    Update the bike information in DB from json.

    First, update the list of existing stations
    then update the bike information for all stations.

    :param station_list: a list of stations dict
    :return:
    """
    bikes_station = DublinBikesStation.objects.raw(
        '''select station_number, latitude, longitude, name, status,
          available_bikes, available_bike_stands, bike_stands,
          sub_query.last_update from storage_dublinbikesstation
inner join (
select  max(id) as id, parent_station_id, max(last_update) as last_update from
            storage_dublinbikesstationrealtimeupdate
            group by parent_station_id)
as sub_query
    on  storage_dublinbikesstation.station_number =
sub_query.parent_station_id
inner join storage_dublinbikesstationrealtimeupdate on
sub_query.parent_station_id = station_number AND
sub_query.id =
storage_dublinbikesstationrealtimeupdate.id;
''')
    latest_bikes = []
    for bikes in bikes_station:
        # TODO: Change the way of getting the lattest station update

        last_update = bikes.last_update
        if type(last_update) != str:
            last_update = last_update.isoformat()
        else:
            # import ipdb; ipdb.set_trace()
            last_update = datetime.datetime.strptime(
                last_update, "%Y-%m-%d %H:%M:%S").replace(
                tzinfo=datetime.timezone.utc)
            last_update = last_update.isoformat()
        latest_bikes.append({
            "station_number": bikes.station_number,
            "latitude": bikes.latitude,
            "longitude": bikes.longitude,
            "name": bikes.name,
            "status": bikes.status,
            "last_update": last_update,
            "available_bikes": bikes.available_bikes,
            "available_bike_stands": bikes.available_bike_stands,
            "bike_stands": bikes.bike_stands
        })

    # print(latest_bikes)
    return latest_bikes

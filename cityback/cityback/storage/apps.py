"""TODO."""
import time
from datetime import timedelta, datetime, timezone

from django.apps import AppConfig
from cityback.storage.models import (
    DublinBikesStation, DublinBikesStationRealTimeUpdate)
from django.db.models import Max, Min
import numpy as np


class StorageConfig(AppConfig):
    """TODO."""

    name = 'storage'


def update_stations(stations):
    """
    Update the bike information in DB from json.

    First, update the list of existing stations
    then update the bike information for all stations.

    :param station: a list of stations dict
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

    for station in stations:
        object, created = (
            DublinBikesStationRealTimeUpdate.objects.get_or_create(
                parent_station=objects[station['number']],
                last_update=getDateTimeFromTimeStampMS(station['last_update']),
                defaults=dict(
                    status=station['status'],
                    available_bikes=station['available_bikes'],
                    available_bike_stands=station['available_bike_stands'],
                    bike_stands=station['bike_stands'],
                )
            ))

    return "Update_stations: {} stations updated!".format(len(stations))


def getDateTimeFromTimeStampMS(timestamp):
    """Convert timestamp in milisecond to datetime object."""
    return datetime.utcfromtimestamp(
        float(timestamp) / 1000.).replace(
        tzinfo=timezone.utc)


def getLatestStationsFromDB():
    """
    Retrieve the lattest information for every stations.

    :return: list of dict
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
            last_update = datetime.strptime(
                last_update, "%Y-%m-%d %H:%M:%S").replace(
                tzinfo=timezone.utc)
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


def getBikesAtTime(dateTime):
    """
    Retrieve the information for every stations at or just less than dateTime.

    :return: list of dict
    """
    bikes_station = DublinBikesStation.objects.raw(
        '''select station_number, latitude, longitude, name, status,
          available_bikes, available_bike_stands, bike_stands,
          sub_query.last_update from storage_dublinbikesstation
inner join (
select  max(id) as id, parent_station_id, max(last_update) as last_update from
            storage_dublinbikesstationrealtimeupdate
            where last_update <= \'''' +
        dateTime +
        '''\' group by parent_station_id)
as sub_query
    on  storage_dublinbikesstation.station_number =
sub_query.parent_station_id
inner join storage_dublinbikesstationrealtimeupdate on
sub_query.parent_station_id = station_number AND
sub_query.id =
storage_dublinbikesstationrealtimeupdate.id;
''')
    bikes_at_time = []
    for bikes in bikes_station:
        last_update = bikes.last_update
        if type(last_update) != str:
            last_update = last_update.isoformat()
        else:
            last_update = datetime.strptime(
                last_update, "%Y-%m-%d %H:%M:%S").replace(
                tzinfo=timezone.utc)
            last_update = last_update.isoformat()
        bikes_at_time.append({
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
    return bikes_at_time


def getBikesTimeRange():
    """
    Get the time range available for the bike updates.

    :return: tuple first, last timestamp in string iso format
    """
    times = DublinBikesStationRealTimeUpdate.objects.all().aggregate(
        Min('last_update'), Max('last_update'))

    startTime = times['last_update__min']
    lastTime = times['last_update__max']

    print(startTime, lastTime)
    return startTime, lastTime


def roundTime(dt=None, round_to=60):
    """Round a datetime object to any time laps in seconds.

    dt : datetime.datetime object, default now.
    roundTo : Closest number of seconds to round to, default 1 minute.
    Author: Thierry Husson 2012 - Use it as you want but don't blame me.
    """
    if dt is None:
        dt = datetime.now()
    dt = dt.replace(tzinfo=None)
    seconds = (dt - dt.min).seconds
    #  this is a floor division, not a comment on following line:
    rounding = (seconds + round_to / 2) // round_to * round_to
    return dt + timedelta(0, rounding - seconds, -dt.microsecond)


def getBikesDistinctTimes(time_delta_s=60):
    """Get all distinct bike times."""
    # times = DublinBikesStationRealTimeUpdate.objects.raw(
    #     '''select id, last_update from
    #         storage_dublinbikesstationrealtimeupdate
    #     ''')

    # times = DublinBikesStationRealTimeUpdate.objects.annotate(
    #         rounded_time=(
    #         roundTime(F('last_update'), 3600)
    #     )
    # )
    # before optimisation: 2.22s
    # after raw sql + python round: 1.8s
    # with pure sql rounding, tuned 0.54s

    start = time.time()
    times = DublinBikesStationRealTimeUpdate.objects.raw('''
        select 1 as id, rdate from (select DISTINCT
        date_round(last_update, '{} seconds') as rdate
        from storage_dublinbikesstationrealtimeupdate) as foo
        order by rdate
        '''.format(time_delta_s))
    times = [t.rdate.replace(tzinfo=None) for t in times]
    end = time.time()
    print("query distinct times took: {}s".format(end - start))
    return times


def getCompressedBikeUpdates(stations=[1], time_delta_s=3600):
    """Get bike update average over the specified delta and stations."""
    start = time.time()
    times = getBikesDistinctTimes(time_delta_s)
    all = DublinBikesStationRealTimeUpdate.objects.all().filter(
        parent_station__in=stations).only(
        'last_update', 'available_bikes', 'bike_stands')
    print(all.count())
    print(len(times))
    #    create 2 numpy array len(times) by 1
    # first is data
    # second is % occupancy
    occupancy = np.zeros((len(times)), dtype=np.float64)
    counts = np.zeros((len(times)), dtype=np.int64)

    for data in all:
        rounded_time = roundTime(data.last_update)
        try:
            idx = times.index(rounded_time)
        except ValueError:
            continue
        stands = data.bike_stands
        if stands != 0:
            occupancy[idx] += (float(data.available_bikes) * 100 /
                               stands)
            counts[idx] += 1

    total = counts.sum()
    empty = counts == 0
    counts[empty] = 1
    occupancy /= counts
    # interpolate
    if len(occupancy) == 0:
        return times, occupancy
    fill = occupancy[0]
    for i in range(occupancy.shape[0]):
        if empty[i]:
            occupancy[i] = fill
        else:
            fill = occupancy[i]
    end = time.time()
    print("computed {} values in {}s".format(
        total,
        end - start
    ))
    return times, occupancy

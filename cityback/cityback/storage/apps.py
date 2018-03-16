"""TODO."""
import time
from datetime import timedelta, datetime, timezone

from django.apps import AppConfig
from django.contrib.gis.geos import Point

from cityback.storage.models import (
    DublinBikesStation, DublinBikesStationRealTimeUpdate)
from django.contrib.gis.db.models import Max, Min


class StorageConfig(AppConfig):
    """TODO."""

    name = 'storage'


def update_stations(stations, timestamp=None):
    """
    Update the bike information in DB from json.

    First, update the list of existing stations
    then update the bike information for all stations.

    :param station  a list of stations dict
    :param now if true insert with current time rounded to nearest minute
           else, get the most recent station_timestamp, rounded to minute
    :return:
    """
    time_delta = 60
    # TODO refactor time_delta

    # get the timestamp for the data
    if timestamp is None:
        timestamp = datetime.now()
    timestamp = roundTime(timestamp, time_delta)

    # insert data between end to now, both exclusive.
    start, end = getBikesTimeRange()
    if start is not None and end is not None:
        end = roundTime(end, 60)
        num_dates = (timestamp - end) // timedelta(seconds=time_delta)
        date_list = [start + timedelta(seconds=(time_delta * x))
                     for x in range(1, num_dates)]
        stations_at_end = getBikesAtTime(end, time_delta)
        objects = []
        for time_ in date_list:
            for station in stations_at_end:
                objects.append(DublinBikesStationRealTimeUpdate(
                    parent_station=objects[station['number']],
                    timestamp=time_.replace(tzinfo=timezone.utc),
                    station_last_update=station['station_last_update'],
                    status=station['status'],
                    available_bikes=station['available_bikes'],
                    available_bike_stands=station['available_bike_stands'],
                    bike_stands=station['bike_stands']
                ))
        DublinBikesStationRealTimeUpdate.objects.bulk_create(objects)
        # print("Filled holes for {} time steps".format(len(date_list)))

    # update the stations at time timestamp.
    for station in stations:
        point = Point(
            station['position']['lng'],
            station['position']['lat'],
            srid=4326  # WGS 84
        )
        station_object, created = DublinBikesStation.objects.update_or_create(
            station_number=station['number'],
            defaults=dict(
                position=point,
                name=station['name'],
                address=station['address'],
                bonus=station['bonus'],
                contract_name=station['contract_name'],
                banking=station['banking']
            )
        )
        # print("timestamp=", timestamp)
        obj, created = DublinBikesStationRealTimeUpdate.objects.get_or_create(
            parent_station=station_object,
            timestamp=timestamp.replace(tzinfo=timezone.utc),
            defaults=dict(
                station_last_update=(
                    getDateTimeFromTimeStampMS(station['last_update'])),
                status=station['status'],
                available_bikes=station['available_bikes'],
                available_bike_stands=station['available_bike_stands'],
                bike_stands=station['bike_stands'],
            )
        )

        # print("created", created, "obj", obj)

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
        '''select 'position', station_number, name, status,
          available_bikes, available_bike_stands, bike_stands,
          sub_query.timestamp, station_last_update
           from storage_dublinbikesstation
inner join (
select  max(id) as id, parent_station_id, max(timestamp) as timestamp from
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

        last_update = bikes.station_last_update
        if type(last_update) != str:
            last_update = last_update.isoformat()
        else:
            last_update = datetime.strptime(
                last_update, "%Y-%m-%d %H:%M:%S").replace(
                tzinfo=timezone.utc)
            last_update = last_update.isoformat()
        latest_bikes.append({
            "station_number": bikes.station_number,
            "latitude": bikes.position.coords[1],
            "longitude": bikes.position.coords[0],
            "name": bikes.name,
            "status": bikes.status,
            "timestamp": bikes.timestamp,
            "station_last_update": last_update,
            "available_bikes": bikes.available_bikes,
            "available_bike_stands": bikes.available_bike_stands,
            "bike_stands": bikes.bike_stands
        })

    # print(latest_bikes)
    return latest_bikes


def getBikesAtTime(date_time, time_delta=60):
    """
    Retrieve the information for every stations at date_time.

    :return: list of dict
    """
    date_time = roundTime(date_time, time_delta)
    bikes_station = DublinBikesStation.objects.raw(
        '''select station_number, 'position', 'name', status,
          available_bikes, available_bike_stands, bike_stands,
          sub_query.last_update from storage_dublinbikesstation
inner join (
select  max(id) as id, parent_station_id, max(station_last_update) as
last_update from
            storage_dublinbikesstationrealtimeupdate
            where 'timestamp'='{}' group by parent_station_id)
as sub_query
    on  storage_dublinbikesstation.station_number =
sub_query.parent_station_id
inner join storage_dublinbikesstationrealtimeupdate on
sub_query.parent_station_id = station_number AND
sub_query.id =
storage_dublinbikesstationrealtimeupdate.id;
'''.format(date_time.isoformat()))
    bikes_at_time = []
    for bikes in bikes_station:
        bikes_at_time.append({
            "station_number": bikes.station_number,
            "latitude": bikes.position.coords[1],
            "longitude": bikes.position.coords[0],
            "name": bikes.name,
            "status": bikes.status,
            "timestamp": date_time,
            "station_last_update": bikes.last_update,
            "available_bikes": bikes.available_bikes,
            "available_bike_stands": bikes.available_bike_stands,
            "bike_stands": bikes.bike_stands
        })

    # print(latest_bikes)
    return bikes_at_time


def getBikesTimeRange():
    """
    Get the time range available for the bike updates.

    :return: tuple first, last timestamp as timestamp object
    """
    times = DublinBikesStationRealTimeUpdate.objects.all().aggregate(
        Min('timestamp'), Max('timestamp'))

    startTime = times['timestamp__min']
    lastTime = times['timestamp__max']

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
        date_round(station_last_update, '{} seconds') as rdate
        from storage_dublinbikesstationrealtimeupdate) as foo
        order by rdate
        '''.format(time_delta_s))
    times = [t.rdate.replace(tzinfo=None) for t in times]
    end = time.time()
    print("query distinct times took: {}s".format(end - start))
    return times


def getCompressedBikeUpdates(stations=[1], time_delta_s=3600):
    """Get bike update average over the specified delta and stations."""
    times = getBikesDistinctTimes(time_delta_s)
    return None, None
    # all = DublinBikesStationRealTimeUpdate.objects.all().filter(
    #     parent_station__in=stations).only(
    #     'last_update', 'available_bikes', 'bike_stands')
    times = DublinBikesStationRealTimeUpdate.objects.raw('''
        select 1 as id, rdate from (select DISTINCT
        date_round(station_last_update, '{} seconds') as rdate
        from storage_dublinbikesstationrealtimeupdate) as foo
        order by rdate
        '''.format(time_delta_s))
    times = [t.rdate.replace(tzinfo=None) for t in times]

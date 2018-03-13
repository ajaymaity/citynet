"""TODO."""
from datetime import timedelta, datetime

from django.apps import AppConfig
from cityback.storage.models import (
    DublinBikesStation, DublinBikesStationRealTimeUpdate)
from django.db.models import Func, F


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
    return datetime.datetime.utcfromtimestamp(
                    float(timestamp) / 1000.).replace(
                    tzinfo=datetime.timezone.utc)


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
            last_update = datetime.datetime.strptime(
                last_update, "%Y-%m-%d %H:%M:%S").replace(
                tzinfo=datetime.timezone.utc)
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
    times = DublinBikesStationRealTimeUpdate.objects.annotate(
        min_field=Func(F('last_update'), function='MIN'))

    timesmax = DublinBikesStationRealTimeUpdate.objects.annotate(
        max_field=Func(F('last_update'), function='MAX'))

    startTime = list(times)[0].min_field
    lastTime = list(timesmax)[0].max_field

    return startTime, lastTime


# class RoundTime(Func)
#     function = 'ROUNDTIME'
#     def __init__(self, datetime, **extra):
#         pass
#     def as_postgresql(selfself, compiler, connection):
#         return self.as_sql(compiler, connection, function=)

#    CREATE FUNCTION date_round(base_date timestamptz, round_interval INTERVAL) RETURNS timestamptz AS $BODY$
# SELECT TO_TIMESTAMP((EXTRACT(epoch FROM $1)::INTEGER + EXTRACT(epoch FROM $2)::INTEGER / 2)
#                 / EXTRACT(epoch FROM $2)::INTEGER * EXTRACT(epoch FROM $2)::INTEGER)
# $BODY$ LANGUAGE SQL STABLE;


def roundTime(dt=None, roundTo=60):
   """Round a datetime object to any time laps in seconds
   dt : datetime.datetime object, default now.
   roundTo : Closest number of seconds to round to, default 1 minute.
   Author: Thierry Husson 2012 - Use it as you want but don't blame me.
   """
   if dt == None : dt = datetime.datetime.now()
   dt = dt.replace(tzinfo=None)
   seconds = (dt - dt.min).seconds
   # // is a floor division, not a comment on following line:
   rounding = (seconds+roundTo/2) // roundTo * roundTo
   return dt + timedelta(0,rounding-seconds,-dt.microsecond)


def getBikesDistinctTimes():
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
    times = DublinBikesStationRealTimeUpdate.objects.only(
        'last_update').distinct()
    times = sorted(list(set(roundTime(t.last_update) for t in times)))
    for time in times:
        print(time)
        # print("{} {} {}".format(
        #     time.id,
        #     time.last_update,
        #     roundTime(time.last_update)
        # ))

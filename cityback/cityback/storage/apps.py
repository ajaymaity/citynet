"""TODO."""
from datetime import timedelta, datetime, timezone

from django.apps import AppConfig
from django.contrib.gis.geos import Point
from django.db import connection
from django.db.models import Max, Min

from cityback.storage.models import (
    DublinBikesStation, DublinBikesStationRealTimeUpdate)
import time


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
        date_list = [end + timedelta(seconds=(time_delta * x))
                     for x in range(1, num_dates)]

        if len(date_list):
            print("num dates={}".format(num_dates))
            print("Filling holes in db, from {} to {}".format(
                date_list[0], date_list[-1]))

        stations_at_end = getBikesAtTime(end, time_delta)
        objects = []
        for time_ in date_list:
            for station in stations_at_end:
                objects.append(DublinBikesStationRealTimeUpdate(
                    parent_station_id=station['station_number'],
                    timestamp=time_.replace(tzinfo=timezone.utc),
                    station_last_update=station['station_last_update'],
                    status=station['status'],
                    available_bikes=station['available_bikes'],
                    available_bike_stands=station['available_bike_stands'],
                    bike_stands=station['bike_stands']
                ))
        DublinBikesStationRealTimeUpdate.objects.bulk_create(objects, 1000)
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
        last_update = station['last_update']
        last_update = (getDateTimeFromTimeStampMS(last_update)
                       if last_update is not None else timestamp.now())
        obj, created = DublinBikesStationRealTimeUpdate.objects.get_or_create(
            parent_station=station_object,
            timestamp=timestamp.replace(tzinfo=timezone.utc),
            defaults=dict(
                station_last_update=last_update,
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
    _, end = getBikesTimeRange()
    return getBikesAtTime(end)


def getBikesAtTime(date_time, time_delta=60):
    """
    Retrieve the information for every stations at date_time.

    :return: list of dict
    """
    timer_start = time.time()
    date_time = roundTime(date_time, time_delta)
    print("getBikesAtTime=", time_delta)
    # for raw queries of geometry fields, see documentation at
    # https://docs.djangoproject.com/en/2.0/ref/contrib/gis/tutorial/
    query = '''select station_number, name, status, {} as position,
          available_bikes, available_bike_stands, bike_stands,
          station_last_update
          from storage_dublinbikesstation
         INNER JOIN
         (SELECT
          parent_station_id,
          avg(available_bikes) as available_bikes,
          avg(bike_stands) as bike_stands,
          avg(available_bike_stands) as available_bike_stands,
          max(station_last_update) as station_last_update,
          max(status) as status
        FROM storage_dublinbikesstationrealtimeupdate
        WHERE timestamp BETWEEN '{}' and '{}'
        GROUP BY parent_station_id
        ) as avg_updates
    on station_number = avg_updates.parent_station_id;
'''.format(
        (connection.ops.select % 'position'),
        date_time.isoformat(),
        (date_time + timedelta(seconds=time_delta)).isoformat()
        )

    bikes_station = DublinBikesStation.objects.raw(query)
    bikes_at_time = []
    for bikes in bikes_station:
        bikes_at_time.append({
            "station_number": bikes.station_number,
            "latitude": bikes.position.coords[1],
            "longitude": bikes.position.coords[0],
            "name": bikes.name,
            "status": bikes.status,
            "station_last_update": bikes.station_last_update,
            "timestamp": date_time.replace(tzinfo=timezone.utc),
            "available_bikes": float(bikes.available_bikes),
            "available_bike_stands": float(
                bikes.available_bike_stands),
            "bike_stands": float(bikes.bike_stands)
        })

    print("GetBikesAtTime took {:.03f}s".format(time.time() - timer_start))
    return bikes_at_time


def getBikesTimeRange():
    """
    Get the time range available for the bike updates.

    :return: tuple first, last timestamp as timestamp object
    """
    start_timer = time.time()

    times = DublinBikesStationRealTimeUpdate.objects.all().aggregate(
        Max('timestamp'), Min('timestamp'))

    if times is not None:
        startTime = times['timestamp__min']
        lastTime = times['timestamp__max']

        print("get bike time range took: {}s".format(time.time()
                                                     - start_timer))
        return startTime, lastTime

    else:
        return None, None


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


def getBikesDistinctTimes(delta_s=60):
    """Get all distinct bike times."""
    start, end = getBikesTimeRange()
    start, end = roundTime(start, delta_s), roundTime(end, delta_s)
    num_dates = (end - start) // timedelta(seconds=delta_s) + 1
    date_list = [start + timedelta(seconds=(delta_s * x))
                 for x in range(num_dates)]
    # print("query distinct times took: {}s".format(time.time() - start_timer))
    return date_list


def getCompressedBikeUpdates(stations=[21], time_delta_s=3600):
    """Get bike update average over the specified delta and stations."""
    times = DublinBikesStationRealTimeUpdate.objects.raw('''
        select 1 as id, avg(available_bikes::float / bike_stands::float)
        as avg_occupancy,
        date_floor(timestamp, '{} seconds') as rdate
        from storage_dublinbikesstationrealtimeupdate
        WHERE parent_station_id in ({})
        and bike_stands <> 0
        group by rdate
        order by rdate
        '''.format(
        time_delta_s,
        ",".join([str(s) for s in stations]))
    )

    return (
        [t.rdate.replace(tzinfo=None) for t in times],
        [float(t.avg_occupancy) * 100 for t in times])

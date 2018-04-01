"""Functions related to Historic and Spatial analysis of bikes."""
from datetime import timedelta, timezone
from django.contrib.gis.geos import GEOSGeometry
from django.db import connection
from django.db.models import Max, Min
from cityback.storage.models import DublinBikesStation, \
    DublinBikesStationRealTimeUpdate


class HistoricAnalysis(object):
    """Contain functions processing the historic data of bikes."""

    @staticmethod
    def get_stations_from_polygon(polygon):
        """Get station ids present within the polygon."""
        poly = GEOSGeometry(polygon)
        stations = DublinBikesStation.objects.all().filter(
            position__within=poly
        ).values_list("station_number", flat=True)
        return list(stations)

    @staticmethod
    def floorTime(dt, round_to=60):
        """Round a datetime object to any time laps in seconds.

        dt : datetime.datetime object, default now.
        roundTo : Closest number of seconds to round to, default 1 minute.
        Author: Thierry Husson 2012 - Use it as you want but don't blame me.
        """
        dt = dt.replace(tzinfo=None)
        seconds = (dt - dt.min).seconds
        #  this is a floor division, not a comment on following line:
        rounding = seconds // round_to * round_to
        return dt + timedelta(0, rounding - seconds, -dt.microsecond)

    @staticmethod
    def getBikesAtTime(date_time, time_delta=60):
        """
        Retrieve the information for every stations at date_time.

        :return: list of dict
        """
        # timer_start = time.time()
        date_time = HistoricAnalysis.floorTime(date_time, time_delta)
        # print("getBikesAtTime=", time_delta)
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
            WHERE timestamp >= '{}' and  timestamp < '{}'
            GROUP BY parent_station_id
            ) as avg_updates
        on station_number = avg_updates.parent_station_id
        order by station_number;
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

        return bikes_at_time

    @staticmethod
    def getBikesTimeRange():
        """
        Get the time range available for the bike updates.

        :return: tuple first, last timestamp as timestamp object
        """
        # start_timer = time.time()

        times = DublinBikesStationRealTimeUpdate.objects.all().aggregate(
            Max('timestamp'), Min('timestamp'))

        startTime = times['timestamp__min']
        lastTime = times['timestamp__max']

        # print("get bike time range took: {}s".format(time.time()
        #                                              - start_timer))
        return startTime, lastTime

    @staticmethod
    def getBikesDistinctTimes(delta_s=60):
        """Get all distinct bike times."""
        start, end = HistoricAnalysis.getBikesTimeRange()
        if start is None or end is None:
            return []
        start, end = (HistoricAnalysis.floorTime(start, delta_s),
                      HistoricAnalysis.floorTime(end, delta_s))
        num_dates = (end - start) // timedelta(seconds=delta_s) + 1
        date_list = [start + timedelta(seconds=(delta_s * x))
                     for x in range(num_dates)]
        return date_list

    @staticmethod
    def getCompressedBikeUpdates(
            stations, time_delta_s=3600, length_limit=4000):
        """Get bike update average over the specified delta and stations."""
        if not stations:
            return None, None
        # import time
        # stopwatch_start = time.time()
        print(type(stations))
        print(stations)
        assert type(stations) == list
        assert type(length_limit) == int

        times = list(DublinBikesStationRealTimeUpdate.objects.raw('''
            with t as (select
             avg(available_bikes::float / bike_stands::float) as avg_occupancy,
             date_floor(timestamp, '{} seconds') as rdate
            from storage_dublinbikesstationrealtimeupdate
            WHERE parent_station_id in ({})
            and bike_stands <> 0
            group by rdate
            order by rdate DESC
            limit {})
            select 1 as id, * from t ORDER BY rdate ASC
            '''.format(
            time_delta_s,
            ",".join([str(s) for s in stations]), length_limit)
        ))

        results = (
            [t.rdate.replace(tzinfo=None) for t in times],
            [float(t.avg_occupancy) * 100 for t in times])
        return results

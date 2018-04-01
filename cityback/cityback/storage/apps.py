"""TODO."""
from datetime import datetime, timedelta, timezone

from django.apps import AppConfig
from django.contrib.gis.geos import Point
from twisted.test.test_sob import objects

from cityback.data_storage.models import (
    DublinBikesStation, DublinBikesStationRealTimeUpdate)
from cityback.historical_analysis.apps import HistoricAnalysis


class StorageConfig(AppConfig):
    """TODO."""

    # noinspection PyUnresolvedReferences
    name = 'data_storage'


class RealTimeProcessing():

    @staticmethod
    def update_stations(stations, timestamp=None):
        """
        Update the bike information in DB from json.

        First, update the list of existing stations
        then update the bike information for all stations.

        :param stations  a list of stations dict
        :param timestamp if true insert with current time rounded to nearest minute
        else, get the most recent station_timestamp, rounded to minute
        :return:
        """
        time_delta = 60
        # TODO refactor time_delta

        # get the timestamp for the data
        if timestamp is None:
            timestamp = datetime.now()
        timestamp = HistoricAnalysis.floorTime(timestamp,
                                               time_delta)

        # insert data between end to now, both exclusive.
        start, end = HistoricAnalysis.getBikesTimeRange()
        if start is not None and end is not None:
            end = HistoricAnalysis.floorTime(end, 60)
            num_dates = (timestamp - end) // timedelta(seconds=time_delta)
            date_list = [end + timedelta(seconds=(time_delta * x))
                         for x in range(1, num_dates)]

            if len(date_list):
                print("num dates={}".format(num_dates))
                print("Filling holes in db, from {} to {}".format(
                    date_list[0], date_list[-1]))

            stations_at_end = HistoricAnalysis.getBikesAtTime(
                end, time_delta)
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
            last_update = (
                RealTimeProcessing.getDateTimeFromTimeStampMS(last_update)
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

    @staticmethod
    def getDateTimeFromTimeStampMS(timestamp):
        """Convert timestamp in milisecond to datetime object."""
        return datetime.utcfromtimestamp(
            float(timestamp) / 1000.).replace(
            tzinfo=timezone.utc)

    @staticmethod
    def getLatestStationsFromDB():
        """
        Retrieve the latest information for every stations.

        :return: list of dict
        """
        _, end = HistoricAnalysis.getBikesTimeRange()
        return HistoricAnalysis.getBikesAtTime(end)
    pass
















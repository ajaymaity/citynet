"""Forecast module."""
import itertools
import time
from cityback.storage.models import DublinBikesStationRealTimeUpdate
from .models import DublinBikesStationAverage


def date_hour_min(timestamp):
    """Convert to hour min format."""
    return timestamp.strftime("%H:%M:00")


def averageModel():
    """CALCULATE AVERAGE EVERY MINUTE FOR ALL STATIONS."""
    all_stations = DublinBikesStationRealTimeUpdate.objects.all()
    distinct_stations = all_stations.\
        order_by("parent_station__station_number").\
        distinct("parent_station__station_number")
    start = time.time()
    bulk_objs = []
    for station in distinct_stations:
        print("***** ", station.parent_station_id,
              " *****")
        stations = all_stations.filter(
            parent_station__station_number__exact=station.parent_station_id)

        objs = stations.order_by("station_last_update")
        groups_by_minute = itertools.groupby(objs,
                                             lambda x: date_hour_min(
                                              x.station_last_update))

        total_times = 0
        for groups_by_minute, matches in groups_by_minute:
            total_times += 1
            sum_available_bikes = 0
            len_available_bikes = 0
            for match in matches:
                len_available_bikes += 1
                sum_available_bikes += match.available_bikes
            avg_available_bikes = sum_available_bikes / len_available_bikes
            # DublinBikesStationAverage.objects.get_or_create(stations,groups_by_minute,avg_available_bikes)
            bulk_objs.append(DublinBikesStationAverage(
                parent_station=station.parent_station,
                time=groups_by_minute,
                avg_available_bikes=avg_available_bikes
            ))

            print(groups_by_minute, avg_available_bikes)
        print("Distinct times: ", total_times)

    all_objects = DublinBikesStationAverage.objects.bulk_create(bulk_objs)
    print(all_objects)

    end = time.time()
    print("Time took: ", (end - start))

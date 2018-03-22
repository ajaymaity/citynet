"""Forecast module."""
from .data_for_forecast import getDataforTheLastNdays
import itertools
import time


def date_hour_min(timestamp):
    """Convert to hour min format."""
    return timestamp.strftime("%H:%M:00")


def averageModel():
    """TODO."""
    all_stations = getDataforTheLastNdays(ndays=7)
    distinct_stations = all_stations.\
        order_by("parent_station__station_number").\
        distinct("parent_station__station_number")
    start = time.time()
    for station in distinct_stations:
        print("***** ", station.parent_station_id,
              " *****")
        stations = all_stations.filter(
            parent_station__station_number__exact=station.parent_station_id)

        objs = stations.order_by("station_last_update")
        groups = itertools.groupby(objs,
                                   lambda x: date_hour_min(
                                       x.station_last_update))

        total_times = 0
        for group, matches in groups:
            total_times += 1
            sum_available_bikes = 0
            len_available_bikes = 0
            for match in matches:
                len_available_bikes += 1
                sum_available_bikes += match.available_bikes
            avg_available_bikes = sum_available_bikes / len_available_bikes
            print(group, avg_available_bikes)
        print("Distinct times: ", total_times)

    end = time.time()
    print("Time took: ", (end - start))

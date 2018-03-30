"""Forecast module."""
import datetime
import itertools
import time

from cityback.storage.apps import getBikesTimeRange
from cityback.storage.models import DublinBikesStationRealTimeUpdate
from .models import DublinBikesStationAverage


def create_stations_average_occupancy():
    """Compute the average occupancy of each station."""
    all_stations = DublinBikesStationRealTimeUpdate.objects.all()
    stopwatch_start = time.time()
    distinct_stations_ids = all_stations.distinct(
        "parent_station__station_number").order_by(
        "parent_station__station_number").values_list(
        'parent_station__station_number', flat=True)

    print("Computing distinct stations took: {}s".format(
        time.time() - stopwatch_start))
    stopwatch_start = time.time()
    avg_stations = []
    for station_id in distinct_stations_ids:

        stopwatch2_start = time.time()
        objs = list(all_stations.filter(
            parent_station_id=station_id).only(
            'timestamp', 'available_bikes', 'bike_stands'))
        print("query took: {}s".format(
            time.time() - stopwatch2_start))
        ordered_times = sorted([(x.timestamp.time(), x) for x in objs],
                               key=lambda x: x[0])
        groups_by_minute = itertools.groupby(
            ordered_times, lambda x: x[0])

        total_times = 0
        for group, matches in groups_by_minute:

            total_times += 1
            sum_occupancy = 0.
            count_entry = 0
            for match in matches:
                count_entry += 1
                bikes, stands = (match[1].available_bikes,
                                 match[1].bike_stands)
                if stands != 0:
                    sum_occupancy += bikes / stands

            if count_entry == 0:
                avg_occupancy = 0
            else:
                avg_occupancy = 100. * sum_occupancy / count_entry

            avg_stations.append(DublinBikesStationAverage(
                parent_station_id=station_id, time=group,
                avg_occupancy=avg_occupancy))

            print(group, avg_occupancy)
        print("Distinct times: ", total_times)

    DublinBikesStationAverage.objects.all().delete()
    DublinBikesStationAverage.objects.bulk_create(avg_stations, 1000)

    print("Computing average for all stations took: {}s".format(
        time.time() - stopwatch_start))


def forecast_occupancy(forecast_minutes, station_list, start_datetime=None):
    """Forecast bikes for the stations in station_list for the time range provided.

    * get the last occupancy for each station
    * compute the delta between each avg occupancy
    * create a new list of station values as the previous value + the delta.
    """
    if start_datetime is None:
        _, end = getBikesTimeRange()
        start_datetime = end
    start_time = start_datetime.time()
    end_time = start_datetime + datetime.timedelta(minutes=forecast_minutes)

    # Too long forecast requested, not supported yet.
    if forecast_minutes > 24 * 60 or start_datetime.day != end_time.day:
        return None
    end_time = end_time.time()

    avg_stations = DublinBikesStationAverage.objects.filter(
        time__gte=start_time, time__lte=end_time).filter(
        parent_station__in=station_list).order_by(
        "parent_station__station_number", "time")

    stations_at_start = (
        DublinBikesStationRealTimeUpdate.objects.filter(
            timestamp=start_datetime, parent_station__in=station_list)
    ).order_by("parent_station__station_number")

    predictions = []
    stopwatch_start = time.time()

    for station in stations_at_start:
        bikes, b_stands = (station.available_bikes,
                           station.bike_stands)
        if b_stands == 0:
            last_occup = 0
        else:
            last_occup = 100. * float(bikes) / b_stands

        avg_occups = avg_stations.filter(parent_station=station.parent_station)
        print("at start", last_occup)

        station_predictions = []
        previous_avg = 0.
        for idx, station_avg in enumerate(avg_occups):
            if idx == 0:
                previous_avg = station_avg.avg_occupancy
            else:
                delta_avg = station_avg.avg_occupancy - previous_avg
                prediction = last_occup + delta_avg
                if prediction > 100.:
                    prediction = 100.
                elif prediction < 0.:
                    prediction = 0.
                last_occup = prediction
                station_predictions.append(prediction)

        predictions.append((station.parent_station.station_number,
                            station_predictions))

    print("forecast time: {}s".format(time.time() - stopwatch_start))
    return predictions

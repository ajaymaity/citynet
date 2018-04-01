"""Create a dev admin account."""
import datetime
import numpy as np
from django.core.management.base import BaseCommand
import time
from cityback.data_storage.apps import HistoricAnalysis
from cityback.data_storage.models import DublinBikesStationRealTimeUpdate
# import ipdb


class Command(BaseCommand):
    """Custom command."""

    def handle(self, *args, **options):
        """Actual code."""
        time_delta = 60

        start, end = HistoricAnalysis.getBikesTimeRange()
        start, end = HistoricAnalysis.floorTime(start, time_delta), \
                     HistoricAnalysis.floorTime(end, time_delta)

        num_dates = (end - start) // datetime.timedelta(seconds=time_delta) + 1
        date_list = [start + datetime.timedelta(seconds=(time_delta * x))
                     for x in range(num_dates)]

        assert(date_list[-1] == end)
        print("number of times", num_dates)

        stopwatch_start = time.time()
        list_stations = DublinBikesStationRealTimeUpdate.objects.all(
        ).values_list('parent_station__station_number', flat=True).distinct()
        list_stations = list(list_stations)
        num_stations = len(list_stations)

        all = DublinBikesStationRealTimeUpdate.objects.all()

        print("number of update records", all.count())

        vlqs = all.values_list('last_update', 'available_bikes', 'bike_stands',
                               'parent_station__station_number')
        r = np.core.records.fromrecords(vlqs, names=[
            'last_update', 'available_bikes', 'bike_stands',
            'parent_station__station_number'])

        print("all data dumped in r")
        occupancy = np.zeros((num_dates, num_stations), dtype=np.float64)
        counts = np.zeros((num_dates, num_stations), dtype=np.int64)

        print("filling numpy array")
        for i, data in enumerate(r):
            if i % 10000 == 0:
                print(i)

            rounded_time = HistoricAnalysis.floorTime(data[0], time_delta)
            try:
                idx = date_list.index(rounded_time)
                station_idx = list_stations.index(data[3])
            except ValueError:
                continue
            stands = data[2]
            if stands != 0:
                occupancy[idx, station_idx] += (float(data[1])
                                                * 100 / stands)
                counts[idx, station_idx] += 1

        total = counts.sum()
        empty = counts == 0
        counts[empty] = 1
        occupancy /= counts
        # interpolate
        if len(occupancy) == 0:
            return date_list, occupancy
        print("filling holes")
        # find first data
        for sidx in range(num_stations):
            idx = 0
            while empty[idx, sidx]:
                idx += 1
            # fill the begining
            print("idx=", idx)
            occupancy[0:idx, sidx] = occupancy[idx, sidx]

        for sidx in range(num_stations):
            fill = occupancy[0, sidx]

            for i in range(occupancy.shape[0]):
                if empty[i, sidx]:
                    occupancy[i, sidx] = fill
                else:
                    fill = occupancy[i, sidx]
        end = time.time()
        print("computed {} values in {}s".format(
            total,
            end - stopwatch_start
        ))
        np.save("times", date_list)
        np.save("occupancy", occupancy)
        print("Saved times and occupancy matrix")

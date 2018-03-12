"""Hello World file testing data retrieval for the Dublin bikes."""

import csv
from cityback.storage.models import (DublinBikesStationRealTimeUpdate,
                                     DublinBikesStation)
from datetime import timedelta, datetime
from django.contrib.gis.geos import Point
from django.utils import timezone

# Settings:
SAMPLE_TIME = 0  # number of minutes between samples
CSV_FILE = "output.csv"  # CSV file to save data in
FORMAT = "%Y%m%d%H%M%S"


def getDataForTheLastWeek():
    """Get data for the last week."""
    some_day_last_week = timezone.now().date() - timedelta(days=7)
    monday_of_last_week = some_day_last_week - timedelta(days=(
            some_day_last_week.isocalendar()[2] - 1))
    monday_of_this_week = monday_of_last_week + timedelta(days=7)
    DublinBikesStationRealTimeUpdate.objects.filter(
        created_at__gte=monday_of_last_week,
        created_at__lt=monday_of_this_week)


def getDataforTheLastNdays(ndays=30):
    """Get data from the db that are between ndays ago and now."""
    last_month = datetime.today() - timedelta(days=ndays)
    items = DublinBikesStationRealTimeUpdate.objects.filter(
        last_update__gte=last_month)
    return items


def getLatLongCordinates(station_name):
    """Retrieve Dublin bikes key."""
    station = DublinBikesStation.objects.get(name=station_name)
    return station.station_number, station.latitude, station.longitude


def distance(station1, station2):
    """Retrieve Dublin bikes key."""
    pnt1 = Point(station1.latitude, station2.longitude, srid=4326)
    pnt2 = Point(station1.latitude, station2.longitude, srid=4326)
    pnt1.distance(pnt2) * 100


def writeToCsv(data, filename="output.csv"):
    """Take the list of results and write as csv to filename."""
    with open(filename, 'w') as fcsv:
        csvf = csv.writer(fcsv, delimiter=",")
        csvf.writerow(["timestamp", "Bikes Free"])
        for d in data:
            csvf.writerow([d.last_update.strftime(FORMAT),
                           d.available_bike_stands -
                           d.available_bikes])

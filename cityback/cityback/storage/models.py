"""Bike storage models definition."""
from django.contrib.gis.db import models


# Create your models here.
class DublinBikesStation(models.Model):
    """A Dublin bikes station."""

    station_number = models.IntegerField(primary_key=True)
    position = models.PointField()
    name = models.CharField(max_length=80)
    address = models.CharField(max_length=120)
    bonus = models.BooleanField(default=False)
    contract_name = models.CharField(max_length=30)
    banking = models.BooleanField(default=False)

    def __str__(self):
        """For returning number and name of station with object."""
        return "station no. %s named '%s'" % (self.station_number, self.name)


class DublinBikesStationRealTimeUpdate(models.Model):
    """A Dublin bikes station real time data."""

    parent_station = models.ForeignKey(DublinBikesStation,
                                       on_delete=models.CASCADE)
    status = models.CharField(max_length=30)
    last_update = models.DateTimeField(null=True)
    available_bikes = models.IntegerField()
    available_bike_stands = models.IntegerField()
    bike_stands = models.IntegerField()

"""Bike storage models definition."""
from django.db import models
from django.contrib import admin


# Create your models here.
class DublinBikesStation(models.Model):
    """A Dublin bikes station."""

    station_number = models.IntegerField(primary_key=True)
    latitude = models.FloatField()
    longitude = models.FloatField()
    name = models.CharField(max_length=80)
    address = models.CharField(max_length=120)
    bonus = models.BooleanField(default=False)


class StationAdmin(admin.ModelAdmin):
    """Create the admin view of the stations."""

    list_display = [field.name for field in
                    DublinBikesStation._meta.get_fields()]


admin.site.register(DublinBikesStation, StationAdmin)


# class DublinBikesStationUpdate(models.Model):
#    parent_station = models.ForeignKey(DublinBikesStation,
#                                       on_delete=models.CASCADE)
#    status = models.CharField(max_length=30)

"""TODO."""

from django.db import models  # NOQA

from cityback.storage.models import DublinBikesStation


# Create your models here.
class DublinBikesStationAverage(models.Model):
    """A Dublin bikes station average value per minute."""

    parent_station = models.ForeignKey(DublinBikesStation,
                                       on_delete=models.CASCADE)
    time = models.TimeField(db_index=True, null=True)
    avg_occupancy = models.FloatField(null=True)

    def __str__(self):
        """For returning number, name and available bikes of station."""
        return "station no. %s named '%s' at %s with available bikes %d" % \
               (self.parent_station.station_number, self.parent_station.name,
                self.time, self.avg_occupancy)

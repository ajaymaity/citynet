# noqa
from django.db import models


# Create your models here.
class DublinBikesStorage(models.Model):
    """Wrapper for Dublin Bikes data storage."""

    def static_storage(self):
        """Store static data."""
        self.number = models.IntegerField(primary_key=True)
        self.latitude = models.FloatField()
        self.longitude = models.FloatField()
        self.name = models.CharField(max_length=30)
        self.address = models.CharField(max_length=120)

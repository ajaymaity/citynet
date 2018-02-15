from django.db import models

# Create your models here.
class DublinBikesStorage(models.Model):
    """Wrapper for Dublin Bikes data storage."""

    def static_storage(self):
        """Store static data."""
        number = models.IntegerField(primary_key=True)
        latitude = models.FloatField()
        longitude = models.FloatField()
        name = models.CharField(max_length=30)
        address = models.CharField(max_length=120)
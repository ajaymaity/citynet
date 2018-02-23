"""TODO."""
from django.db import models


class SocketClient(models.Model):
    """Define all the clients waiting for data update."""

    channel_name = models.CharField(max_length=200)

"""TODO."""
from django.db import models


class SocketClient(models.Model):
    channel_name = models.CharField(max_length=200)


"""Rendering of views done in this module."""

from django.shortcuts import render
from cityback.storage.apps import getLattestStationsFromDB
import json


def rtStations(request):
    """Create your views here."""
    # print(getLattestStationsFromDB())
    return render(
        request, "rtStations.html", {
            "stations":
                json.dumps(getLattestStationsFromDB())})

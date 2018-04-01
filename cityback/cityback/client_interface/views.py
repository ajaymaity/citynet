"""Rendering of views done in this module."""

from django.shortcuts import render
from cityback.data_storage.apps import getLatestStationsFromDB
from cityback.visualisation.apps import convertToGeoJson
import json


def rtStations(request):
    """Render Dublin bikes station average value per minute."""
    latestStations = getLatestStationsFromDB()
    # latestStations = []
    return render(
        request, "rtStations.html", {
            "stations":
                json.dumps(convertToGeoJson(latestStations))})

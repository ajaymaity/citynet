"""Rendering of views done in this module."""

from django.shortcuts import render
from cityback.storage.apps import RealTimeProcessing
from cityback.client_interface.conversion import convertToGeoJson
import json


def rtStations(request):
    """Render Dublin bikes station average value per minute."""
    latestStations = RealTimeProcessing.getLatestStationsFromDB()
    # latestStations = []
    return render(
        request, "rtStations.html", {
            "stations":
                json.dumps(convertToGeoJson(latestStations))})

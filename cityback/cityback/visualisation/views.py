"""Rendering of views done in this module."""

from django.shortcuts import render
from cityback.storage.apps import getLatestStationsFromDB
from cityback.visualisation.apps import convertToGeoJson
import json


def rtStations(request):
    """Create your views here
    Refactor to class based view
    ."""
    latestStations = getLatestStationsFromDB()
    # latestStations = []
    return render(
        request, "rtStations.html", {
            "stations":
                json.dumps(convertToGeoJson(latestStations))})

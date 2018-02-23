"""Rendering of views done in this module."""

from django.shortcuts import render
from cityback.storage.apps import get_stations
import json


def indexView(request):
    """Create your views here."""
    print(get_stations())
    return render(
        request, "index.html", {"stations": json.dumps(get_stations())})

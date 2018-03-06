"""All the celery tasks are defined here."""
from __future__ import absolute_import, unicode_literals

from channels.layers import get_channel_layer

from cityback.retrieval.data_retrieval import BikesRetrieval
from cityback.storage.apps import update_stations
from celery import shared_task
from cityback.storage.apps import getLattestStationsFromDB
from asgiref.sync import async_to_sync
from cityback.visualisation.apps import convertToGeoJson
import json


@shared_task
def periodic_station_update():
    """Retreive station and update in db."""
    print("Updating stations...")
    bikes = BikesRetrieval()
    stations = bikes.get_dynamic_data()
    update_stations(stations)

    latestStations = getLattestStationsFromDB()
    data = json.dumps({"stations": convertToGeoJson(latestStations)})
    channel_layer = get_channel_layer()

    async_to_sync(channel_layer.group_send)(
            "stationUpdateGroup", {"type": "group.send",
                                   "text": data})

    print("done sending bike station update.")

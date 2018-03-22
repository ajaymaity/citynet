"""All the celery tasks are defined here."""
from __future__ import absolute_import, unicode_literals
# from channels.layers import get_channel_layer
from cityback.retrieval.data_retrieval import BikesRetrieval
from cityback.storage.apps import update_stations
from celery import shared_task
# from asgiref.sync import async_to_sync
# from cityback.visualisation.apps import getLatestStationJSON


@shared_task
def periodic_station_update():
    """Retreive station and update in db."""
    print("Updating stations...")
    bikes = BikesRetrieval()
    stations = bikes.get_dynamic_data()
    update_stations(stations)

    # latestStations = getLatestStationJSON()

    # channel_layer = get_channel_layer()
    #
    # async_to_sync(channel_layer.group_send)(
    #         "stationUpdateGroup", {"type": "group.send",
    #                                "text": latestStations})

    # TODO re-enable real-time bikes
    print("done sending bike station update.")

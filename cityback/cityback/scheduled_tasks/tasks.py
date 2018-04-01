"""Tasks run by the scheduler."""
from asgiref.sync import async_to_sync
from celery import shared_task
from channels.layers import get_channel_layer

from cityback.data_retrieval.data_retrieval import BikesRetrieval
from cityback.client_interface.conversion import getLatestStationJSON
from cityback.storage.apps import RealTimeProcessing


@shared_task
def periodic_station_update():
    """Retreive station and update in db."""
    print("Updating stations...")
    bikes = BikesRetrieval()
    stations = bikes.get_dynamic_data()
    RealTimeProcessing.update_stations(stations)

    latestStations = getLatestStationJSON()

    channel_layer = get_channel_layer()

    async_to_sync(channel_layer.group_send)(
            "stationUpdateGroup", {"type": "group.send",
                                   "text": latestStations})

    # TODO re-enable real-time bikes
    print("done sending bike station update.")

"""All the celery tasks are defined here."""
from __future__ import absolute_import, unicode_literals
from cityback.retrieval.data_retrieval import BikesRetrieval
from cityback.storage.apps import update_stations
from celery import shared_task


@shared_task
def periodic_station_update():
    """Retreive station and update in db."""
    bikes = BikesRetrieval()
    stations = bikes.get_dynamic_data()
    update_stations(stations)



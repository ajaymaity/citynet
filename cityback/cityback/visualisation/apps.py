"""Forecast function and convertToGeoJson function."""
import json

from django.apps import AppConfig

from cityback.storage.apps import getLatestStationsFromDB


class VisualisationConfig(AppConfig):
    """Set up visualistion config."""

    name = 'visualisation'


def convertToGeoJson(data):
    """Convert data in GeoJSON format."""
    geojson = dict()
    geojson['type'] = 'FeatureCollection'
    geojson['features'] = list()

    for k in data:
        occupancy = (k['available_bikes'] * 100 / k['bike_stands']
                     if k['bike_stands'] != 0 else 100)
        vacancy = (k['available_bike_stands'] * 100 / k['bike_stands']
                   if k['bike_stands'] != 0 else 0)
        newFeature = {
            "type": "Feature",
            "geometry": {
                "type": "Point",
                "coordinates":
                    [k['longitude'], k['latitude']]
            },
            "properties": {
                "title": ("S" + str(k['station_number']) +
                          ",B:" + str(k['available_bikes']) + ", S:" +
                          str(k['available_bike_stands'])),
                "description": "",
                "occupancy": occupancy,
                "vacancy": vacancy,
                "status": k['status'],
                "station_number": str(k['station_number']),
                "station_name": k['name']
            }
        }
        geojson['features'].append(newFeature)
        # geojson['name'] =
    return geojson


def getLatestStationJSON():
    """
    Get the json formatted last station updates.

    @:return json of the stations updates
    """
    latestStations = getLatestStationsFromDB()
    data = json.dumps({"stations": convertToGeoJson(latestStations)})
    return data

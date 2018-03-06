"""TODO."""

from django.apps import AppConfig
import json

class VisualisationConfig(AppConfig):
    """Set up visualistion config."""

    name = 'visualisation'

# previousOccupancy = -1
def convertToGeoJson(data):
    geojson = dict()
    geojson['type'] = 'FeatureCollection';
    geojson['features'] = list()

    for k in data:

        occupancy = k['available_bikes'] * 100 / k['bike_stands']
        # occupancyChanged = 0
        # if previousOccupancy == -1:
        #     previousOccupancy = occupancy
        # else:
        #     if occupancy != previousOccupancy:
        #         occupancyChanged = 1

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
                "vacancy": k['available_bike_stands'] * 100 / k['bike_stands'],
                "status": k['status'],
                # "occupancyChanged": occupancyChanged,
            }
        }
        geojson['features'].append(newFeature)
    return geojson
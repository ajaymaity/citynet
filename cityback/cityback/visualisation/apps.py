"""TODO."""

from django.apps import AppConfig


class VisualisationConfig(AppConfig):
    """Set up visualistion config."""

    name = 'visualisation'


def convertToGeoJson(data):
    """Convert data in GeoJSON format."""
    geojson = dict()
    geojson['type'] = 'FeatureCollection'
    geojson['features'] = list()

    for k in data:
        occupancy = k['available_bikes'] * 100 / k['bike_stands']
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
            }
        }
        geojson['features'].append(newFeature)
        # geojson['name'] =
    return geojson
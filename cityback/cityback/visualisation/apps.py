"""Forecast function and convertToGeoJson function."""
import json
from django.apps import AppConfig
from cityback.storage.apps import getLatestStationsFromDB
from .models import DublinBikesStationAverage
from cityback.storage.models import DublinBikesStationRealTimeUpdate
import datetime
from django.db.models.query import QuerySet
import time


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


def getForecast(startTime, endTime, currentDate, station_list):
    """Perform forecast using Average Model."""
    startTime = datetime.datetime.strptime(startTime, "%H:%M:%S")
    endTime = datetime.datetime.strptime(endTime, "%H:%M:%S")
    currentDate = datetime.datetime.strptime(currentDate, "%Y-%m-%d")
    currentDateTime = currentDate.replace(hour=startTime.hour,
                                          minute=startTime.minute)
    currentDateTime_oneMinuteBefore = currentDateTime - \
        datetime.timedelta(minutes=1)

    items_from_model = DublinBikesStationAverage.objects.filter(
        time__gte=startTime - datetime.timedelta(minutes=1),
        time__lte=endTime)
    items_from_model = items_from_model.order_by("time")

    item_at_currentDateTime_beforeOneMinute = \
        DublinBikesStationRealTimeUpdate.objects.filter(
            timestamp__exact=currentDateTime_oneMinuteBefore
        )

    predictions = []
    start = time.time()
    for station in station_list:

        item_at_currentDateTime_bfmn_for_a_station = \
            item_at_currentDateTime_beforeOneMinute.filter(
                parent_station__station_number__exact=station
            )

        if len(
                item_at_currentDateTime_bfmn_for_a_station) \
                == 0:\

                    continue

        assert len(
                    item_at_currentDateTime_bfmn_for_a_station) == 1

        items_from_model_for_a_station = \
            items_from_model.filter(
                parent_station__station_number__exact=station
            )

        query = items_from_model_for_a_station.all().query
        query.group_by = ['time']
        items_from_model_for_a_station = \
            QuerySet(query=query, model=items_from_model_for_a_station)

        for idx, item_from_model in enumerate(items_from_model_for_a_station):
            prediction_for_a_station = {}
            if (idx == 0):
                continue
            else:
                current_time_bikes_from_model = \
                    item_from_model.avg_available_bikes
                diff =\
                    current_time_bikes_from_model\
                    - item_at_currentDateTime_bfmn_for_a_station[0].\
                    available_bikes

                prediction = \
                    item_at_currentDateTime_bfmn_for_a_station[0] \
                    .available_bikes + diff
                prediction_time = \
                    currentDateTime_oneMinuteBefore \
                    + datetime.timedelta(minutes=idx)

                prediction_for_a_station["station_number"] = \
                    item_from_model.parent_station.station_number
                prediction_for_a_station["time"] = prediction_time
                prediction_for_a_station["predicted_available_bikes"] = \
                    prediction
                predictions.append(prediction_for_a_station)

    end = time.time()
    print(end - start)

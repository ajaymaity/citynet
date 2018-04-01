#!/usr/bin/python
# coding=utf-8
"""An example script that is install in the bin PATH of the target.

This script downloads the lattest station update to a json file.
"""
import datetime
import time
from cityback.data_retrieval.data_retrieval import BikesRetrieval
import json


st = datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d_%H:%M:%S')
out_path = st + "_stations_updates.json"
bikes = BikesRetrieval()
stations = bikes.get_dynamic_data()
with open(out_path, "w") as outfile:
    json.dump(stations, outfile)

print("Successfully downloaded {} Dublin Bike stations in {}".format(
    len(stations), out_path))

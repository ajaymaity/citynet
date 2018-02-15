#!/usr/bin/python
# coding=utf-8
"""Load the configuration dict from the json config."""

import os
import json


def get_private_config():
    """Return the project private config as a json dict."""
    config_file = os.path.join(os.path.dirname(os.path.realpath(__file__)),
                               "..", "..", "..",
                               "config_private", "config.json")
    with open(config_file, "r") as cfile:
        data = json.load(cfile)
    return data

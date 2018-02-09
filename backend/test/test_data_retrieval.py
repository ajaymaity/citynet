#!/usr/bin/python
# coding=utf-8

# Base Python File (self.py)
# Created: Tue 23 Jan 2018 16:01:45 GMT
# Version: 1.0
#
# This Python script was developped by Cory.
#
# (c) Cory <sgryco@gmail.com>

import unittest
from cityback import data_retrieval


class TestKey(unittest.TestCase):

    def test_key(self):
        self.assertTrue(data_retrieval.get_apikey().endswith("47b20"))


if __name__ == '__main__':
    unittest.main()

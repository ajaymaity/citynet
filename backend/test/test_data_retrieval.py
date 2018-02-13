#!/usr/bin/python
# coding=utf-8
"""Test cases for the data retrieval part."""

import unittest
from cityback import data_retrieval


class TestAPI(unittest.TestCase):
    """Test the access key."""

    def test_key(self):
        """Check the connectivity using the Dublin bikes key."""
        self.assertTrue(data_retrieval.get_apikey().endswith("47b20"))
        self.assertTrue(data_retrieval.check_connectivity())


if __name__ == '__main__':
    unittest.main()

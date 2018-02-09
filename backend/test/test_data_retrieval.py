#!/usr/bin/python
# coding=utf-8
"""Test cases for the data retrieval part."""

import unittest
from cityback import data_retrieval


class TestKey(unittest.TestCase):
    """Test the access key."""

    def test_key(self):
        """Chek the last key digits."""
        self.assertTrue(data_retrieval.get_apikey().endswith("47b20"))


if __name__ == '__main__':
    unittest.main()

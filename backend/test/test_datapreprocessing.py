#!/usr/bin/python
# coding=utf-8
"""Test cases for the data preprocessing part."""

import unittest
from cityback.data_preprocessing import add

class TestCelery(unittest.TestCase):
    """Test the access key."""

    def test_task(self):
        result = add.apply(args=(4, 4)).get()
        self.assertEqual(result, 8)

if __name__ == '__main__':
    unittest.main()

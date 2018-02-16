#!/usr/bin/python
# coding=utf-8
"""Test cases for the data preprocessing part."""

import unittest
from cityback import data_processing


class TestCelery(unittest.TestCase):
    """Test base Celery tasks."""

    def test_task(self):
        """Test the add celery task with apply."""
        result = data_processing.add.apply(args=(4, 4)).get()
        self.assertEqual(result, 8)


if __name__ == '__main__':
    unittest.main()

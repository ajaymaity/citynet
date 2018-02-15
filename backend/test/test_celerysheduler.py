#!/usr/bin/python.
# coding=utf-8
"""Test cases for the celery scheduler class."""
import unittest

from cityback.data_scheduler import test


class TestMyCeleryWorker(unittest.TestCase):
    """Test the celery worker."""

    def setUp(self):
        """
        Test the celery workers,celery_task.

        eager makes tasks synchronous.
        """
        test.conf.update(CELERY_TASK_ALWAYS_EAGER=True)

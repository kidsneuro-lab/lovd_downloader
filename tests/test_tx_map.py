#!/usr/bin/env python

"""Tests for `lovd_downloader` package."""

import unittest

import requests

from lovd_downloader import tx_map
from lovd_downloader.common import InvalidLOVDSiteException

class TestTxMap(unittest.TestCase):
    """Tests for `lovd_downloader` package."""

    def setUp(self):
        """Set up test fixtures, if any."""

    def tearDown(self):
        """Tear down test fixtures, if any."""

    def test_000_invalid_url(self):
        """Test something."""
        with self.assertRaises(requests.exceptions.ConnectionError):
            tx_map.get_gene_map('http://nonexistanturl', 'transcripts.tsv', 1, 10)

    def test_001_non_lovd_installation(self):
        """Test something."""
        with self.assertRaises(InvalidLOVDSiteException):
            tx_map.get_gene_map('https://www.google.com', 'transcripts.tsv', 1, 10)

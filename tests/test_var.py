#!/usr/bin/env python

"""Tests for `lovd_downloader` package."""

import unittest
from pathlib import Path
import shutil

import requests

from lovd_downloader import var
from lovd_downloader.common import InvalidLOVDSiteException, GeneNotInTxMapException

class TestTxMap(unittest.TestCase):
    """Tests for `lovd_downloader` package."""
    tx_map_tmp = Path("tests").joinpath("transcripts.tsv.test")
    tx_map =  Path("tests").joinpath("transcripts.tsv")

    def setUp(self):
        """Set up test fixtures, if any."""   
        if TestTxMap.tx_map_tmp.exists():
            shutil.copy(TestTxMap.tx_map_tmp.as_posix(), TestTxMap.tx_map.as_posix())

    def tearDown(self):
        """Tear down test fixtures, if any."""
        if TestTxMap.tx_map.exists():
            TestTxMap.tx_map.unlink()

    def test_000_invalid_url(self):
        """Test something."""
        with self.assertRaises(requests.exceptions.ConnectionError):
            var.get_variants(lovd_url='http://nonexistanturl', output='variants.tsv', tx_map=TestTxMap.tx_map.as_posix(), genes=['AGA'])

    def test_001_non_lovd_installation(self):
        """Test something."""
        with self.assertRaises(InvalidLOVDSiteException):
            var.get_variants(lovd_url='https://www.google.com', output='variants.tsv', tx_map=TestTxMap.tx_map.as_posix(), genes=['AGA'])

    def test_001_gene_not_in_transcript_map(self):
        """Test something."""
        with self.assertRaises(GeneNotInTxMapException):
            var.get_variants(lovd_url='https://www.google.com', output='variants.tsv', tx_map=TestTxMap.tx_map.as_posix(), genes=['ABCD'])

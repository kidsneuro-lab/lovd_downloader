#!/bin/sh
sudo make install
sudo make dist
pip install dist/lovd_downloader-0.2.0.tar.gz
lovd_tx_map -u "https://databases.lovd.nl" -o transcripts.tsv
lovd_variants -u "https://databases.lovd.nl" -o variants.tsv -t transcripts.tsv -g "CAPN3,DYSF"
lovd_variants -u "https://databases.lovd.nl" -o variants.tsv -t transcripts.tsv

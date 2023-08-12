#!/bin/sh

awk 'NR > 1' transcripts.tsv > tmp_transcripts.tsv

split -dl 5000 tmp_transcripts.tsv tmp_transcripts_subset

for TMP_FILE in `ls -1 tmp_transcripts_subset*`; do
    FILE=$(echo "$TMP_FILE" | sed 's/tmp_//')

    head -n 1 transcripts.tsv > "${FILE}.tsv"
    cat $TMP_FILE >> "${FILE}.tsv"
done

rm tmp_transcripts.tsv
rm tmp_transcripts_subset*

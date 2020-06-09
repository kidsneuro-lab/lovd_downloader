"""Console script for lovd_downloader."""
import argparse
import sys
import logging

from . import tx_map

def main():
    """Console script for lovd_downloader."""
    parser = argparse.ArgumentParser()
    parser.add_argument('-u', '--url', action='store', type=str, help="LOVD URL", required=True)
    parser.add_argument('-o', '--output', action='store', type=str, help='Path of output TSV (tab delimited) file', required=True)
    parser.add_argument('-p', '--pages', action='store', type=int, default=None, help="Limit no. of pages (handy for testing)", required=False)
    parser.add_argument('-e', '--entries', action='store', type=int, default=1000, help="No. of entries per page)", required=False, choices=[10,25,50,100,250,500,1000])
    parser.add_argument('-v', '--verbose', action='store_true', help="Display verbose messages", required=False)

    args = parser.parse_args()

    if args.verbose:
        logging.basicConfig(level=logging.DEBUG, format='%(levelname)s %(message)s')
    else:
        logging.basicConfig(level=logging.INFO, format='%(levelname)s %(message)s')

    tx_map.get_gene_map(lovd_url=args.url, output=args.output, page_count_limit=args.pages, entries_limit=args.entries) #"https://databases.lovd.nl/shared/transcripts")
    
    return 0

if __name__ == "__main__":
    sys.exit(main())  # pragma: no cover

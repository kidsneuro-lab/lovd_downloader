"""Console script for lovd_downloader."""
import argparse
import sys
import logging

from . import var

def main():
    """Console script for lovd_downloader."""
    parser = argparse.ArgumentParser()
    parser.add_argument('-u', '--url', action='store', type=str, help="LOVD URL", required=True)
    parser.add_argument('-o', '--output', action='store', type=str, help='Path of output TSV (tab delimited) file', required=True)
    parser.add_argument('-t', '--tx', action='store', type=str, help="LOVD transcripts map", required=True)
    parser.add_argument('-g', '--genes', action='store', type=str, help="Comma separated list of genes (Not specifying this will select all genes", default=None, required=False)
    parser.add_argument('-p', '--pages', action='store', type=int, default=None, help="Limit no. of pages (handy for testing)", required=False)
    parser.add_argument('-e', '--entries', action='store', type=int, default=1000, help="No. of entries per page)", required=False, choices=[10,25,50,100,250,500,1000])
    parser.add_argument('-v', '--verbose', action='store_true', help="Display verbose messages", required=False)

    args = parser.parse_args()

    if args.verbose:
        logging.basicConfig(level=logging.DEBUG, format='%(levelname)s %(message)s')
    else:
        logging.basicConfig(level=logging.INFO, format='%(levelname)s %(message)s')

    if args.genes is not None:
        genes_list = args.genes.split(',')
    else:
        genes_list = None

    var.get_variants(lovd_url=args.url, output=args.output, tx_map=args.tx, genes=genes_list, page_count_limit=args.pages, entries_limit=args.entries)
    
    return 0

if __name__ == "__main__":
    sys.exit(main())  # pragma: no cover

import math
import logging
import traceback
import random
import time

import requests
import pandas as pd
from bs4 import BeautifulSoup
import lxml

from . import common

logger = logging.getLogger('tx_map')

def get_gene_map(lovd_url: str, output:str, page_count_limit: int = None, entries_limit:int = 1000):
    lovd_url = "{}{}".format(lovd_url, common.lovd_tx_url_suffix)
    
    lovd_params = {'order':'id_,ASC',
                   'page_size':entries_limit,
                   'page':1}

    tx_list = []

    try:
        logger.info("Obtaining list of transcripts on page: {}".format(1))
        r = requests.get(lovd_url, headers=common.lovd_headers, params=lovd_params)
        soup = BeautifulSoup(r.content, features="lxml")

        total_entries = int(soup.find("input", {'name':'total'})['value'])
        logger.info("Total no. of transcripts in LOVD: {}".format(total_entries))        
        
        page_count = math.ceil(total_entries / entries_limit)
        logger.info("No. of pages: {} ({} entries per page)".format(page_count, entries_limit))        

        logger.debug("Searching for <table id='viewlistTable_Transcripts'>")
        viewlistTable_Transcripts = soup.find(id='viewlistTable_Transcripts')

        tx_df = pd.read_html(viewlistTable_Transcripts.prettify(), converters={'ID': str})[0]
        tx_df['Download_Date'] = time.strftime('%Y-%m-%d')
        tx_list.append(tx_df)

        if page_count > 1:
            # Set a limit on the page count if user has restricted
            if page_count_limit is not None:
                logger.debug("Limiting no. of pages extracted to: {}".format(page_count_limit))
                if page_count > page_count_limit:
                    page_count = page_count_limit

            for page in range(2, page_count + 1):
                logger.info("Obtaining list of transcripts on page: {}".format(page))
                lovd_params = {'order':'id_,ASC',
                               'page_size':entries_limit,
                               'page':page}

                logger.debug('Sleep for random no. of seconds') # That may reduce the chances of being blocked
                time.sleep(random.choice([3,5,7,9]))

                r = requests.get(lovd_url, headers=common.lovd_headers, params=lovd_params)
                soup = BeautifulSoup(r.content, features="lxml")

                logger.debug("Searching for <table id='viewlistTable_Transcripts'>")
                viewlistTable_Transcripts = soup.find(id='viewlistTable_Transcripts')

                tx_df = pd.read_html(viewlistTable_Transcripts.prettify(), converters={'ID': str})[0]
                tx_df['Download_Date'] = time.strftime('%Y-%m-%d')
                tx_list.append(tx_df)

    except requests.exceptions.RequestException:
        logger.error("Encountered error while accessing URL [{}]: {}".format(lovd_url, traceback.format_exc()))
        exit(2)

    except Exception:
        logger.error("Encountered error: {}".format(traceback.format_exc()))
        exit(2)

    else:
        genes_map = pd.concat(tx_list)
        logger.info("Total no. of transcripts retrieved: {}".format(genes_map.shape[0]))

        # Replace all non alpha-numeric characters with an underscore
        genes_map.columns = genes_map.columns.str.replace("[^0-9a-zA-Z]+","_")
        genes_map.to_csv(output, sep="\t", index=False)

import math
import logging
import traceback
import re
import random
import time

import requests
import pandas as pd
from bs4 import BeautifulSoup
import lxml

from lovd_downloader import common
from lovd_downloader.common import InvalidLOVDSiteException, GeneNotInTxMapException

logger = logging.getLogger('variants')

def get_variants(lovd_url: str, output:str, tx_map:str, genes:list = None, page_count_limit: int = None, entries_limit: int = 1000):    
    try:
        tx_map = pd.read_csv(tx_map, sep="\t", dtype={'ID':str})
    except Exception:
        logger.error("Encountered error while loading transcripts: {}".format(traceback.format_exc()))
        raise

    if len(set(genes).difference(tx_map['Gene_ID'])) != 0:
        logger.error("Genes {} not in list of transcripts. Please check list of genes queries".format(', '.join(set(genes).difference(tx_map['Gene_ID']))))
        raise GeneNotInTxMapException

    vars_list = []

    if genes is None:
        logger.info("All genes variants to be extracted")
        genes = tx_map['Gene_ID'].tolist()
    else:
        logger.info("Extracting variants for {}".format(", ".join(genes)))

    for gene in genes:
        for tx in tx_map.loc[tx_map['Gene_ID'] == gene].apply(lambda x: {'id':x['ID'], 'name':x['NCBI_ID'], 'count':x['Variants']}, axis=1):
            if tx['count'] == 0:
                logger.info("Skipping {} ({}). No variants in LOVD".format(gene, tx['name']))
            else:
                try:
                    logger.info("Obtaining unique variants for {} ({})".format(gene, tx['name']))

                    url = "{}/shared/variants/{}/unique#object_id=VariantOnTranscriptUnique,VariantOnGenome".format(lovd_url, gene)
                    lovd_params = {'id':gene,
                                'order':'VariantOnGenome/DBID',
                                'page_size':entries_limit,
                                'search_transcriptid':tx['id'],
                                'page':1}

                    r = requests.get(url, headers=common.lovd_headers, params=lovd_params)
                    soup = BeautifulSoup(r.content, features="lxml")

                    total_entries = int(soup.find("input", {'name':'total'})['value'])
                    logger.info("Total no. of variants: {}".format(total_entries))

                    page_count = math.ceil(total_entries / entries_limit)
                    logger.debug("No. of pages: {} ({} entries per page)".format(page_count, entries_limit))   

                    logger.debug("Searching for <table id='viewlistTable_*'>")
                    viewlistTable = soup.find_all(id=re.compile('viewlistTable'))[0]

                    vars_df = pd.read_html(viewlistTable.prettify())[0]
                    vars_df['Transcript'] = tx['name']
                    vars_df['Gene'] = gene
                    vars_df['Download_Date'] = time.strftime('%Y-%m-%d')
                    vars_list.append(vars_df)

                    if page_count > 1:
                        # Set a limit on the page count if user has restricted
                        if page_count_limit is not None:
                            logger.debug("Limiting no. of pages extracted to: {}".format(page_count_limit))
                            if page_count > page_count_limit:
                                page_count = page_count_limit

                        for page in range(2, page_count + 1):
                            logger.debug("Obtaining variants on page: {}".format(page))
                            lovd_params = {'id':gene,
                                        'order':'VariantOnGenome/DBID',
                                        'page_size':entries_limit,
                                        'search_transcriptid':tx['id'],
                                        'page':page}

                            logger.debug('Sleep for random no. of seconds') # That may reduce the chances of being blocked
                            time.sleep(random.choice([3,5,7,9]))
                            
                            r = requests.get(url, headers=common.lovd_headers, params=lovd_params)
                            soup = BeautifulSoup(r.content, features="lxml")

                            logger.debug("Searching for <table id='viewlistTable_*'>")
                            viewlistTable = soup.find_all(id=re.compile('viewlistTable'))[0]

                            vars_df = pd.read_html(viewlistTable.prettify())[0]
                            vars_df['Transcript'] = tx['name']
                            vars_df['Gene'] = gene
                            vars_df['Download_Date'] = time.strftime('%Y-%m-%d')
                            vars_list.append(vars_df)
                
                except requests.exceptions.RequestException:
                    logger.error("Encountered error while accessing URL [{}]: {}".format(lovd_url, traceback.format_exc()))
                    raise

                except TypeError:
                    logger.error("Invalid format. The URL [{}] may not be a valid LOVD installation".format(lovd_url))
                    raise InvalidLOVDSiteException

                except Exception:
                    logger.error("Encountered error: {}".format(traceback.format_exc()))
                    raise

    if len(vars_list) > 0:
        variants = pd.concat(vars_list)
        logger.info("Total no. of variants retrieved: {}".format(variants.shape[0]))

        # Replace all non alpha-numeric characters with an underscore
        variants.columns = variants.columns.str.replace("[^0-9a-zA-Z]+","_").str.replace("^_|_$","")
        variants.to_csv(output, sep="\t", index=False)
    else:
        logger.info("No variants retrieved")
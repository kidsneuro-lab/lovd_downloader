lovd_tx_url_suffix = '/shared/transcripts'

lovd_headers = {'Connection':'keep-alive',
                'pragma':'no-cache',
                'cache-control':'no-cache',
                'Upgrade-Insecure-Requests':'1',
                'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36',
                'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9'}

class LOVDDownloaderException(Exception):
    pass

class InvalidLOVDSiteException(LOVDDownloaderException):
    pass

class GeneNotInTxMapException(LOVDDownloaderException):
    pass
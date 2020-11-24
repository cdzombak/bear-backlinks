import logging
import os
import sys


def get_bear_api_token() -> str:
    retv = os.getenv('CDZ_BEAR_API_TOKEN')
    if retv is not None:
        return retv
    try:
        with open('.bear-api-token', 'r') as f:
            retv = f.read().strip()
    except Exception as e:  #noqa
        logging.critical('could not get Bear API token from environment (CDZ_BEAR_API_TOKEN) or file (.bear_api_token)', exc_info=e)
        sys.exit(2)
    return retv

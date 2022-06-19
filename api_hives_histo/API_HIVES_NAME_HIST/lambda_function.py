import sys
import json
import logging
from collections import Counter
import requests
import pandas as pd

from lib import *

logger = logging.getLogger()
logger.setLevel(logging.INFO)


start_endpoint = "https://wnk07eo5oc.execute-api.eu-central-1.amazonaws.com/dev/v1/beekeepers"


def lambda_handler(event, context):
    logger.info(f"Request: {event}")
    response_code = 200
    try:
        logger.info(f"asking {start_endpoint}")
        all_beekepers = requests.get(start_endpoint)
        logger.info("asked")
        # TODO: check if ok
        beekepers_dict = all_beekepers.json()
        logger.info(f"got all beekeepers! they are {len(beekepers_dict)}")
        logger.info(beekepers_dict[0].keys())
        logger.info(beekepers_dict[0]['hives'][0].keys())
        # START HIVES/NAME_HIST queens names hist
        all_queens_names = get_queens(beekepers_dict)
        queen_names_counts_data = make_histogram_from_list(all_queens_names)
        logger.info(queen_names_counts_data)
        # END HIVES/NAME_HIST queens names hist


    except Exception as e: # TODO: check specific exceptions
        logger.error("ERROR: Unexpected error")
        logger.error(e)
        sys.exit()
    response = {
        'statusCode': response_code,
        'body': json.dumps(queen_names_counts_data)
    }

    logger.info(f"Response: {queen_names_counts_data}")

    return response

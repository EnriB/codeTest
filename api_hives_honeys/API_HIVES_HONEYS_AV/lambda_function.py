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
        # START API HONEYS_AV
        honeys_list = get_all_honeys(beekepers_dict)
        total_honey_by_category = asked_query(honeys_list)
        logger.info(total_honey_by_category)
        # END API HONEYS_AV

    except Exception as e: # TODO: check specific exceptions
        logger.error("ERROR: Unexpected error")
        logger.error(e)
        sys.exit()
    response = {
        'statusCode': response_code,
        'body': json.dumps(total_honey_by_category)
    }

    logger.info(f"Response: {response}")

    return response

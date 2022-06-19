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
    """
    this lambda responds to a parameterless request with a sorteed list of all
    hives from the specified endpoint
    """
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
        # START GET SORTED HIVES LIST API FUNC API HIVES
        hives = get_hives(beekepers_dict)
        logger.info(f"hives keys: {hives[0].keys()}, n hives {len(hives)}")
        logger.info(f"first hive: {hives[0]}")
        # END GET SORTED HIVES LIST API FUNC API

    except Exception as e: # TODO: check specific exceptions
        logger.error("ERROR: Unexpected error")
        logger.error(e)
        sys.exit()
    response = {
        'statusCode': response_code,
        'body': json.dumps(hives)
    }

    logger.info(f"Response: {response}")

    return response

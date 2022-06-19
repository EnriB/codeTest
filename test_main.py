import sys
import json
import logging
import requests

logger = logging.getLogger()
logger.setLevel(logging.INFO)



start_endpoint = "https://wnk07eo5oc.execute-api.eu-central-1.amazonaws.com/dev/v1/beekeepers"


def get_hives(beekeepers_list):
    hives_list = []
    for beekeper in beekeepers_list:
        try:
            hives = beekeper['hives']
            for hive in hives:
                hive['beekeper_id'] = beekeper['id']
                hive['beekeper_ranking'] = beekeper['ranking']
                hives_list.append(hive)
        except KeyError:
            continue
    sorted_hives = sorted(hives_list, key= lambda x: x['beekeper_ranking'], reverse=True)
    return sorted_hives


try:
    print("asking {start_endpoint}")
    all_beekepers = requests.get(start_endpoint)
    print("asked")
    # TODO: check if ok
    beekepers_dict = all_beekepers.json()
    print(f"got all beekeepers! they are {len(beekepers_dict)}")
    print(beekepers_dict[0].keys())
    print(beekepers_dict[0]['hives'][0].keys())
    hives = get_hives(beekepers_dict)
    print(f"hives keys: {hives[0].keys()}, n hives {len(hives)}")
    print(f"first hive: {hives[0]}")
except Exception as e: # TODO: check specific exceptions
    logger.error("ERROR: Unexpected error")
    logger.error(e)
    sys.exit()
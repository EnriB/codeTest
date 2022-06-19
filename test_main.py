import sys
import json
import logging
from collections import Counter
import requests
import pandas as pd

logger = logging.getLogger()
logger.setLevel(logging.INFO)



start_endpoint = "https://wnk07eo5oc.execute-api.eu-central-1.amazonaws.com/dev/v1/beekeepers"


# TODO: refactor all gets, too much in common

def get_hives(beekeepers_list, sort_hives=True):
    hives_list = []
    for beekeper in beekeepers_list:
        try:
            hives = beekeper['hives']
            for hive in hives:
                hive['beekeper_id'] = beekeper['id']
                hive['beekeper_ranking'] = beekeper['ranking']
                hives_list.append(hive)
        except KeyError:  # beekeper has no hives
            continue
    if sort_hives:
        sorted_hives = sorted(hives_list,
                              key=lambda x: x['beekeper_ranking'], reverse=True)
        return sorted_hives
    else:
        return hives_list


def get_queens(beekeepers_list):
    queen_names = []
    for beekeper in beekeepers_list:
        try:
            hives = beekeper['hives']
            for hive in hives:
                queen_names.append(hive['queen_name'])
        except KeyError:  # beekeper has no hives, queen has no name?
            continue
    return queen_names


def make_histogram_from_list(list_of_strings):
    counter = Counter(list_of_strings)
    output = {}
    for name, count in sorted(counter.items()): # alphabetic order
        output[name] = count
    return output


def get_all_honeys(beekeepers_list):
    honeys_list = []
    for beekeper in beekeepers_list:
        try:
            honeys = beekeper['honeys']
            for honey in honeys:
                honeys_list.append(honey)
        except KeyError:  # beekeper has no honey
            continue
    return honeys_list


def asked_query(honeys_list):
    df = pd.DataFrame(honeys_list)
    print(df.columns)
    # assuming tipologia is the plant of the honey
    result = df.groupby(['plant'])['name'].count().to_json()
    return result


try:
    print("asking {start_endpoint}")
    all_beekepers = requests.get(start_endpoint)
    print("asked")
    # TODO: check if ok
    beekepers_dict = all_beekepers.json()
    print(f"got all beekeepers! they are {len(beekepers_dict)}")
    print(beekepers_dict[0].keys())
    print(beekepers_dict[0]['hives'][0].keys())
    # START GET SORTED HIVES LIST API FUNC API HIVES
    hives = get_hives(beekepers_dict)
    print(f"hives keys: {hives[0].keys()}, n hives {len(hives)}")
    print(f"first hive: {hives[0]}")
    # END GET SORTED HIVES LIST API FUNC API
    # START HIVES/NAME_HIST queens names hist
    all_queens_names = get_queens(beekepers_dict)
    queen_names_counts_data = make_histogram_from_list(all_queens_names)
    print(queen_names_counts_data)
    # END HIVES/NAME_HIST queens names hist
    # START API HONEYS_AV
    honeys_list = get_all_honeys(beekepers_dict)
    total_honey_by_category = asked_query(honeys_list)
    print(total_honey_by_category)
    # END API HONEYS_AV

except Exception as e: # TODO: check specific exceptions
    logger.error("ERROR: Unexpected error")
    logger.error(e)
    sys.exit()
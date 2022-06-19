import pandas as pd


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
    # assuming tipologia is the plant of the honey
    result = df.groupby(['plant'])['name'].count().to_json()
    return result
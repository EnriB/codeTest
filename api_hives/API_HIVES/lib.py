
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

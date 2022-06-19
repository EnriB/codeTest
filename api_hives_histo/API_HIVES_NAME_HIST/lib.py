from collections import Counter


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


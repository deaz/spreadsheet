from typing import Dict


def get_sorted_values(dictionary: Dict):
    return list(zip(*sorted(dictionary.items())))[1]

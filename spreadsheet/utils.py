from typing import Dict
import sys


def get_sorted_values(dictionary: Dict):
    return list(zip(*sorted(dictionary.items())))[1]


def exit_with_error(message):
    sys.stderr.write(message + '\n')
    sys.exit(1)

from typing import Dict, List
import sys


def get_sorted_values(dictionary: Dict) -> List:
    return list(zip(*sorted(dictionary.items())))[1]


def exit_with_error(message: str) -> None:
    sys.stderr.write(message + '\n')
    sys.exit(1)

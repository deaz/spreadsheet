import re
import sys
from typing import Dict, List, Tuple

from spreadsheet.cell import Cell


def get_sorted_values(dictionary: Dict) -> List:
    return list(zip(*sorted(dictionary.items())))[1]


def exit_with_error(message: str) -> None:
    sys.stderr.write(message + '\n')
    sys.exit(1)


def get_operations_and_operands(cell: Cell) -> Tuple[List[str], List[str]]:
    operation_re = re.compile(r'[-+/*]')
    operand_re = re.compile(r'[A-Za-z][1-9]|\d+')
    operations = operation_re.findall(cell.value)
    operands = operand_re.findall(cell.value)
    return operations, operands

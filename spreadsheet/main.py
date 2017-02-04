import re
from enum import Enum
import operator
from typing import Dict
import copy

from utils import get_sorted_values
import errors

CellType = Enum('CellType',
                ['NONE', 'NUMBER', 'EXPRESSION', 'STRING', 'ERROR'])


class Cell:
    def __init__(self, cell_type: CellType, cell_value):
        self.type = cell_type
        self.value = cell_value


Sheet = Dict[int, Dict[str, Cell]]


def read_input():
    try:
        row_count, column_count = map(int, input().strip().split(' '))
    except ValueError as e:
        raise Exception('Error during reading rows and columns count') from e

    sheet = dict()
    for row_index in range(1, 1 + row_count):
        try:
            row = dict()
            for index, cell in enumerate(input().split('\t')):
                column_letter = chr(ord('A') + index)
                row[column_letter] = cell
        except EOFError as e:
            raise Exception('Too few rows') from e
        if len(row) != column_count:
            raise Exception('Columns count in row {} is not equal to {}'
                            .format(row_index + 1, column_count))
        sheet[row_index] = row
    return sheet


def parse(sheet):
    new_sheet = dict()
    for row_index, row in sheet.items():
        new_row = dict()
        for column_letter, cell in row.items():
            new_row[column_letter] = syntax_check(cell)
        new_sheet[row_index] = new_row
    return new_sheet


# TODO: separate checking and converting
def syntax_check(cell):
    if not cell:
        return Cell(CellType.NONE, '')
    elif cell[0] == '\'':
        return Cell(CellType.STRING, cell[1:])
    elif cell[0] == '=':
        if not is_valid_expression(cell):
            return Cell(CellType.ERROR, errors.INVALID_SYNTAX)
        return Cell(CellType.EXPRESSION, cell[1:])
    elif cell.isdigit():
        return Cell(CellType.NUMBER, int(cell))
    else:
        return Cell(CellType.ERROR, errors.INVALID_SYNTAX)


def is_valid_expression(cell):
    reference_cell = re.compile(
        r'^=([A-Za-z]\d|\d+)([-+/*]([A-Za-z]\d|\d+))*$')
    return reference_cell.match(cell)


def compute_sheet(sheet: Sheet):
    computed_sheet = copy.deepcopy(sheet)
    for row_index, row in sheet.items():
        for column_letter, cell in row.items():
            if cell.type == CellType.EXPRESSION:
                visited = set()
                new_cell = compute_cell(
                    computed_sheet, row_index, column_letter, visited)
                cell.value = new_cell.value
                cell.type = new_cell.type


def compute_cell(sheet: Sheet, row: int, column: str, visited: set) -> Cell:
    cell_address = column + str(row)
    if cell_address in visited:
        return Cell(CellType.ERROR, errors.CIRCULAR_DEP)
    visited.add(cell_address)

    cell = sheet[row][column]

    if cell.type != CellType.EXPRESSION:
        return cell

    term_re = re.compile(r'[A-Za-z]\d|\d+')
    operation_re = re.compile(r'[-+/*]')
    operation_funcs = {'+': operator.add, '-': operator.sub,
                       '*': operator.mul, '/': operator.floordiv}
    operands = term_re.findall(cell.value)
    operations = operation_re.findall(cell.value)
    cell_value = 0
    # '+' is dummy operation for first operand
    for operation, operand in zip(['+'] + operations, operands):
        computed_cell = compute_term(operand, sheet, visited)
        value = computed_cell.value
        if computed_cell.type == CellType.ERROR:
            return computed_cell
        elif computed_cell.type == CellType.STRING:
            return Cell(CellType.ERROR, errors.WRONG_ARG)
        elif computed_cell.type == CellType.NONE:
            value = 0
        try:
            cell_value = operation_funcs[operation](cell_value, value)
        except ZeroDivisionError:
            return Cell(CellType.ERROR, errors.ZERO_DIV)
    return Cell(CellType.NUMBER, cell_value)


def compute_term(term: str, sheet: Sheet, visited: set) -> Cell:
    if term.isdigit():
        return Cell(CellType.NUMBER, int(term))
    else:
        return compute_cell(sheet, int(term[1]), term[0].upper(), visited)


def format_sheet(sheet: Sheet) -> str:
    result = ''
    sorted_rows = get_sorted_values(sheet)
    for row in sorted_rows:
        sorted_values = get_sorted_values(row)
        result += '\t'.join(map(lambda cell: str(cell.value), sorted_values))
        result += '\n'
    return result


def main():
    sheet = read_input()
    sheet = parse(sheet)
    compute_sheet(sheet)
    print(format_sheet(sheet))


if __name__ == '__main__':
    main()

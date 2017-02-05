import operator
import re
from typing import Dict, Tuple
import copy

import errors
from cell import Cell, CellType
from utils import get_sorted_values, exit_with_error

Sheet = Dict[int, Dict[str, Cell]]


def read_dimensions() -> Tuple[int, int]:
    try:
        row_count, column_count = map(int, input().strip().split(' '))
    except ValueError:
        exit_with_error('Error during reading rows and columns count')
    if row_count <= 0 or column_count <= 0:
        exit_with_error('Row and column counts must be positive integers')
    return row_count, row_count


def read_input(row_count, column_count) -> Sheet:
    sheet = dict()
    for row_index in range(1, 1 + row_count):
        row = dict()
        try:
            for index, cell in enumerate(input().split('\t')):
                column_letter = chr(ord('A') + index)
                row[column_letter] = parse_cell(cell)
        except EOFError:
            exit_with_error('Error: Too few rows')
        if len(row) != column_count:
            exit_with_error(f'Error: Columns count in row {row_index}'
                            f' is not equal to {column_count}')
        sheet[row_index] = row
    return sheet


def parse_cell(cell: str) -> Cell:
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


def is_valid_expression(cell: str) -> bool:
    reference_cell_re = re.compile(
        r'^=([A-Za-z]\d|\d+)([-+/*]([A-Za-z]\d|\d+))*$')
    return bool(reference_cell_re.match(cell))


def eval_sheet(sheet: Sheet) -> Sheet:
    evaluated = copy.deepcopy(sheet)
    for row_index, row in evaluated.items():
        for column_letter, cell in row.items():
            if cell.type == CellType.EXPRESSION:
                visited = set()
                row[column_letter] = eval_cell(
                    evaluated, row_index, column_letter, visited)
    return evaluated


def eval_cell(sheet: Sheet, row: int, column: str, visited: set) -> Cell:
    cell_address = column + str(row)
    if cell_address in visited:
        return Cell(CellType.ERROR, errors.CIRCULAR_DEP)
    visited.add(cell_address)

    try:
        cell = sheet[row][column]
    except KeyError:
        return Cell(CellType.ERROR, errors.NONEXISTENT_CELL)

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
        evaluated_cell = eval_term(operand, sheet, visited)
        value = evaluated_cell.value
        if evaluated_cell.type == CellType.ERROR:
            return evaluated_cell
        elif evaluated_cell.type == CellType.STRING:
            return Cell(CellType.ERROR, errors.WRONG_ARG)
        elif evaluated_cell.type == CellType.NONE:
            value = 0
        try:
            cell_value = operation_funcs[operation](cell_value, value)
        except ZeroDivisionError:
            return Cell(CellType.ERROR, errors.ZERO_DIV)
    return Cell(CellType.NUMBER, cell_value)


def eval_term(term: str, sheet: Sheet, visited: set) -> Cell:
    if term.isdigit():
        return Cell(CellType.NUMBER, int(term))
    else:
        return eval_cell(sheet, int(term[1]), term[0].upper(), visited)


def format_sheet(sheet: Sheet) -> str:
    result = ''
    sorted_rows = get_sorted_values(sheet)
    for row in sorted_rows:
        sorted_values = get_sorted_values(row)
        result += '\t'.join(map(lambda cell: str(cell.value), sorted_values))
        result += '\n'
    return result


def main() -> None:
    row_count, column_count = read_dimensions()
    sheet = read_input(row_count, column_count)
    evaluated_sheet = eval_sheet(sheet)
    print(format_sheet(evaluated_sheet))


if __name__ == '__main__':
    main()

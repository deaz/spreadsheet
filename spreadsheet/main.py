import re
from enum import Enum
import operator
from typing import Dict
import copy

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
        return Cell(CellType.NONE, None)
    elif cell[0] == '\'':
        return Cell(CellType.STRING, cell[1:])
    elif cell[0] == '=':
        if not is_valid_expression(cell):
            return Cell(CellType.ERROR, '#VALUE!')
        return Cell(CellType.EXPRESSION, cell[1:])
    elif cell.isdigit():
        return Cell(CellType.NUMBER, int(cell))
    else:
        return Cell(CellType.ERROR, '#PARSE!')


def is_valid_expression(cell):
    reference_cell = re.compile(
        r'^=([A-Za-z]\d|\d+)([-+/*]([A-Za-z]\d|\d+))*$')
    return reference_cell.match(cell)


def compute_sheet(sheet: Sheet):
    computed_sheet = copy.deepcopy(sheet)
    for row_index, row in sheet.items():
        for column_letter, cell in row.items():
            if cell.type == CellType.EXPRESSION:
                cell.value = compute_cell(
                    computed_sheet, row_index, column_letter)
                cell.type = CellType.NUMBER


def compute_cell(sheet: Sheet, row: int, column: str):
    cell = sheet[row][column]

    if cell.type != CellType.EXPRESSION:
        # TODO: check for error cell
        return cell.value

    term_re = re.compile(r'[A-Za-z]\d|\d+')
    operation_re = re.compile(r'[-+/*]')
    operation_funcs = {'+': operator.add, '-': operator.sub,
                       '*': operator.mul, '/': operator.floordiv}
    operands = term_re.findall(cell.value)
    operations = operation_re.findall(cell.value)
    cell_value = compute_term(operands[0], sheet)
    for operation, operand in zip(operations, operands[1:]):
        term_value = compute_term(operand, sheet)
        cell_value = operation_funcs[operation](cell_value, term_value)
    return cell_value


def compute_term(term: str, sheet: Sheet):
    if term.isdigit():
        return int(term)
    else:
        return compute_cell(sheet, int(term[1]), term[0].upper())


def format_sheet(sheet: Sheet):
    result = ''
    for row in sheet.values():
        sorted_values = list(zip(*sorted(row.items())))[1]
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

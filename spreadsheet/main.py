import re


def read_input():
    try:
        row_count, column_count = map(int, input().strip().split(' '))
    except ValueError as e:
        raise Exception('Error during reading rows and columns count') from e

    sheet = []
    for row_index in range(row_count):
        try:
            row = list(input().split('\t'))
        except EOFError as e:
            raise Exception('Too few rows') from e
        if len(row) != column_count:
            raise Exception('Too few columns in row {}'.format(row_index + 1))
        sheet.append(row)
    return sheet


def syntax_check(cell):
    if not cell:
        return '*nothing*'
    elif cell[0] == '\'':
        return 'string:' + cell
    elif cell[0] == '=':
        if not reference_check(cell):
            return '#VALUE!'
        return 'expression:' + cell
    elif cell.isdigit():
        return 'number:' + cell
    else:
        return '#PARSE!'


def reference_check(cell):
    reference_cell = re.compile(
        r'^=([A-Za-z]\d|\d+)([-+/*]([A-Za-z]\d|\d+))*$')
    return reference_cell.match(cell)


def parse(sheet):
    new_sheet = []
    for row in sheet:
        new_row = []
        for cell in row:
            new_row.append(syntax_check(cell))
        new_sheet.append(new_row)
    return new_sheet


def main():
    sheet = read_input()
    sheet = parse(sheet)
    print(sheet)


if __name__ == '__main__':
    main()

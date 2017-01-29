def read_input():
    row_count, column_count = map(int, input().strip().split(' '))
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
        return 'expression:' + cell
    elif cell.isdigit():
        return 'number:' + cell
    else:
        return '#PARSE!'


def parse(sheet):
    new_sheet = []
    for row in sheet:
        for cell in row:
            print(syntax_check(cell))


def main():
    sheet = read_input()
    parse(sheet)


if __name__ == '__main__':
    main()

import unittest

import spreadsheet.errors as errors
from spreadsheet.main import format_sheet
from spreadsheet.cell import Cell, CellType


class ParseCellTest(unittest.TestCase):
    def test_format(self):
        sheet = {
            2: {'B': Cell(CellType.NUMBER, 123),
                'A': Cell(CellType.STRING, 'qwe')},
            1: {'A': Cell(CellType.ERROR, errors.CIRCULAR_DEP),
                'B': Cell(CellType.NONE, '')}
        }
        formatted_sheet = (f'{errors.CIRCULAR_DEP}\t\n'
                           f'qwe\t123\n')

        self.assertEqual(format_sheet(sheet), formatted_sheet)

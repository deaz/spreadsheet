import unittest

from spreadsheet.main import parse_cell
from spreadsheet.cell import Cell, CellType


class ParseCellTest(unittest.TestCase):
    def test_none_cell(self):
        self.assertEqual(parse_cell(''), Cell(CellType.NONE, ''))

    def test_string_cell(self):
        pass

    def test_number_cell(self):
        pass

    def test_expression_cell(self):
        pass

    def test_error_cell(self):
        pass

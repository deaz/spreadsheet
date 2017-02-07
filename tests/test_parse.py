import unittest

import spreadsheet.errors as errors
from spreadsheet.main import parse_cell, is_valid_expression
from spreadsheet.cell import Cell, CellType


class ParseCellTest(unittest.TestCase):
    def test_none_cell(self):
        self.assertEqual(parse_cell(''), Cell(CellType.NONE, ''))

    def test_string_cell(self):
        self.assertEqual(parse_cell('\'string'),
                         Cell(CellType.STRING, 'string'))

    def test_number_cell(self):
        self.assertEqual(parse_cell('100500'),
                         Cell(CellType.NUMBER, 100500))

    def test_expression_cell(self):
        self.assertEqual(parse_cell('=1+2+b1'),
                         Cell(CellType.EXPRESSION, '1+2+b1'))
        self.assertEqual(parse_cell('=100+2+b1'),
                         Cell(CellType.EXPRESSION, '100+2+b1'))
        self.assertEqual(parse_cell('=1'),
                         Cell(CellType.EXPRESSION, '1'))
        self.assertEqual(parse_cell('=b1'),
                         Cell(CellType.EXPRESSION, 'b1'))

    def test_error_cell(self):
        self.assertEqual(parse_cell('\t'),
                         Cell(CellType.ERROR, errors.INVALID_SYNTAX))
        self.assertEqual(parse_cell('string'),
                         Cell(CellType.ERROR, errors.INVALID_SYNTAX))
        self.assertEqual(parse_cell('-42'),
                         Cell(CellType.ERROR, errors.INVALID_SYNTAX))
        self.assertEqual(parse_cell(' '),
                         Cell(CellType.ERROR, errors.INVALID_SYNTAX))
        self.assertEqual(parse_cell('='),
                         Cell(CellType.ERROR, errors.INVALID_SYNTAX))
        self.assertEqual(parse_cell('=a1-'),
                         Cell(CellType.ERROR, errors.INVALID_SYNTAX))
        self.assertEqual(parse_cell('=-1'),
                         Cell(CellType.ERROR, errors.INVALID_SYNTAX))
        self.assertEqual(parse_cell('=a+b'),
                         Cell(CellType.ERROR, errors.INVALID_SYNTAX))
        self.assertEqual(parse_cell('=/3'),
                         Cell(CellType.ERROR, errors.INVALID_SYNTAX))


class IsValidExpressionTest(unittest.TestCase):
    def test(self):
        self.assertTrue(is_valid_expression('=1'))
        self.assertTrue(is_valid_expression('=B1'))
        self.assertTrue(is_valid_expression('=B1-3'))
        self.assertFalse(is_valid_expression('=-B1'))
        self.assertFalse(is_valid_expression('1+1'))

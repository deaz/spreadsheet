import unittest

import spreadsheet.errors as errors
from spreadsheet.main import eval_term, eval_cell, eval_sheet
from spreadsheet.cell import Cell, CellType


class EvalTermTest(unittest.TestCase):
    def test(self):
        self.assertEqual(eval_term('123', dict(), set()),
                         Cell(CellType.NUMBER, 123))

        sheet = {1: {'A': Cell(CellType.NUMBER, 100)}}
        self.assertEqual(eval_term('A1', sheet, set()),
                         Cell(CellType.NUMBER, 100))


class EvalCellTest(unittest.TestCase):
    def test(self):
        self.assertEqual(eval_cell(dict(), 3, 'C', {'C3'}),
                         Cell(CellType.ERROR, errors.CIRCULAR_DEP))
        sheet = {1: {'A': Cell(CellType.EXPRESSION, 'a1')}}
        self.assertEqual(eval_cell(sheet, 1, 'A', set()),
                         Cell(CellType.ERROR, errors.CIRCULAR_DEP))

        self.assertEqual(eval_cell(dict(), 3, 'C', set()),
                         Cell(CellType.ERROR, errors.NONEXISTENT_CELL))

        sheet = {1: {'A': Cell(CellType.NUMBER, 123)}}
        self.assertEqual(eval_cell(sheet, 1, 'A', set()),
                         Cell(CellType.NUMBER, 123))

        sheet = {1: {'A': Cell(CellType.EXPRESSION, '10+2/3*4+b1'),
                     'B': Cell(CellType.NONE, '')}}
        self.assertEqual(eval_cell(sheet, 1, 'A', set()),
                         Cell(CellType.ERROR, errors.WRONG_ARG))

        sheet = {1: {'A': Cell(CellType.EXPRESSION, '2/0')}}
        self.assertEqual(eval_cell(sheet, 1, 'A', set()),
                         Cell(CellType.ERROR, errors.ZERO_DIV))

        sheet = {1: {'A': Cell(CellType.EXPRESSION, 'b1'),
                     'B': Cell(CellType.STRING, '123')}}
        self.assertEqual(eval_cell(sheet, 1, 'A', set()),
                         Cell(CellType.STRING, '123'))

        sheet = {1: {'A': Cell(CellType.EXPRESSION, 'b1+2'),
                     'B': Cell(CellType.STRING, '\'123')}}
        self.assertEqual(eval_cell(sheet, 1, 'A', set()),
                         Cell(CellType.ERROR, errors.WRONG_ARG))


class EvalSheetTest(unittest.TestCase):
    def test(self):
        input_sheet = {
            1: {'A': Cell(CellType.NUMBER, 123),
                'B': Cell(CellType.EXPRESSION, '23+a2-73/C2*13'),
                'C': Cell(CellType.ERROR, errors.INVALID_SYNTAX)},
            2: {'A': Cell(CellType.EXPRESSION, 'g1'),
                'B': Cell(CellType.STRING, '=123+b2'),
                'C': Cell(CellType.NUMBER, 6)},
            3: {'A': Cell(CellType.EXPRESSION, '1/b2'),
                'B': Cell(CellType.EXPRESSION, '1/0'),
                'C': Cell(CellType.STRING, 'ok')}
        }
        output_sheet = {
            1: {'A': Cell(CellType.NUMBER, 123),
                'B': Cell(CellType.ERROR, errors.NONEXISTENT_CELL),
                'C': Cell(CellType.ERROR, errors.INVALID_SYNTAX)},
            2: {'A': Cell(CellType.ERROR, errors.NONEXISTENT_CELL),
                'B': Cell(CellType.STRING, '=123+b2'),
                'C': Cell(CellType.NUMBER, 6)},
            3: {'A': Cell(CellType.ERROR, errors.WRONG_ARG),
                'B': Cell(CellType.ERROR, errors.ZERO_DIV),
                'C': Cell(CellType.STRING, 'ok')}
        }
        self.assertEqual(eval_sheet(input_sheet), output_sheet)

from enum import Enum

CellType = Enum('CellType',
                ['NONE', 'NUMBER', 'EXPRESSION', 'STRING', 'ERROR'])


class Cell:
    def __init__(self, cell_type: CellType, cell_value):
        self.type = cell_type
        self.value = cell_value

from enum import Enum
from collections import namedtuple

CellType = Enum('CellType',
                ['NONE', 'NUMBER', 'EXPRESSION', 'STRING', 'ERROR'])

Cell = namedtuple('Cell', ['type', 'value'])

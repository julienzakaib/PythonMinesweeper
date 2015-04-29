__author__ = 'cthulhu'
from enum import Enum


class State(Enum):

    # Hidden State
    Mine = 1
    Empty = 2
    Number = 3

    # Visible State
    Hidden = 4
    Visible = 5
    Flag = 6

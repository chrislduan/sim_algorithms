from enum import Enum


class Color(Enum):
    NONE = None
    UNCOLORED = 0
    P1 = 1
    P2 = 2


NUM_NODES = 6

Board = list[list[Color]]
Edge = tuple[int, int]

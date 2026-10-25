import pytest
from consts import Color
from sim_board import GameBoard


"""
Your GameBoard functions will not be explicitly tested, but they will be used extensively in the process 
of testing your Player2 implementation. If these are not correct, it may cause severe issues with grading.
You should take care to test these rigorously.
"""


def test_color_edge():
    board: GameBoard = GameBoard()
    board.color_edge((0, 1), Color.P1)
    assert board.board == [
        [
            Color.NONE,
            Color.P1,
            Color.UNCOLORED,
            Color.UNCOLORED,
            Color.UNCOLORED,
            Color.UNCOLORED,
        ],
        [
            Color.P1,
            Color.NONE,
            Color.UNCOLORED,
            Color.UNCOLORED,
            Color.UNCOLORED,
            Color.UNCOLORED,
        ],
        [
            Color.UNCOLORED,
            Color.UNCOLORED,
            Color.NONE,
            Color.UNCOLORED,
            Color.UNCOLORED,
            Color.UNCOLORED,
        ],
        [
            Color.UNCOLORED,
            Color.UNCOLORED,
            Color.UNCOLORED,
            Color.NONE,
            Color.UNCOLORED,
            Color.UNCOLORED,
        ],
        [
            Color.UNCOLORED,
            Color.UNCOLORED,
            Color.UNCOLORED,
            Color.UNCOLORED,
            Color.NONE,
            Color.UNCOLORED,
        ],
        [
            Color.UNCOLORED,
            Color.UNCOLORED,
            Color.UNCOLORED,
            Color.UNCOLORED,
            Color.UNCOLORED,
            Color.NONE,
        ],
    ]

    board.color_edge((5, 3), Color.P2)
    assert board.board == [
        [
            Color.NONE,
            Color.P1,
            Color.UNCOLORED,
            Color.UNCOLORED,
            Color.UNCOLORED,
            Color.UNCOLORED,
        ],
        [
            Color.P1,
            Color.NONE,
            Color.UNCOLORED,
            Color.UNCOLORED,
            Color.UNCOLORED,
            Color.UNCOLORED,
        ],
        [
            Color.UNCOLORED,
            Color.UNCOLORED,
            Color.NONE,
            Color.UNCOLORED,
            Color.UNCOLORED,
            Color.UNCOLORED,
        ],
        [
            Color.UNCOLORED,
            Color.UNCOLORED,
            Color.UNCOLORED,
            Color.NONE,
            Color.UNCOLORED,
            Color.P2,
        ],
        [
            Color.UNCOLORED,
            Color.UNCOLORED,
            Color.UNCOLORED,
            Color.UNCOLORED,
            Color.NONE,
            Color.UNCOLORED,
        ],
        [
            Color.UNCOLORED,
            Color.UNCOLORED,
            Color.UNCOLORED,
            Color.P2,
            Color.UNCOLORED,
            Color.NONE,
        ],
    ]


def test_get_winner():
    board: GameBoard = GameBoard()
    board.board = [
        [
            Color.NONE,
            Color.P1,
            Color.UNCOLORED,
            Color.UNCOLORED,
            Color.UNCOLORED,
            Color.UNCOLORED,
        ],
        [
            Color.P1,
            Color.NONE,
            Color.UNCOLORED,
            Color.UNCOLORED,
            Color.UNCOLORED,
            Color.UNCOLORED,
        ],
        [
            Color.UNCOLORED,
            Color.UNCOLORED,
            Color.NONE,
            Color.UNCOLORED,
            Color.UNCOLORED,
            Color.UNCOLORED,
        ],
        [
            Color.UNCOLORED,
            Color.UNCOLORED,
            Color.UNCOLORED,
            Color.NONE,
            Color.UNCOLORED,
            Color.P2,
        ],
        [
            Color.UNCOLORED,
            Color.UNCOLORED,
            Color.UNCOLORED,
            Color.UNCOLORED,
            Color.NONE,
            Color.UNCOLORED,
        ],
        [
            Color.UNCOLORED,
            Color.UNCOLORED,
            Color.UNCOLORED,
            Color.P2,
            Color.UNCOLORED,
            Color.NONE,
        ],
    ]
    assert board.get_winner() is None

    # A board with a red triangle between nodes 0, 1, and 3
    board.board = [
        [
            Color.NONE,
            Color.P1,
            Color.UNCOLORED,
            Color.P1,
            Color.UNCOLORED,
            Color.UNCOLORED,
        ],
        [
            Color.P1,
            Color.NONE,
            Color.UNCOLORED,
            Color.P1,
            Color.UNCOLORED,
            Color.UNCOLORED,
        ],
        [
            Color.UNCOLORED,
            Color.UNCOLORED,
            Color.NONE,
            Color.UNCOLORED,
            Color.UNCOLORED,
            Color.UNCOLORED,
        ],
        [Color.P1, Color.P1, Color.UNCOLORED, Color.NONE, Color.UNCOLORED, Color.P2],
        [
            Color.UNCOLORED,
            Color.UNCOLORED,
            Color.UNCOLORED,
            Color.UNCOLORED,
            Color.NONE,
            Color.UNCOLORED,
        ],
        [
            Color.UNCOLORED,
            Color.UNCOLORED,
            Color.UNCOLORED,
            Color.P2,
            Color.UNCOLORED,
            Color.NONE,
        ],
    ]
    assert board.get_winner() == Color.P2

    # A board with a blue triangle between nodes 2, 3, and 5
    board.board = [
        [
            Color.NONE,
            Color.UNCOLORED,
            Color.UNCOLORED,
            Color.P1,
            Color.UNCOLORED,
            Color.UNCOLORED,
        ],
        [
            Color.UNCOLORED,
            Color.NONE,
            Color.UNCOLORED,
            Color.P1,
            Color.UNCOLORED,
            Color.UNCOLORED,
        ],
        [
            Color.UNCOLORED,
            Color.UNCOLORED,
            Color.NONE,
            Color.P2,
            Color.UNCOLORED,
            Color.P2,
        ],
        [Color.P1, Color.P1, Color.P2, Color.NONE, Color.UNCOLORED, Color.P2],
        [
            Color.UNCOLORED,
            Color.UNCOLORED,
            Color.UNCOLORED,
            Color.UNCOLORED,
            Color.NONE,
            Color.UNCOLORED,
        ],
        [
            Color.UNCOLORED,
            Color.UNCOLORED,
            Color.P2,
            Color.P2,
            Color.UNCOLORED,
            Color.NONE,
        ],
    ]
    assert board.get_winner() == Color.P1

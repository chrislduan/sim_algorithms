import pytest
from consts import Board, Color, Edge, NUM_NODES
from sim_board import GameBoard
from player2 import Player2
from .test_helpers import generate_fig4_board, moveset_equal, create_board


def test_miniboard_starter() -> None:
    # See Fig. 4
    board = generate_fig4_board(None)
    expected_miniboard_1 = generate_fig4_board("b")
    expected_miniboard_2 = generate_fig4_board("c")

    # Act
    miniboard = Player2.get_miniboard(board.board)
    assert (
        miniboard == expected_miniboard_1.board
        # or miniboard == expected_miniboard_2.board
    )


def test_get_allowed_moves_starter() -> None:
    # Initialize a miniboard (Fig. 6b)
    miniboard = generate_fig4_board("b")

    expected_moves = [(0, 1), (0, 2), (0, 3), (0, 4)]
    actual_moves = Player2.get_allowed_moves(Color.P2, miniboard.board)
    assert moveset_equal(frozenset(expected_moves), frozenset(actual_moves))


def test_maximal_allowed_sets_starter() -> None:
    # Initialize a miniboard (Fig. 6b)
    miniboard = generate_fig4_board("b")

    expected_set = frozenset([(0, 1), (0, 3), (0, 4)])

    # Act
    actual_sets = Player2.get_maximal_allowed_sets(Color.P2, miniboard.board)

    # Assert
    assert len(actual_sets) == 1
    assert moveset_equal(expected_set, actual_sets.pop())

def test_maximal_allowed_sets_case_1() -> None:
    # miniboard = [[Color.UNCOLORED for _ in range(NUM_NODES)] for _ in range(NUM_NODES)]

    # miniboard[(0, 1)] = Color.UNCOLORED
    # miniboard[(1, 0)] = Color.UNCOLORED
    # miniboard[(5, 1)] = Color.UNCOLORED
    # miniboard[(1, 5)] = Color.UNCOLORED
    #
    #
    # miniboard[(0, 5)] = Color.P1
    # miniboard[(5, 0)] = Color.P2

    red = [(0,5)]
    miniboard = create_board(red, [])

    miniboard.board[2] = [Color.NONE] * NUM_NODES
    for y in range(NUM_NODES):
        miniboard.board[y][2] = Color.NONE
    miniboard.board[3] = [Color.NONE] * NUM_NODES
    for y in range(NUM_NODES):
        miniboard.board[y][3] = Color.NONE
    miniboard.board[4] = [Color.NONE] * NUM_NODES
    for y in range(NUM_NODES):
        miniboard.board[y][4] = Color.NONE

    miniboard.board[1] = [Color.UNCOLORED, Color.NONE, Color.NONE, Color.NONE, Color.NONE, Color.UNCOLORED]
    miniboard.board[5] = [Color.UNCOLORED, Color.UNCOLORED, Color.NONE, Color.NONE, Color.NONE, Color.NONE]

    # expected_set = frozenset([(0, 1), (1, 5)])
    expected_sets = {frozenset([(0,1)]), frozenset([(1, 5)])}
    # Act
    actual_sets = Player2.get_maximal_allowed_sets(Color.P1, miniboard.board)

    assert moveset_equal(expected_sets.pop(), actual_sets.pop())



def test_get_move_starter() -> None:
    red = [(4, 3), (4, 2), (4, 1)]
    blue = [(3, 2), (2, 1)]

    board = create_board(red, blue)

    possible_moves = [(0, 1), (1, 0), (5, 1), (1, 5), (0, 3), (3, 0), (5, 3), (3, 5)]
    actual_move = Player2.get_move(board.board)

    assert actual_move in possible_moves


def test_get_move_case_1() -> None:
    red = [(0, 1), (1, 2), (1, 3), (1,4), (1,5)]
    blue = [(0, 4), (2, 5), (3, 4), (4,5)]

    board = create_board(red, blue)

    actual_move = Player2.get_move(board.board)

    assert actual_move in [(0,2), (2,0), (2,3), (3,2)]


def test_get_move_case_2() -> None:
    red = [(0,5)]
    blue = []

    board_1 = create_board(red,blue)

    move_1 = Player2.get_move(board_1.board)

    print(move_1)

from __future__ import annotations
from consts import Board, Color, Edge, NUM_NODES
from sim_board import GameBoard
from player2 import Player2


# Checks if two sets of moves/edges are equivalent
def moveset_equal(set1: frozenset[Edge], set2: frozenset[Edge]) -> bool:
    set2_mutable = {edge for edge in set2}
    for edge in set1:
        if edge in set2:
            set2_mutable.remove(edge)
            continue
        edge_reversed = (edge[1], edge[0])
        if edge_reversed in set2:
            set2_mutable.remove(edge_reversed)
            continue
        print(f"Set 1 contains more instances of {edge} than set 2")
        return False
    if len(set2_mutable) != 0:
        print("Set 2 contains elements not found in set 1")
        return False
    return True


# Creates a board with the edges initialized
def create_board(red_edges: list[Edge], blue_edges: list[Edge]) -> GameBoard:
    board = GameBoard()
    for edge in red_edges:
        board.color_edge(edge, Color.P1)
    for edge in blue_edges:
        board.color_edge(edge, Color.P2)
    return board


def generate_fig4_board(miniboard: str | None) -> GameBoard:
    # Initialize colored edges
    red = [(4, 3), (4, 2), (4, 1)]
    blue = [(3, 2), (2, 1)]

    board = create_board(red, blue)
    if miniboard == "b":
        # Remove Node 5
        board.board[5] = [Color.NONE] * NUM_NODES
        for y in range(NUM_NODES):
            board.board[y][5] = Color.NONE
    elif miniboard == "c":
        # Remove Node 0
        board.board[0] = [Color.NONE] * NUM_NODES
        for y in range(NUM_NODES):
            board.board[y][0] = Color.NONE
    return board

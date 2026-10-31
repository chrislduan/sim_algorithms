from __future__ import annotations
from consts import Board, Color, Edge, NUM_NODES


class GameBoard:
    """
    Game board manager class. Encapsulates behaviors concerning the state of the board.
    """

    def __init__(self):
        """
        Initialize `board` as the adjacency matrix for the starting board.
        Use `Color.NONE` for edges that do not exist, and `Color.UNCOLORED` for the other edges.
        """
        # create board of Uncolored Edges
        self.board = [[Color.UNCOLORED for _ in range(NUM_NODES)] for _ in range(NUM_NODES)]
        # traverse across diagonal to label edges None
        for diag in range(NUM_NODES):
            self.board[diag][diag] = Color.NONE


    def color_edge(self, edge: Edge, color: Color) -> None:
        """
        Update `board` to reflect coloring the given edge.
        """
        point_1 = edge[0]
        point_2 = edge[1]
        self.board[point_1][point_2] = color
        self.board[point_2][point_1] = color

    def find_triangle(self, player_color: Color) -> bool:
        """
        Given a Player color, search for the list for triangles
        """

        # get triangle combinations to check by looping over every 3 points
        triangle_combos = []
        for i in range(0 , NUM_NODES - 2):
            for j in range(i + 1, NUM_NODES - 1):
                for k in range(j + 1, NUM_NODES):
                    forms_triangle = self.board[i][j] == player_color and self.board[i][k] == player_color and self.board[j][k] == player_color
                    if forms_triangle:
                        return True

        # if no triangle return none
        return False


    def get_winner(self) -> Color | None:
        """
        Return the color of the player that has won (Color.P1 or Color.P2).
        If the game is still in progress (no one has won yet), return None.
        """
        # if we find triangle for P1, then P2 wins
        if self.find_triangle(Color.P1):
            return Color.P2
        # if we find triangle for P2, then P1 wins
        if self.find_triangle(Color.P2):
            return Color.P1
        return None



    def __str__(self):
        """
        Formats the board as a string. Provided for your convenience while debugging.
        """
        string = ""
        for row in self.board:
            for item in row:
                string += "{edge:<10}".format(edge=item.name)
            string += "\n"
        return string

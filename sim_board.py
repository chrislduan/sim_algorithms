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
        self.board = [[Color.UNCOLORED for _ in range(6)] for _ in range(6)]
        # traverse across diagonal to label edges None
        for diag in range(6):
            self.board[diag][diag] = Color.NONE


    def color_edge(self, edge: Edge, color: Color) -> None:
        """
        Update `board` to reflect coloring the given edge.
        """
        point_1 = edge[0]
        point_2 = edge[1]
        self.board[point_1][point_2] = color
        self.board[point_2][point_1] = color

    def find_triangle(self, player_color: Color):
        """
        Given a Player color, search for the list for triangles
        """
        # set of nodes
        node_set = set()
        # set of edges
        edge_set = set()
        for row in len(self.board):
            for col in len(self.board[row]):
                edge = self.board[row][col]
                # add edge to player's set of nodes if it matches player
                if edge == player_color:
                    node_set.add(edge[0])
                    node_set.add(edge[1])
                    edge_set.add(edge)

        # if number of nodes, there cannot be any triangles
        if len(node_set) < 3:
            return False

        # get triangle combinations to check, list of 3-edge lists
        # using our list of nodes
        triangle_combos = []
        for i in range(0 , len(node_set) - 2):
            for j in range(i + 1, len(node_set) - 1):
                for k in range(j + 1, len(node_set)):
                    edge_1 = (node_set[i], node_set[j])
                    edge_2 = (node_set[j], node_set[k])
                    edge_3 = (node_set[k], node_set[i])

                    triangle_combos.append([edge_1, edge_2, edge_3])

        # check if triangle combination exists in our edge set
        for combo in triangle_combos:
            if combo[0] in edge_set and combo[1] in edge_set and combo[2] in edge_set:
                return True

        # if no triangle return none
        return False


    def get_winner(self) -> Color | None:
        """
        Return the color of the player that has won (Color.P1 or Color.P2).
        If the game is still in progress (no one has won yet), return None.
        """
        # raise NotImplementedError

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

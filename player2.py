from __future__ import annotations

from typing import Any

from consts import Board, Color, Edge, NUM_NODES


class Player2:
    """
    Implements a winning strategy for the second player in a game of Sim
    """

    @staticmethod
    def get_move(board: Board) -> Edge:
        """
        Return a possible move for the second player (blue) that follows the optimal strategy laid out in the handout,
        given the input board state. If multiple moves are viable, this method can return any of them.
        """
        # get miniboard
        miniboard = Player2.get_miniboard(board)

        # get allowed moves
        allowed_moves = Player2.get_allowed_moves(Color.P2, miniboard)

        # if only on allowed_move, choose that move
        if len(allowed_moves) == 1:
            return allowed_moves[0]

        # get maximal allowed set for p2
        p2_maximal_allowed_sets = Player2.get_maximal_allowed_sets(Color.P2, miniboard)

        # if only one move within p2 maximal allowed set, return it
        if len(p2_maximal_allowed_sets) == 1 and len(p2_maximal_allowed_sets[0]):
            return allowed_moves[0]

        # get maximal allowed set for p1
        p1_maximal_allowed_sets = Player2.get_maximal_allowed_sets(Color.P1, miniboard)

        # find move that appears in most maximal_allowed_set
        move_count: dict[Edge, int] = dict()
        for move_set in p1_maximal_allowed_sets:
            for move in move_set:
                if move not in move_set:
                    move_count[move] = 1
                else:
                    move_count[move] += 1

        # get the maximum count within move_count
        next_move = max(move_count, key=move_count.get)
        return next_move

    @staticmethod
    def get_miniboard(board: Board) -> Board | None:
        """
        Return a miniboard from the input board state. If there are multiple miniboards, this method can return any of them.
        """
        colored_board = board

        # list of colored nodes
        colored_nodes = []

        # remove all non-colored edges on the board and get list of colored nodes
        for i in range(len(board)):
            for j in range(len(board[i])):
                if board[i][j] == Color.UNCOLORED:
                    colored_board[i][j] = Color.NONE
                if board[i][j] == Color.P1 or board[i][j] == Color.P2:
                    if i not in colored_nodes:
                        colored_nodes.append(i)
                    if j not in colored_nodes:
                        colored_nodes.append(j)

        # get list of possible nodes to add to the board (dictionary of lists, keyed on nodes)
        # by finding the nodes without any colored edges
        node_uncolored_edge_count = {
            0: [],
            1: [],
            2: [],
            3: [],
            4: [],
            5: []
        }
        for i in range(len(board)):
            for j in range(len(board[i])):
                # check through edges marked none that are not diagonals
                if board[i][j] == Color.NONE and i != j:
                    # correct board such that any node with colored edges will have uncolored edges as well
                    if i in colored_nodes and j in colored_nodes:
                        colored_board[i][j] = Color.UNCOLORED
                    # add to non_colored_edge count if the node is not part of the colored set
                    if i not in colored_nodes:
                        node_uncolored_edge_count[i].append(j)

        # go through every node
        for node in node_uncolored_edge_count:
            # if all edges are colored, skip
            if len(node_uncolored_edge_count[node]) == 0:
                continue
            # create a miniboard including all colored edges and uncolored edges linking to current node
            miniboard = colored_board
            # mark all edges connected to node as uncolored
            for i in range(NUM_NODES):
                # set all edges related to node and a colored node as uncolored except for diagonal
                if i in colored_nodes and miniboard[node][i] == Color.NONE and node != i:
                    # color node in both directions
                    miniboard[node][i] = Color.UNCOLORED
                    miniboard[i][node] = Color.UNCOLORED

            # check if there is at least one allowed move for P2 on this board
            allowed_moves = Player2.get_allowed_moves(Color.P2, miniboard)

            if len(allowed_moves) > 1:
                return miniboard

        return None

    @staticmethod
    def get_power_set(move_set: list):
        """
        Using recursion to get power set of move list
        """
        # define base case, returning set with emtpy set if set is not a list
        if not move_set:
            return [[]]

        # recursively get the smaller power sets by using given set with last item removed
        collected_sets = Player2.get_power_set(move_set[:-1])

        # retrieve last item
        last_item = move_set[-1]

        # loop through each item in subset to get all possible lists with last_item
        power_set = []
        for subset in collected_sets:
            power_set.append(subset + [last_item])

        return collected_sets + power_set

    @staticmethod
    def get_maximal_allowed_sets(player: Color, board: Board) -> set[frozenset[Edge]]:
        """
        Return a set of all distinct maximal allowed sets for the given player over the input board state.
        If player is Color.P1, find all maximal p1-allowed sets; if player is Color.P2, find all maximal p2-allowed sets.
        """
        allowed_moves = Player2.get_allowed_moves(player, board)

        # get every possible combination of allowed_moves by getting the power set
        # moves_power_set = Player2.get_power_set(allowed_moves)
        # # sort power set by size of each set in it, largest set first
        # moves_power_set.sort(key=len, reverse = True)
        #
        # # get every possible set of allowed_moves that doesn't make triangle in given board
        # maximal_set = []
        # for move_set in moves_power_set:
        #     # if size of current set is smaller than our maximal set, skip check
        #     if len(move_set) < len(maximal_set):
        #         continue
        #
        #     # loop through every edge in move_set, and create a demo board
        #     demo_board = board

        def has_triangle(player: Color, miniboard: Board):
            player_edges = []
            for row in range(len(board)):
                for col in range(row, len(board[row])):
                    if miniboard[row][col] == player:
                        player_edges.append((row, col))
            for edge in player_edges:
                p1, p2 = edge
                for p3 in range(NUM_NODES):
                    if p3 == p1 or p3 == p2:
                        continue

                    # get ordered pair edges that could possibly make a triangle
                    edge_1 = (min(p1, p3), max(p1, p3))
                    edge_2 = (min(p2, p3), max(p2, p3))

                    if edge_1 in player_edges and edge_2 in player_edges:
                        return True
            return False

        # implement using a dfs
        maximal_set = []
        largest_set_length = 0

        # helper function to go over moves
        def move_dfs(move_set, board: Board):
            visited_edges.append(move_set[0])
            move_list = []
            for move in move_set:
                p1, p2 = move
                move_board = board
                move_board[p1][p2] = player
                move_board[p2][p1] = player
                forms_triangle = has_triangle(player, move_board)
                if not forms_triangle:
                    move_list.extend(move_dfs(move_set[1:], move_board))
                    move_list.append(move)
                if forms_triangle:
                    if len(visited_edges) > 0:
                        visited_edges.pop()
                    return []
                if len(visited_edges) > 0:
                    visited_edges.pop()
            return move_list

        # for move in allowed_moves:
        #     move_stack = [move]

        # do a depth first search for each move set to see if it makes a triangle
        while len(allowed_moves) > 0:
            visited_edges = []
            current_move_set = move_dfs(allowed_moves, board)
            if len(current_move_set) > 0:
                if len(current_move_set) == largest_set_length:
                    maximal_set.append(current_move_set)
                elif len(current_move_set) > largest_set_length:
                    maximal_set = [current_move_set]
                    largest_set_length = len(current_move_set)
            allowed_moves.pop(0)


        return maximal_set

    @staticmethod
    def get_allowed_moves(player: Color, board: Board) -> list[Edge]:
        """
        Return a list of all distinct valid moves for the given player over the input board state.
        """
        # get list of uncolored edges and player edges
        player_edges = []
        uncolored_edges = []
        for row in range(len(board)):
            # doing range of col greater than row, that way we only look at ordered edges
            # i.e. only listing (0,1) and (1,2) instead of the former and (1, 0) and (2, 10)
            for col in range(row, len(board[row])):
                if board[row][col] == Color.UNCOLORED:
                    uncolored_edges.append((row, col))
                elif board[row][col] == player:
                    player_edges.append((row, col))

        # create list of allowed moves by going through every uncolored edge
        allowed_moves = []
        for edge in uncolored_edges:
            p1, p2 = edge
            triangle = False

            # loops through available points, checking if they make a triangle
            for p3 in range(NUM_NODES):
                # skip if we are already using that point
                if p3 == p1 or p3 == p2:
                    continue

                # get ordered pair edges that could possibly make a triangle
                edge_1 = (min(p1, p3), max(p1, p3))
                edge_2 = (min(p2, p3), max(p2, p3))

                # checks if it forms a triangle
                if edge_1 in player_edges and edge_2 in player_edges:
                    triangle = True
                    break

            if not triangle:
                allowed_moves.append(edge)

        return allowed_moves

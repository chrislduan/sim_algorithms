from __future__ import annotations

from typing import Any

import itertools

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

        # helper function to create copy of a given board, prevents pointer issues
        def copy_board(original: Board) -> Board:
            copied_board = [[Color.UNCOLORED for _ in range(NUM_NODES)] for _ in range(NUM_NODES)]
            for row in range(NUM_NODES):
                for col in range(NUM_NODES):
                    copied_board[row][col] = original[row][col]
            return copied_board

        copy_of_board = copy_board(board)


        # get miniboard
        miniboard = Player2.get_miniboard(copy_of_board)

        # case if miniboard is none, use the whole board
        if miniboard is None:
            miniboard = copy_board(copy_of_board)

        # get allowed moves
        allowed_moves = Player2.get_allowed_moves(Color.P2, miniboard)

        # if only on allowed_move, choose that move
        if len(allowed_moves) == 1:
            return allowed_moves[0]

        # get maximal allowed set for p2
        p2_maximal_allowed_sets = Player2.get_maximal_allowed_sets(Color.P2, miniboard)

        # find moves that appear in most p2 maximal sets
        p2_maximal_move_counts = dict()
        maximum_appearances = 0
        for move in allowed_moves:
            # counter for how many sets a move appears in a p2 maximal sets
            move_appearances = 0
            for move_set in p2_maximal_allowed_sets:
                if move in move_set:
                    move_appearances += 1
            # add to p2_maximal_move_counts dictionary
            p2_maximal_move_counts[move] = move_appearances
            if move_appearances > maximum_appearances:
                maximum_appearances = move_appearances

        # parse through dictionary of move counts and get list of moves that appear in most (best moves)
        p2_best_moves = []
        for move_key in p2_maximal_move_counts.keys():
            appearances = p2_maximal_move_counts[move_key]
            if appearances == maximum_appearances:
                p2_best_moves.append(move_key)

        if len(p2_best_moves) == 1:
            return p2_best_moves[0]

        # get maximal allowed set for p1
        p1_maximal_allowed_sets = Player2.get_maximal_allowed_sets(Color.P1, miniboard)
        p1_allowed_moves = Player2.get_allowed_moves(Color.P1, miniboard)

        # when p1 has no choices, choose first move from the best p2 moves
        if len(p1_allowed_moves) == 0:
            return p2_best_moves[0]


        # find move that appears in most maximal_allowed_set
        most_p1_move = p2_best_moves[0]
        p1_move_count = -1
        # using p2 moves used most in maximal p2 sets and find the move in the most p1 maximal allowed sets
        # returning the first one that is found if there are multiple that appear the maximum amount
        for move in p2_best_moves:
            move_count = 0
            for move_set in p1_maximal_allowed_sets:
                if move in move_set:
                    move_count += 1
            if move_count > p1_move_count:
                p1_move_count = move_count
                most_p1_move = move

        return most_p1_move

    @staticmethod
    def get_miniboard(board: Board) -> Board | None:
        """
        Return a miniboard from the input board state. If there are multiple miniboards, this method can return any of them.
        """
        # list of colored nodes
        colored_nodes = []

        # remove all non-colored edges on the board and get list of colored nodes
        for i in range(len(board)):
            for j in range(len(board[i])):
                if board[i][j] == Color.P1 or board[i][j] == Color.P2:
                    if i not in colored_nodes:
                        colored_nodes.append(i)
                    if j not in colored_nodes:
                        colored_nodes.append(j)

        # get list of possible nodes to add to board
        possible_nodes = []
        for node in range(NUM_NODES):
            if node not in colored_nodes:
                possible_nodes.append(node)

        # go through every possible combination of remaining nodes to see if it creates a valid miniboard
        # check if we can add 0, 1, 2, ... N nodes to the board
        for num_added_nodes in range(len(possible_nodes) + 1):
            # loop through every possible combination of added nodes
            for added_nodes in itertools.combinations(possible_nodes, num_added_nodes):
                # create list of nodes
                nodes = []
                # add all colored nodes
                for node in colored_nodes:
                    nodes.append(node)
                # add possible combination of additional nodes we have to our miniboard to test
                for node in added_nodes:
                    if node not in nodes:
                        nodes.append(node)

                # sort for sake of ease in making miniboard
                nodes.sort()

                # create a miniboard
                miniboard = [[Color.NONE for _ in range(NUM_NODES)] for _ in range(NUM_NODES)]

                # mark diagonal as none
                for i in range(NUM_NODES):
                    miniboard[i][i] = Color.NONE

                # copy the edges from our board that we have nodes for
                for i in range(len(nodes)):
                    for j in range(i + 1, len(nodes)):
                        point_1 = nodes[i]
                        point_2 = nodes[j]
                        miniboard[point_1][point_2] = board[point_1][point_2]
                        miniboard[point_2][point_1] = board[point_2][point_1]

                # get list of allowed moves on our current miniboard
                allowed_moves = Player2.get_allowed_moves(Color.P2, miniboard)

                # check if allowed moves is empty, if so, try next possible miniboard
                if len(allowed_moves) == 0:
                    continue

                # track if smallest board
                is_smallest_board = True

                # loop through every node to see if we can remove it and get a valid miniboard
                for removed_node in nodes:
                    # skip colored nodes as we cannot remove them
                    if removed_node in colored_nodes:
                        continue

                    # remove the current node and make new set of remaining nodes
                    remaining_nodes = []
                    for node in nodes:
                        if node != removed_node:
                            remaining_nodes.append(node)

                    # create new temporary miniboard that has lost the removed node
                    temp_miniboard = [[Color.NONE for _ in range(NUM_NODES)] for _ in range(NUM_NODES)]
                    for i in range(NUM_NODES):
                        temp_miniboard[i][i] = Color.NONE

                    # copy the edges from our board that we have nodes for
                    for i in range(len(remaining_nodes)):
                        for j in range(i + 1, len(remaining_nodes)):
                            point_1 = remaining_nodes[i]
                            point_2 = remaining_nodes[j]
                            temp_miniboard[point_1][point_2] = board[point_1][point_2]
                            temp_miniboard[point_2][point_1] = board[point_2][point_1]

                    # check if this temp miniboard with removed node has P2 allowed moves
                    temp_allowed_moves = Player2.get_allowed_moves(Color.P2, temp_miniboard)
                    # if new temp board has allowed moves, we are not at smallest board, so continue to next
                    if len(temp_allowed_moves) > 0:
                        is_smallest_board = False
                        break

                # after checking all possible removed nodes, if still smallest board, return it
                if is_smallest_board:
                    return miniboard

        return None




    @staticmethod
    def get_maximal_allowed_sets(player: Color, board: Board) -> set[frozenset[Edge]]:
        """
        Return a set of all distinct maximal allowed sets for the given player over the input board state.
        If player is Color.P1, find all maximal p1-allowed sets; if player is Color.P2, find all maximal p2-allowed sets.
        """

        # first get allowed moves on a board
        allowed_moves = Player2.get_allowed_moves(player, board)

        # helper function to check if a miniboard has triangle
        def has_triangle(player: Color, miniboard: Board):
            # loop through every set of 3 nodes
            for i in range(0, NUM_NODES - 2):
                for j in range(i + 1, NUM_NODES - 1):
                    for k in range(j + 1, NUM_NODES):
                        forms_triangle = (miniboard[i][j] == player and miniboard[i][k] == player and
                                         miniboard[j][k] == player)
                        if forms_triangle:
                            return True
            return False

        # searching through lists of length N to 0 for allowed sets, largest to smallest
        # such as if given 4 moves, check if all 4 is an allowed set, and stop if so
        ## If not, go to next length, 3, check if any combinations of 3 moves is an allowed set, and stop if so
        ## otherwise proceed down the list
        # iterate through size N to 0
        for size in range(len(allowed_moves), 0, -1):
            maximal_sets = set()

            # get all possible combinations of current size
            for move_combo in itertools.combinations(allowed_moves, size):
                # create a copy of board for checking
                check_board = [row[:] for row in board]
                valid_move_set = True

                # check if every move in move_combination is allowed together
                for point_1, point_2 in move_combo:
                    check_board[point_1][point_2] = player
                    check_board[point_2][point_1] = player
                    forms_triangle = has_triangle(player, check_board)
                    if forms_triangle:
                        valid_move_set = False

                # checks if no triangle has formed, and adds to list as frozen set
                if valid_move_set:
                    maximal_sets.add(frozenset(move_combo))

            # stop if set list is not empty, and return the move set of all maximal moves
            if maximal_sets:
                return maximal_sets

        # return empty set if no moves found
        return set()




    @staticmethod
    def get_allowed_moves(player: Color, board: Board) -> list[Edge]:
        """
        Return a list of all distinct valid moves for the given player over the input board state.
        """
        # get list of uncolored edges and set of player edges
        player_edges = set()
        uncolored_edges = []
        for row in range(len(board)):
            # doing range of col greater than row, that way we only look at ordered edges
            # i.e. only listing (0,1) and (1,2) instead of the former and (1, 0) and (2, 10)
            for col in range(row + 1, len(board[row])):
                if board[row][col] == Color.UNCOLORED:
                    uncolored_edges.append((row, col))
                elif board[row][col] == player:
                    player_edges.add((row, col))

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
            # add move to allowed moves if no triangle is formed
            if not triangle:
                allowed_moves.append(edge)

        return allowed_moves

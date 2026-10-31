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
        if not miniboard:
            miniboard = copy_of_board.copy()

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

        # when p1 has no choices, choose first move from p2 allowed
        if len(p1_allowed_moves) == 0:
            return allowed_moves[0]


        # find move that appears in most maximal_allowed_set
        most_p1_move = p1_allowed_moves[0]
        p1_move_count = 0
        for move in p1_allowed_moves:
            # check if p1 move is in the move(s) contained in the greatest number of maximal P2-allowed sets
            if move in p2_best_moves:
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
        colored_board = board.copy()

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
        for i in range(NUM_NODES):
            for j in range(NUM_NODES):
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
    def get_maximal_allowed_sets(player: Color, board: Board) -> set[frozenset[Edge]]:
        """
        Return a set of all distinct maximal allowed sets for the given player over the input board state.
        If player is Color.P1, find all maximal p1-allowed sets; if player is Color.P2, find all maximal p2-allowed sets.
        """

        # helper function to create copy of a given board to start mini board
        def local_copy_board(original: Board) -> Board:
            copied_board = [[Color.UNCOLORED for _ in range(NUM_NODES)] for _ in range(NUM_NODES)]
            for row in range(NUM_NODES):
                for col in range(NUM_NODES):
                    copied_board[row][col] = original[row][col]
            return copied_board

        copy_of_board = local_copy_board(board)

        # first get allowed moves on a board
        allowed_moves = Player2.get_allowed_moves(player, copy_of_board)

        # helper function to check if a miniboard has triangle
        def has_triangle(player: Color, miniboard: Board):
            # make list of player edges
            player_edges = []
            for row in range(NUM_NODES):
                for col in range(row, NUM_NODES):
                    if miniboard[row][col] == player:
                        player_edges.append((row, col))

            # grab each edge
            for edge in player_edges:
                p1, p2 = edge
                # check each point not connected to the edge and simulate the triangle it makes
                for p3 in range(NUM_NODES):
                    if p3 == p1 or p3 == p2:
                        continue

                    # get ordered pair edges that could possibly make a triangle
                    edge_1 = (min(p1, p3), max(p1, p3))
                    edge_2 = (min(p2, p3), max(p2, p3))

                    # check if all edges of simulated triangle belong to player
                    if edge_1 in player_edges and edge_2 in player_edges:
                        return True
            return False

        # helper function to do a breadth first search of moves
        # searching through lists of length N to 0 for allowed sets
        # such as if given 4 moves, check if all 4 is an allowed set, and stop if so
        ## If not, go to next length, 3, check if any combinations of 3 moves is an allowed set, and stop if so
        ## otherwise proceed down the list
        def move_bfs(move_set, board: Board):

            # copy the given move set and board
            copied_move_set = move_set.copy()
            move_board = local_copy_board(board)

            # current length lists
            # using set of tuples to prevent duplicate move combinations
            current_length_set = {tuple(copied_move_set)}

            # loop through current length
            while current_length_set:
                length_allowed_moves = []
                next_length_set = set()

                for possible_set in current_length_set:
                    # turn set into list
                    possible_set_list = list(possible_set)

                    # create a copy of board for checking
                    check_board = local_copy_board(move_board)
                    valid_list = True
                    # check if every move in set is allowed
                    for move in possible_set_list:
                        point_1, point_2 = move
                        check_board[point_1][point_2] = player
                        check_board[point_2][point_1] = player
                        forms_triangle = has_triangle(player, check_board)
                        if forms_triangle:
                            valid_list = False

                    # checks if any no triangle has formed
                    if valid_list:
                        length_allowed_moves.append(possible_set_list)

                    # if no matches were found with current length, move to next length
                    if not length_allowed_moves:
                        for i in range(len(possible_set_list)):
                            # create the next possible combinations out of each object in list
                            next_combo = tuple(possible_set_list[:i] + possible_set_list[i+1:])
                            next_length_set.add(next_combo)

                # stop if set list is not empty
                if length_allowed_moves:
                    return length_allowed_moves

                # move to next possible length
                current_length_set = next_length_set

            # final case return empty list
            return []

        result_sets = []
        maximal_sets = move_bfs(allowed_moves, copy_of_board)
        for moveset in maximal_sets:
            result_sets.append(frozenset(moveset))
        result_sets = frozenset(maximal_sets)
        return result_sets



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
            # add move to allowed moves if no triangle is formed
            if not triangle:
                allowed_moves.append(edge)

        return allowed_moves

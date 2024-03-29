from random import randint

BOARD_SIZE = 8

# Mapping player and direction to x, y change in board
ACTIONS = {
    1: {
        "Right": (1, 1),
        "Left": (1, -1)
    },
    2: {
        "Right": (-1, 1),
        "Left": (-1, -1)
    }
}


def read_board():
    """ Read in game board

    Read in the game board from stdin

    :returns Dictionary of board with following properties:
        - 1: List of player one locations on board
        - 2: List of player two attributes on board

        Locations are tuples in the form (x, y)

    """
    board = {
        1: [],
        2: []
    }

    for i in range(BOARD_SIZE):
        tmp_row = [int(x) for x in input().split()]
        for j in range(BOARD_SIZE):
            if tmp_row[j] != 0:
                board[tmp_row[j]].append((i, j))

    return board


def print_move(move, reason):
    """ Print a move of with reason

    Prints a move off in following format:
        StartY, StartX
        NumMoves
        MoveY MoveX (For NumMoves times)
        Reason

    :param dict move: Dictionary of the move to be printed

    :param string reason: Reason to make move (any comment on move)

    """
    # Print starting location and number of moves
    move_str = str(move["start"][0]) + " " + str(move["start"][1]) + "\n"
    move_str += str(len(move["locations"])) + "\n"

    # Add landing locations
    for i in range(len(move["locations"])):
        locations = move["locations"][i]
        move_str += str(locations[0]) + " " + str(locations[1])

        # Add new line on all but last location
        if i < len(move["locations"]) - 1:
            move_str += "\n"

    print(move_str)
    print(reason)


def get_location(board, piece):
    """ Given a tuple, retrieve location on board

    :param dict board: Board to get piece at

    :param tuple piece: Tuple of piece location to get (x, y)

    :raises IndexError if piece out of bounds

    :returns Value at given index in board

    """
    # Raise error if trying to look at piece out of bounds
    if (piece[0] < 0 or piece[1] < 0 or
       piece[0] >= BOARD_SIZE or piece[1] >= BOARD_SIZE):
        raise IndexError("IndexError: Piece out of bounds")

    # Default to empty space
    val = 0

    # Check if location contains a piece
    if piece in board[1]:
        val = 1
    elif piece in board[2]:
        val = 2

    return val


def move_result(board, move, player):
    """ Get board after given move is made

    Simulate move being made on given board and return resulting board

    :param list board: Board to simulate move on

    :param dict move: Move to simulate on board

    :param int player: Player that is making move

    :returns New board representation with move executed. Opponent pieces
        that got jumped will be removed and piece will be in ending location

    """
    # Duplicate board
    new_board = {
        1: [x for x in board[1]],
        2: [x for x in board[2]]
    }

    # Get opponent
    opp = 2 if player == 1 else 1

    # Move piece from start to end
    piece = move["start"]
    new_piece = move["locations"][-1]

    # Remove piece from player
    new_board[player].remove(piece)
    new_board[player].append(new_piece)

    # Remove all jumped pieces
    new_board[opp] = [x for x in board[opp] if x not in move["pieces_jumped"]]

    return new_board


def possible_jumps(board, player, piece):
    """ Get possible jumps a piece can make

    Given a piece, see if any opponent pieces can be (single) jumped

    :param dict board: Board to examine scenario

    :param int player: Number of player to check for jumps (1 or 2)

    :param tuple piece: Piece to check on board (y, x)

    :returns List of tuples where first value is place being jumped to
        and second value is location of piece being jumped

    """
    # Get actions
    actions = ACTIONS[player]

    # Get opponent number
    opp = 2 if player == 1 else 1

    # Array of jump locations (because possible to make up to two jumps)
    jump_locations = []

    # Generate left and right pieces
    for a in actions:
        new_loc = (piece[0] + actions[a][0], piece[1] + actions[a][1])

        # Check for jump left
        try:
            if get_location(board, new_loc) == opp:
                # Check to see if next piece open to jump
                nxt = (new_loc[0] + actions[a][0], new_loc[1] + actions[a][1])

                # Next location has to be open
                try:
                    if get_location(board, nxt) == 0:
                        # Jump possible add location
                        jump_locations.append((nxt, new_loc))
                    else:
                        pass
                except IndexError:
                    # Off board
                    pass
        except IndexError:
            # Caught index errror (jump out of bounds stop trying)
            pass

    return jump_locations


def get_move(board, player, piece, direction):
    """ Generate a move given a piece and direction if possible

    Given a piece location and direction, determine the following moves
        that can be made accounting for mandatory jumping.

    :param dict board: Board to check move on

    :param int player: Player to check move of (1 or 2)

    :param tuple piece; Piece to make the move on (y, x)

    :param string direction: Direction to make move (Left or Right)

    :returns Move if possile, None if move is invalid
        Move object contains following attributes:
            -start (tuple): Piece starting location (y, x)
            -locations (list): List of locations piece being moved to
            -pieces_jumped (list): List of pieces being jumped in move

    """
    # Get cooresponding action
    action = ACTIONS[player][direction]

    # Calculate coordinates of the new score
    new_location = (piece[0] + action[0], piece[1] + action[1])

    # Start building move
    move = {
        "start": piece,
        "locations": [],
        "pieces_jumped": []
    }

    # Try/Except to allow checking if on board
    try:
        on_board = get_location(board, new_location)
    except IndexError:
        # Can not make move
        return None

    # Check if space open
    if on_board == 0:
        # Possible to move
        move["locations"].append(new_location)
        return move
    elif on_board == player:
        # Player piece there, impossible move
        return None
    else:
        # Opponent on new location, check if jumps possible
        other_side = (new_location[0] + action[0], new_location[1] + action[1])

        # Try/Except to allow checking if on board
        try:
            jump_spot = get_location(board, other_side)
        except IndexError:
            # Can not make move
            return None

        if jump_spot == 0:
            # Jump can be made
            move["locations"].append(other_side)

            # Add piece to jumped pieces
            move["pieces_jumped"].append(new_location)

            # Check for double/triple jumps
            possible = possible_jumps(board, player, other_side)

            while len(possible) != 0:
                # TODO: Will only make one move even if two possible
                next_move = possible[0]

                # Add to list
                move["locations"].append(next_move[0])

                # Add piece jumped
                move["pieces_jumped"].append(next_move[1])

                # Look for more possible
                possible = possible_jumps(board, player, next_move[0])

            return move
        else:
            # Jump can not be made
            return None


def get_available_moves(board, player):
    """ Get all available moves

    Get a list of all available moves for a given player

    :param dict board: Board to check

    :param int player: Player to get possible moves for (1 or 2)

    :returns List of all possible moves

    """
    pieces = board[player]
    actions = ["Left", "Right"]
    moves = []

    # Loop through all pieces and test moves
    for piece in pieces:
        for action in actions:
            move = get_move(board, player, piece, action)

            if move is not None:
                moves.append(move)

    return moves


def safe_pieces(board, player):
    """ Get number of safe pieces

    Get number of pieces that are safe for the rest of the game. IE, past
        every opponent piece

    :param dict board: Board to look at

    :param int player: Player to look at board for

    :returns List of pieces that are safe for given player

    """
    # To get least moved piece get min y for player 1 and max y for 2
    min_max = {1: min, 2: max}

    # Get opponent
    opp = 2 if player == 1 else 1

    # Get lowest opponent
    if len(board[opp]) == 0:
        return board[player]

    lowest = min_max[opp](board[opp], key=lambda x: x[0])

    # Get list of pieces "lower" than lowest opponent
    if opp == 2:
        safe = [x for x in board[player] if x[0] >= lowest[0]]
    else:
        safe = [x for x in board[player] if x[0] <= lowest[0]]

    return safe


def get_vulnerable(board, player):
    """ Get vulnerable pieces

    Get pieces for player that have a path to be jumped. So either
        front/right and back/left and/or front/left and back/right are both
        open

    :param dict board: Reference to board to look at

    :param int player: Player to look at

    :returns list of pieces that are vulnerable

    """
    # Get Actions
    actions = ACTIONS[player]

    # Start with empty list
    vulnerable = []

    # Analyze all player moves to see if empty space behind
    for move in board[player]:
        for a in actions:
            back = (move[0] - actions[a][0], move[1] - actions[a][1])
            forward = (move[0] + actions[a][0], move[1] + actions[a][1])

            # Check direction
            try:
                if (get_location(board, back) == 0 and
                   get_location(board, forward)):
                    vulnerable.append(move)
            except IndexError:
                pass

    return vulnerable


def score_board(board, move, player):
    """ Scores board for opponent

    Scores the board with the following metrics:
        num_player - Number of player pieces on board
        num_opponent - Number of opponent pieces on board
        player_safe - Guaranteed scores for player
        opp_safe - Guaranteed scores for opponent
        can_be_jumped - Player pieces that can be jumped on opp next turn
        player_wall - Player pieces on the wall
        opp_wall - Opponent pieces on the wall
        player_vul - Player pieces that can be jumped but not immediately

    :param dict board: Board to score

    :param int player: Player to score board for

    :returns Integer score for given board

    """
    # Get opponent
    opp = 2 if player == 1 else 1

    # Start score
    score = 0

    # Number jumped in move
    num_jumped = len(move["pieces_jumped"])

    # Count number of pieces for player and opponent
    num_player = len(board[player])
    num_opponent = len(board[opp])

    """ Player Count Score """
    score += 2 * (num_player - num_opponent)

    # Get guaranteed safe pieces
    player_safe = safe_pieces(board, player)
    opp_safe = safe_pieces(board, opp)

    # Get available opponent moves
    opp_moves = get_available_moves(board, opp)
    player_moves = get_available_moves(board, player)

    avg_move_per_piece = len(player_moves) / num_player
    avg_move_per_piece_opp = len(opp_moves) / num_opponent

    """ Win Conditions """
    # Return high score if move wins game
    if num_opponent == 0 or len(player_safe) > num_opponent:
        score += 9999999

    if len(opp_moves) == 0 and num_player > num_opponent:
        score += 9999999

    # Count best jump
    if len(opp_moves) > 0:
        # Find most number of pieces opponent can take
        opp_best_move = max(opp_moves, key=lambda x: len(x["pieces_jumped"]))
        opp_most_take = len(opp_best_move["pieces_jumped"])

        # Analyze player move for trade
        next_board = move_result(board, opp_best_move, opp)

        next_moves = get_available_moves(next_board, player)

        if len(next_moves) > 0:
            most_take = max(next_moves, key=lambda x: len(x["pieces_jumped"]))
            most_take = len(most_take["pieces_jumped"])
        else:
            most_take = 0

        if most_take > opp_most_take:
            score += most_take
        else:
            score -= opp_most_take
    else:
        opp_most_take = 0

    # Discourage allowing moves that set up Double+ jumps for opponent
    if opp_most_take > 1:
        score -= opp_most_take
    elif opp_most_take == 0:
        score += 5

    if num_jumped > opp_most_take:
        score += num_jumped - opp_most_take

    return score


def score_all_moves(board, moves, player):
    """ Score every move in given list

    Loop through list and calculate score for every move

    :param dict board: Board moves are being made on

    :param list moves: List of moves to score

    :param int player: Player scoring moves for

    :returns List of moves with all moves scored

    """
    for move in moves:
        tmp_board = move_result(board, move, player)

        move["score"] = score_board(tmp_board, move, player)

    return moves


if __name__ == "__main__":
    # Read in game board
    game_board = read_board()

    # Get player
    player_num = int(input())

    # Get all available moves
    moves = get_available_moves(game_board, player_num)

    scored_moves = score_all_moves(game_board, moves, player_num)

    highest_score = max(scored_moves, key=lambda x: x["score"])

    # Print a random move
    print_move(highest_score, highest_score["score"])

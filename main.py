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
    """
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

    :param list board: Board to get piece at

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


def possible_jumps(board, player, piece):
    """
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
                        jump_locations.append(nxt)
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
    """
    """
    # Get cooresponding action
    action = ACTIONS[player][direction]

    # Calculate coordinates of the new score
    new_location = (piece[0] + action[0], piece[1] + action[1])

    # Start building move
    move = {
        "start": piece,
        "locations": []
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

            # Check for double/triple jumps
            possible = possible_jumps(board, player, other_side)

            while len(possible) != 0:
                # TODO: Will only make one move even if two possible
                next_move = possible[0]

                # Add to list
                move["locations"].append(next_move)

                # Look for more possible
                possible = possible_jumps(board, player, next_move)

            return move
        else:
            # Jump can not be made
            return None


def get_available_moves(board, player):
    """
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


if __name__ == "__main__":
    # Read in game board
    game_board = read_board()

    # Get player
    player_num = int(input())

    # Get all available moves
    moves = get_available_moves(game_board, player_num)

    # Print a random move
    print_move(moves[randint(0, len(moves) - 1)], "Random")

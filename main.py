BOARD_SIZE = 8

# Mapping player and direction to x, y change in board
ACTIONS = {
    1: {
        "Right": (1, 1),
        "Left": (-1, 1)
    },
    2: {
        "Right": (1, -1),
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
                board[tmp_row[j]].append((j, i))

    return board

def print_move(move, reason):
    """
    """
    # Print starting location and number of moves
    move_str = " ".join([str(x) for x in move["start"]]) + "\n"
    move_str += str(move["moves"]) + "\n"
    
    # Add landing locations
    for i in range(move["moves"]):
        move_str += " ".join([str(x) for x in move["locations"][i]])
        
        # Add new line on all but last location
        if i < move["moves"] - 1:
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
    if piece[0] < 0 or piece[1] < 0 or piece[0] >= BOARD_SIZE or piece[1] >= BOARD_SIZE:
        raise IndexError("IndexError: Piece out of bounds")

    # Default to empty space
    val = 0

    # Check if location contains a piece
    if piece in board[1]:
        val = 1
    elif piece in board[2]:
        val = 2

    return val


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
        "moves": 1,
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
        pass
    
    
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

    print(game_board, player_num)
    print(get_location(game_board, (4, 1)))
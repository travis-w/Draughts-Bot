BOARD_SIZE = 8


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

    val = 0

    if piece in board[1]:
        val = 1
    elif piece in board[2]:
        val = 2

    return val


if __name__ == "__main__":
    # Read in game board
    game_board = read_board()

    # Get player
    player_num = int(input())

    print(game_board, player_num)
    print(get_location(game_board, (4, 1)))


def read_board():
    """ Read in game board
    
    Read in the game board as a 2D list
    
    :returns list of board representation
    
    """
    board = []
    for i in range(8):
        board.append([int(x) for x in input().split()])
    return board
    
if __name__ == "__main__":
    # Read in game board
    game_board = read_board()
    
    # Get player
    player_num = int(input())
    
    print(game_board, player_num)
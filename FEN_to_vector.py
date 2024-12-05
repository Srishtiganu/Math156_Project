import numpy as np

# Dictionaries to convert pieces and letters to numbers
piece_to_num = {'p':0, 'P':1, 'r':2, 'R':3, 'n':4, 'N':5, 'b':6, 'B':7, 'q':8, 'Q':9, 'k':10, 'K':11}
alphabet = {'a':0, 'b':1, 'c':2, 'd':3, 'e':4, 'f':5, 'g':6, 'h':7}

# Convert a FEN representation of the board into a vector of numbers
def to_vector(FEN):
    # Split the FEN string into different parts to process separately
    parts = FEN.split()
    board = parts[0]
    board_vector = np.zeros((8,8,12))
    player = parts[1]
    player_vector = np.array([0])
    castling = parts[2]
    castling_vector = np.array([0,0,0,0])
    ep = parts[3]
    ep_vector = np.zeros((8,2))
    # This tracks how many moves until the 50 move rule forces a draw
    half_move_vector = np.array([int(parts[4])])
    i = 0
    j = 0
    
    # Loop through the board representation, setting values appropriately
    # if there is a piece at the corresponding square
    for char in board:
        if char.isalpha():
            board_vector[i][j][piece_to_num[char]] = 1
            i += 1
        if char.isnumeric():
            i += int(char)
        if char == '/':
            j += 1
            i = 0

    # Set a parameter based on whether white or black is to move
    if player == 'w':
        player_vector[0] = 0
    if player == 'b':
        player_vector[0] = 1

    # Set a castling rights vector
    if 'K' in castling:
        castling_vector[0] = 1
    if 'Q' in castling:
        castling_vector[1] = 1
    if 'k' in castling:
        castling_vector[2] = 1
    if 'q' in castling:
        castling_vector[3] = 1
    
    # Set a flag if en passant is legal and denote where
    if ep != '-':
        file = alphabet[ep[0]]
        row = int(int(ep[1]) / 3 - 1)
        ep_vector[file][row] = 1
    
    # Append all of the data vectors and return the result
    v1 = board_vector.flatten()
    v2 = player_vector
    v3 = castling_vector
    v4 = ep_vector.flatten()
    v5 = half_move_vector
    final_vector = np.concatenate([v1, v2, v3, v4, v5])
    return final_vector
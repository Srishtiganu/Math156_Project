import numpy as np

piece_to_num = {'p':0, 'P':1, 'r':2, 'R':3, 'n':4, 'N':5, 'b':6, 'B':7, 'q':8, 'Q':9, 'k':10, 'K':11}

alphabet = {'a':0, 'b':1, 'c':2, 'd':3, 'e':4, 'f':5, 'g':6, 'h':7}

def to_vector(FEN):
    parts = FEN.split()
    board = parts[0]
    board_vector = np.zeros((8,8,12))
    player = parts[1]
    player_vector = np.array([0])
    castling = parts[2]
    castling_vector = np.array([0,0,0,0])
    ep = parts[3]
    ep_vector = np.zeros((8,2))
    half_move_vector = np.array([int(parts[4])])
    i = 0
    j = 0
    for char in board:
        if char.isAlpha():
            board_vector[i][j][piece_to_num[char]] = 1
            i += 1
        if char.isNum():
            i += int(char)
        if char == '/':
            j += 1
            i = 0

    if player == 'w':
        player_vector[0] = 0
    if player == 'b':
        player_vector[0] = 1

    if 'K' in castling:
        castling_vector[0] = 1
    if 'Q' in castling:
        castling_vector[1] = 1
    if 'k' in castling:
        castling_vector[2] = 1
    if 'q' in castling:
        castling_vector[3] = 1
    
    if ep != '-':
        file = alphabet[ep[0]]
        row = int(ep[1]) / 3 - 1
        ep_vector[file][row] = 1
    
    final_vector = np.concatenate([board_vector.flatten(), player_vector, castling_vector, ep_vector, half_move_vector])
    return final_vector

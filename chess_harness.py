import random
import chess
import os

# Get a move from the user that indicates their move
# Moves are denoted by a source and destination square
# If the move is invalid it asks again. The player can also resign by typing "resign"
def get_move(board):
    legal_moves = board.legal_moves
    move = input("Enter move: ")
    if move == 'resign':
        return move
    try:
        cmove = chess.Move.from_uci(move)
        if cmove not in legal_moves:
            raise
        return cmove
    except:
        while True:
            print(board)
            move = input("Invalid move, try again: ")
            if move == 'resign':
                return move
            try:
                cmove = chess.Move.from_uci(move)
                if cmove not in legal_moves:
                    raise
                return cmove
            except:
                pass

# If the player did not resign, update the board with the move they input, otherwise resign
def process_player_move(board):
    player_move = get_move(board)
    try:
        board.push(player_move)
        print(board)
        return 0
    except:
        print(board)
        return 1

# Allow the network to make the best move according to its evaluation function
def process_computer_move(board, eval, player):
    best_eval = None
    best_move = None
    # Initialize the best move variable with the worst possible case
    if player == 'white':
        best_eval = float("inf")
    if player == 'black':
        best_eval = float("-inf")
    # Iterate through the legal moves, evaluate them, and keep track of the best one
    for move in board.legal_moves:
        board.push(move)
        value = eval_harness(board, eval)
        board.pop()
        if player == 'white':
            if value < best_eval:
                best_eval = value
                best_move = move
        if player == 'black':
            if value > best_eval:
                best_eval = value
                best_move = move
    # Make the best move
    board.push(best_move)
    print(board)

# Play a Chess game
def game(eval_function, player='select'):
    # Decide on whether the player will play as white or black
    while player not in ['white', 'black']:
        player = input("Enter whether you will play as white or black: ")
        if player in ['white', 'w', 'White', 'W']:
            player = 'white'
            break
        if player in ['black', 'b', "Black", 'B']:
            player = 'black'
            break
    # Initialize the board. If the player goes second, the computer makes the first move
    board = chess.Board()
    print(board)
    if player == 'black':
        process_computer_move(board, eval_function, player)
    # Process player and computer moves until the game ends
    while True:
        rc = process_player_move(board)
        # Detect resgination and respond accordingly
        if rc == 1:
            if player == 'black':
                print('1-0')
            if player == 'white':
                print('0-1')
            return
        # Process moves other than resgnation
        if board.outcome() is not None:
            print(board.result())
            return
        process_computer_move(board, eval_function, player)
        if board.outcome() is not None:
            print(board.result())
            return

# Return a random number as the board evaluation
def random_eval(board):
    return random.randint(-1000,1000)

# Evaluate positins where the game is over with their true values. Otherwise call the evaluation function
def eval_harness(board, eval=random_eval):
    if board.outcome() is not None:
        res = board.result()
        if res == '1-0':
            return float('inf')
        if res == '0-1':
            return float('-inf')
        if res == '1/2-1/2':
            return float(0)
    return eval(board.fen())

game(random_eval, player='select')
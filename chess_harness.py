import random
import chess
import os

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

def process_player_move(board):
    player_move = get_move(board)
    try:
        board.push(player_move)
        print(board)
        return 0
    except:
        print(board)
        return 1

def process_computer_move(board, eval, player):
    best_eval = None
    best_move = None
    if player == 'white':
        best_eval = float("inf")
    if player == 'black':
        best_eval = float("-inf")
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
    board.push(best_move)
    print(board)


def game(eval_function, player='select'):
    while True:
        player = input("Enter whether you will play as white or black: ")
        if player in ['white', 'w', 'White', 'W']:
            player = 'white'
            break
        if player in ['black', 'b', "Black", 'B']:
            player = 'black'
            break
    board = chess.Board()
    print(board)
    if player == 'black':
        process_computer_move(board, eval_function, player)
    while True:
        rc = process_player_move(board)
        if rc == 1:
            if player == 'black':
                print('1-0')
            if player == 'white':
                print('0-1')
            return
        if board.outcome() is not None:
            print(board.result())
            return
        process_computer_move(board, eval_function, player)
        if board.outcome() is not None:
            print(board.result())
            return

def random_eval(board):
    return random.randint(-1000,1000)

def eval_harness(board, eval=random_eval):
    if board.outcome() is not None:
        res = board.result()
        if res == '1-0':
            return float('inf')
        if res == '0-1':
            return float('-inf')
        if res == '1/2-1/2':
            return float(0)
    return eval(board)

game(random_eval, player='select')
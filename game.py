import math
import random

WIN_PATTERNS = [
    [0,1,2],[3,4,5],[6,7,8],
    [0,3,6],[1,4,7],[2,5,8],
    [0,4,8],[2,4,6]
]

def check_winner(board):
    for a, b, c in WIN_PATTERNS:
        if board[a] == board[b] == board[c] and board[a] != " ":
            return board[a], [a, b, c]
    return None, []

def is_full(board):
    return " " not in board

def minimax(board, is_maximizing, alpha, beta):
    winner, _ = check_winner(board)

    if winner == "O":
        return 1
    elif winner == "X":
        return -1
    elif is_full(board):
        return 0

    if is_maximizing:
        best_score = -math.inf
        for i in range(9):
            if board[i] == " ":
                board[i] = "O"
                score = minimax(board, False, alpha, beta)
                board[i] = " "
                best_score = max(best_score, score)
                alpha = max(alpha, best_score)
                if beta <= alpha:
                    break
        return best_score

    else:
        best_score = math.inf
        for i in range(9):
            if board[i] == " ":
                board[i] = "X"
                score = minimax(board, True, alpha, beta)
                board[i] = " "
                best_score = min(best_score, score)
                beta = min(beta, best_score)
                if beta <= alpha:
                    break
        return best_score

def get_best_move(board, mode="Unbeatable"):
    available = [i for i in range(9) if board[i] == " "]

    if mode == "Smart":
        if random.random() < 0.3:
            return random.choice(available)

    best_score = -math.inf
    best_move = None

    for i in range(9):
        if board[i] == " ":
            board[i] = "O"
            score = minimax(board, False, -math.inf, math.inf)
            board[i] = " "
            if score > best_score:
                best_score = score
                best_move = i

    return best_move
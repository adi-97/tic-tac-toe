from flask import Flask, render_template, request, jsonify
import random

app = Flask(__name__)

board = [""] * 9
difficulty = "medium"
computer_first = False

def check_winner(b):
    winning_combos = [
        (0, 1, 2), (3, 4, 5), (6, 7, 8),  # Rows
        (0, 3, 6), (1, 4, 7), (2, 5, 8),  # Columns
        (0, 4, 8), (2, 4, 6)              # Diagonals ← fixed this!
    ]
    for a, b1, c in winning_combos:
        if b[a] == b[b1] == b[c] and b[a] != "":
            return b[a]
    if all(cell != "" for cell in b):
        return "Draw"
    return None

def available_moves(b):
    return [i for i, cell in enumerate(b) if cell == ""]

def make_computer_move():
    global difficulty
    moves = available_moves(board)
    if not moves:
        return None

    if difficulty == "easy":
        return random.choice(moves)
    
    if difficulty == "medium":
        # Try to win
        for i in moves:
            copy = board[:]
            copy[i] = "O"
            if check_winner(copy) == "O":
                return i
        # Block opponent
        for i in moves:
            copy = board[:]
            copy[i] = "X"
            if check_winner(copy) == "X":
                return i
        # Otherwise random
        return random.choice(moves)

    if difficulty == "hard":
        best_score = -float('inf')
        best_move = None
        for i in moves:
            board[i] = "O"
            score = minimax(board, False)
            board[i] = ""
            if score > best_score:
                best_score = score
                best_move = i
        return best_move

def minimax(b, is_maximizing):
    winner = check_winner(b)
    if winner == "O":
        return 1
    elif winner == "X":
        return -1
    elif winner == "Draw":
        return 0

    if is_maximizing:
        best_score = -float('inf')
        for i in available_moves(b):
            b[i] = "O"
            score = minimax(b, False)
            b[i] = ""
            best_score = max(score, best_score)
        return best_score
    else:
        best_score = float('inf')
        for i in available_moves(b):
            b[i] = "X"
            score = minimax(b, True)
            b[i] = ""
            best_score = min(score, best_score)
        return best_score

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/move", methods=["POST"])
def move():
    global board
    data = request.get_json()
    pos = data["position"]

    if board[pos] == "":
        board[pos] = "X"
        winner = check_winner(board)
        if winner:
            return jsonify({'board': board, 'winner': winner})

        comp_move = make_computer_move()
        if comp_move is not None:
            board[comp_move] = "O"
        winner = check_winner(board)
        if winner:
            return jsonify({'board': board, 'winner': winner})

    return jsonify({'board': board})

@app.route("/reset", methods=["POST"])
def reset():
    global board, difficulty, computer_first
    data = request.get_json()
    computer_first = data.get("computer_first", False)
    difficulty = data.get("difficulty", "medium")
    
    board = [""] * 9
    if computer_first:
        comp_move = make_computer_move()
        if comp_move is not None:
            board[comp_move] = "O"
    
    return jsonify({'board': board})

if __name__ == "__main__":
    app.run(debug=True)

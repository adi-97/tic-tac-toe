from flask import Flask, render_template, request, jsonify
import random

app = Flask(__name__)

board = [""] * 9
difficulty = "medium"
game_over = False


def check_winner(b):
    winning_combos = [
        (0, 1, 2), (3, 4, 5), (6, 7, 8),
        (0, 3, 6), (1, 4, 7), (2, 5, 8),
        (0, 4, 8), (2, 4, 6)
    ]
    for combo in winning_combos:
        a, b1, c = combo
        if b[a] == b[b1] == b[c] and b[a] != "":
            return b[a], list(combo)
    if all(cell != "" for cell in b):
        return "Draw", []
    return None, []


def available_moves(b):
    return [i for i, cell in enumerate(b) if cell == ""]


def minimax(b, is_maximizing, depth=0, alpha=-float('inf'), beta=float('inf')):
    winner, _ = check_winner(b)
    if winner == "O":
        return 10 - depth   # prefer faster wins
    if winner == "X":
        return depth - 10   # prefer slower losses
    if winner == "Draw":
        return 0

    if is_maximizing:
        best = -float('inf')
        for i in available_moves(b):
            b[i] = "O"
            score = minimax(b, False, depth + 1, alpha, beta)
            b[i] = ""
            best = max(best, score)
            alpha = max(alpha, best)
            if beta <= alpha:
                break
        return best
    else:
        best = float('inf')
        for i in available_moves(b):
            b[i] = "X"
            score = minimax(b, True, depth + 1, alpha, beta)
            b[i] = ""
            best = min(best, score)
            beta = min(beta, best)
            if beta <= alpha:
                break
        return best


def make_computer_move():
    moves = available_moves(board)
    if not moves:
        return None

    if difficulty == "easy":
        return random.choice(moves)

    if difficulty == "medium":
        # Win if possible
        for i in moves:
            copy = board[:]
            copy[i] = "O"
            winner, _ = check_winner(copy)
            if winner == "O":
                return i
        # Block player win
        for i in moves:
            copy = board[:]
            copy[i] = "X"
            winner, _ = check_winner(copy)
            if winner == "X":
                return i
        # Prefer center, then corners, then edges
        for i in [4, 0, 2, 6, 8, 1, 3, 5, 7]:
            if i in moves:
                return i

    if difficulty == "hard":
        best_score = -float('inf')
        best_move = None
        alpha = -float('inf')
        for i in moves:
            board[i] = "O"
            score = minimax(board, False, 1, alpha, float('inf'))
            board[i] = ""
            if score > best_score:
                best_score = score
                best_move = i
            alpha = max(alpha, best_score)
        return best_move


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/move", methods=["POST"])
def move():
    global board, game_over
    data = request.get_json()
    pos = data["position"]

    if game_over or board[pos] != "":
        return jsonify({'board': board, 'error': 'Invalid move'})

    board[pos] = "X"
    winner, winning_cells = check_winner(board)
    if winner:
        game_over = True
        return jsonify({'board': board, 'winner': winner, 'winning_cells': winning_cells})

    comp_move = make_computer_move()
    if comp_move is not None:
        board[comp_move] = "O"
    winner, winning_cells = check_winner(board)
    if winner:
        game_over = True
        return jsonify({'board': board, 'winner': winner, 'winning_cells': winning_cells})

    return jsonify({'board': board})


@app.route("/reset", methods=["POST"])
def reset():
    global board, difficulty, game_over
    data = request.get_json()
    computer_first = data.get("computer_first", False)
    difficulty = data.get("difficulty", "medium")
    game_over = False
    board = [""] * 9

    if computer_first:
        comp_move = make_computer_move()
        if comp_move is not None:
            board[comp_move] = "O"

    return jsonify({'board': board})


if __name__ == "__main__":
    app.run(debug=True)

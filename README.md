# Tic Tac Toe — Web Game with AI

A polished, interactive Tic Tac Toe game built with HTML, CSS, JavaScript, and a Python Flask backend. Play against an AI opponent with three difficulty levels, including an unbeatable Hard mode powered by Minimax with Alpha-Beta Pruning.

---

## Features

- **3 difficulty levels** — Easy (random), Medium (strategic), Hard (unbeatable Minimax)
- **Choose who goes first** — you or the computer
- **Score tracker** — wins, losses, and draws persist across games in a session
- **Winning cell highlight** — the winning three cells pulse in gold when the game ends
- **Sound effects** — Web Audio API tones for moves, wins, losses, and draws (no external files)
- **Polished light-theme UI** — colour-coded cells (red for X, blue for O), smooth pop-in animations, and a dot-grid background
- **Game-over protection** — the board is fully locked after each game ends; no stray clicks accepted

---

## How It Works

| Difficulty | Strategy |
|------------|----------|
| Easy | Picks a random available cell |
| Medium | Wins immediately if possible → blocks the player → prefers center, corners, then edges |
| Hard | Full Minimax search with Alpha-Beta Pruning and depth-weighted scoring — always takes the fastest win and never loses |

---

## Getting Started

### Requirements

- Python 3.7+
- pip

### Install & Run

```bash
git clone https://github.com/adi-97/tic-tac-toe.git
cd tic-tac-toe
pip install -r requirements.txt
python app.py
```

Open your browser and go to: **http://127.0.0.1:5000**

> Do **not** open `index.html` directly in the browser — the game logic runs on the Flask server.

---

## Project Structure

```
tic-tac-toe/
├── app.py               # Flask backend — game logic, Minimax AI
├── requirements.txt     # Python dependencies
└── templates/
    └── index.html       # Frontend — UI, styles, and JavaScript
```

---

## Tech Stack

- **Backend** — Python, Flask
- **Frontend** — HTML5, CSS3, Vanilla JavaScript
- **AI** — Minimax algorithm with Alpha-Beta Pruning
- **Audio** — Web Audio API (fully self-contained, no CDN)

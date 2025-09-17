```markdown
# 🔴🟡 Connect Four AI

A smart Connect Four game built in Python featuring an AI player that uses the minimax algorithm with alpha-beta pruning. Perfect for testing your skills against an intelligent opponent or watching two AIs battle it out!

## 🎮 Game Modes

- **Human vs Human** (`four_game.py`) - Classic two-player mode
- **Human vs AI** (`connect4_ai1.py`) - Challenge the AI player  
- **AI vs AI** (`connect4_ai2.py`) - Watch two AIs compete

## 🧠 AI Features

- **Minimax Algorithm** with alpha-beta pruning for optimal move selection
- **6-ply search depth** - looks ahead 6 moves to plan strategy
- **Smart evaluation** - prioritizes center columns and recognizes winning patterns
- **Instant win/block detection** - never misses obvious winning moves or threats
- **Optimized performance** - alpha-beta pruning reduces search time significantly

## 🚀 Getting Started

### Prerequisites
```
pip install numpy pygame
```

### Running the Game
```
# Play against AI
python connect4_ai1.py

# Human vs Human
python four_game.py  

# Watch AI vs AI
python connect4_ai2.py
```

## 🎯 How It Works

The AI uses a **minimax algorithm** to evaluate all possible moves up to 6 turns ahead. It scores positions based on:

- Winning patterns (horizontal, vertical, diagonal)
- Center column control (more connection opportunities)  
- Blocking opponent threats
- Creating multiple winning opportunities

**Alpha-beta pruning** dramatically speeds up the search by eliminating clearly inferior move branches.

## 📁 Project Structure

- `aiplayer1.py` - Main AI implementation (sophisticated minimax)
- `aiplayer2.py` - Alternative AI approach  
- Game modes: `four_game.py`, `connect4_ai1.py`, `connect4_ai2.py`
- `aiplayerNotes.txt` - Detailed strategy documentation

## 🎓 Educational Value

Great for learning:
- Game theory and minimax algorithms
- Alpha-beta pruning optimization
- Python game development with Pygame
- AI evaluation functions and heuristics

---

Built as part of an Introduction to AI course. The AI is surprisingly challenging - good luck beating it! 🎯
```

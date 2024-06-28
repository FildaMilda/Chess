# Chess Interface Documentation

## Introduction
This Python program is a simple chess interface created using Pygame. It allows two players to play a game of chess starting from the standard initial position. Players alternate moves, with the program enforcing the correct turn order (white first, then black).

## Installation
Before running the program, ensure you have the required dependencies installed. You can install Pygame using pip:

```bash
pip install pygame
```

## Usage
To run the chess interface, execute the main script:

```bash
python src/main.py
```

The game window will open, displaying the chessboard with the starting position. 

## Controls
- **Mouse**: Click on a piece to select it. Click on the desired destination square to move the selected piece.
- The game enforces turn order, so players must move in the correct sequence (white moves first, then black).

## Features
- **Turn-Based Play**: The interface ensures that players alternate moves, starting with white.
- **Basic Piece Movement**: Players can click on a piece and move it to a valid square.
- **Graphical Interface**: The chessboard and pieces are rendered using Pygame, providing a visual representation of the game state.

## Code Structure
The program consists of several key components:

1. **Initialization**: The Pygame library is initialized, and the game window is set up.
2. **Game Loop**: The main loop of the program, which handles events, updates the game state, and redraws the board.
3. **Event Handling**: User inputs (mouse clicks) are processed to select and move pieces.
4. **Game Logic**: The rules for moving pieces and alternating turns are enforced.

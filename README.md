# Tetris Game

This is a simple Tetris game developed using Python and the Pygame library. The game features basic Tetris mechanics, including different tetromino shapes, collision detection, score tracking, and a simple interface.

## Features
- Tetromino shapes: I, O, T (more shapes can be added easily).
- Colorful tetrominoes.
- Collision detection with the game board.
- Score tracking with a visible score panel.
- Automatic line clearing when rows are filled.

## Prerequisites
To run this game, you need the following installed on your system:
- Python 3.x
- Pygame library

### Installing Pygame
You can install Pygame using pip:
```bash
pip install pygame
```

## How to Run the Game
1. Clone or download this repository to your local machine.
2. Open a terminal in the project directory.
3. Run the following command to start the game:
   ```bash
   python tetris.py
   ```

## Gameplay Instructions
- Use the **Left Arrow** key to move the tetromino left.
- Use the **Right Arrow** key to move the tetromino right.
- Use the **Down Arrow** key to move the tetromino down faster.
- The game automatically spawns a new tetromino when the current one locks into place.
- Rows are cleared when they are completely filled, and your score increases.

## Code Overview
### Main Components
1. **Game Initialization**: The game sets up the display, initializes variables, and starts the main game loop.
2. **Tetromino Management**: Tetrominoes are randomly generated, and their position and rotation are managed throughout the game.
3. **Collision Detection**: Ensures that tetrominoes do not overlap with each other or go out of bounds.
4. **Scoring and Line Clearing**: Tracks the player's score and clears rows when they are filled.
5. **Rendering**: Draws the game board, tetrominoes, and score panel.


## Customization
- **Adding New Shapes**: You can add more tetromino shapes by modifying the `SHAPES` list in the code.
- **Changing Colors**: Update the `COLORS` list to use your preferred colors.
- **Adjusting Game Speed**: Modify the `fall_speed` variable to increase or decrease the tetromino falling speed.

## Screenshots
https://github.com/user-attachments/assets/a6d67b19-8d4f-4ca9-a7ec-1f36e7ffabbe

## License
This project is licensed under the MIT License. Feel free to use and modify it as you like.

## Acknowledgments
- This game was developed as a learning project to explore Python and Pygame.
- Inspired by the classic Tetris game.

---

Enjoy playing Tetris!


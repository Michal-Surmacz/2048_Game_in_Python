# 2048_Game_in_Python
This program implements the logic game 2048 using the Pygame library. The player's goal is to merge tiles with the same values to achieve the value of 2048 on the game board.

## Libraries
- `pygame`: Library for creating games in Python.
- `random`: Module for generating pseudorandom numbers.
- `math`: Module containing mathematical functions.

## Constants and Settings
- `FPS = 60`: Frames per second.
- `WIDTH, HEIGHT = 800, 800`: Width and height of the game window.
- `ROWS = 4`, `COLS = 4`: Number of rows and columns in the grid.
- `RECT_HEIGHT`, `RECT_WIDTH`: Height and width of a single tile in the grid.
- `OUTLINE_COLOR`, `BACKGROUND_COLOR`, `FONT_COLOR`: Colors used in the game.
- `OUTLINE_THICKNESS`: Thickness of grid lines.
- `FONT`: Font object used for drawing text on tiles.
- `MOVE_VEL`: Speed of tile movement.

## Tile Class
- `value`: Value of the tile (2 or 4).
- `row`, `col`: Tile position in the grid.
- `x`, `y`: Pixel position of the tile on the screen.
- Methods: `get_color()`, `draw()`, `set_pos()`, `move()`.

## Helper Functions
- `draw_grid(window)`: Draws the grid on the game screen.
- `draw(window, tiles)`: Draws all tiles and the grid on the screen.
- `get_random_pos(tiles)`: Returns a random empty position on the grid.
- `update_tiles(window, tiles, sorted_tiles)`: Updates the tiles on the grid after a player move.

## Main Game Loop
- `main(window)`: Main function that starts the main game loop.
- Handles user events and updates the game screen in the main loop.

## Player Movement Handling
- `move_tiles(window, tiles, clock, direction)`: Handles player movements (left, right, up, down) on the grid.
- Utilizes lambda functions to handle tile movement in different directions.
- Checks for collisions, tile merging, and generates new tiles.

## Game Start
- `if __name__ == "__main__": main(WINDOW)`: Starts the main `main()` function when the program starts, initiating the game.

import pygame  # Import the pygame library for game development
import random  # Import the random module for random number generation
import math  # Import the math module for mathematical functions

pygame.init()  # Initialize pygame

FPS = 60  # Frames per second for the game

# Define the dimensions of the game window and grid
WIDTH, HEIGHT = 800, 800
ROWS = 4
COLS = 4

# Calculate the height and width of each grid cell
RECT_HEIGHT = HEIGHT // ROWS
RECT_WIDTH = WIDTH // COLS

# Define colors and other constants for UI
OUTLINE_COLOR = (187, 173, 160)
OUTLINE_THICKNESS = 10
BACKGROUND_COLOR = (205, 192, 180)
FONT_COLOR = (119, 110, 101)

# Define font settings for tile values
FONT = pygame.font.SysFont("comicsans", 60, bold=True)

# Velocity of tile movement
MOVE_VEL = 20

# Create the game window
WINDOW = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("2048")  # Set the window title

# Tile class to represent each tile in the game
class Tile:
    COLORS = [  # Colors corresponding to different tile values
        (237, 229, 218),
        (238, 225, 201),
        (243, 178, 122),
        (246, 150, 101),
        (247, 124, 95),
        (247, 95, 59),
        (237, 208, 115),
        (237, 204, 99),
        (236, 202, 80),
    ]

    def __init__(self, value, row, col):
        self.value = value  # Value of the tile (2, 4, 8, etc.)
        self.row = row  # Row index in the grid
        self.col = col  # Column index in the grid
        self.x = col * RECT_WIDTH  # X-coordinate of the tile on the window
        self.y = row * RECT_HEIGHT  # Y-coordinate of the tile on the window

    def get_color(self):
        # Get color based on the logarithm of the tile value
        color_index = int(math.log2(self.value)) - 1
        color = self.COLORS[color_index]
        return color

    def draw(self, window):
        color = self.get_color()  # Get color for the tile
        # Draw the tile rectangle on the window
        pygame.draw.rect(window, color, (self.x, self.y, RECT_WIDTH, RECT_HEIGHT))

        # Render the text for the tile value
        text = FONT.render(str(self.value), 1, FONT_COLOR)
        # Draw the text at the center of the tile rectangle
        window.blit(
            text,
            (
                self.x + (RECT_WIDTH / 2 - text.get_width() / 2),
                self.y + (RECT_HEIGHT / 2 - text.get_height() / 2),
            ),
        )

    def set_pos(self, ceil=False):
        # Update tile position based on its coordinates
        if ceil:
            self.row = math.ceil(self.y / RECT_HEIGHT)
            self.col = math.ceil(self.x / RECT_WIDTH)
        else:
            self.row = math.floor(self.y / RECT_HEIGHT)
            self.col = math.floor(self.x / RECT_WIDTH)

    def move(self, delta):
        # Move the tile by the specified delta (change in position)
        self.x += delta[0]
        self.y += delta[1]

# Function to draw grid lines on the window
def draw_grid(window):
    for row in range(1, ROWS):
        y = row * RECT_HEIGHT
        pygame.draw.line(window, OUTLINE_COLOR, (0, y), (WIDTH, y), OUTLINE_THICKNESS)

    for col in range(1, COLS):
        x = col * RECT_WIDTH
        pygame.draw.line(window, OUTLINE_COLOR, (x, 0), (x, HEIGHT), OUTLINE_THICKNESS)

    pygame.draw.rect(window, OUTLINE_COLOR, (0, 0, WIDTH, HEIGHT), OUTLINE_THICKNESS)

# Function to draw tiles and grid on the window
def draw(window, tiles):
    window.fill(BACKGROUND_COLOR)  # Fill the window with background color

    # Draw each tile on the window
    for tile in tiles.values():
        tile.draw(window)

    draw_grid(window)  # Draw grid lines on the window

    pygame.display.update()  # Update the display

# Function to get a random position for a new tile
def get_random_pos(tiles):
    row = None
    col = None
    while True:
        row = random.randrange(0, ROWS)
        col = random.randrange(0, COLS)

        if f"{row}{col}" not in tiles:
            break

    return row, col

# Function to move tiles based on user input
def move_tiles(window, tiles, clock, direction):
    updated = True  # Flag to check if any tile has been moved
    blocks = set()  # Set to keep track of merged tiles

    # Functions and variables based on the direction of movement
    if direction == "left":
        def sort_func(x): return x.col
        reverse = False
        delta = (-MOVE_VEL, 0)
        def boundary_check(tile): return tile.col == 0
        def get_next_tile(tile): return tiles.get(f"{tile.row}{tile.col - 1}")
        def merge_check(tile, next_tile): return tile.x > next_tile.x + MOVE_VEL
        move_check = lambda tile, next_tile: tile.x > next_tile.x + RECT_WIDTH + MOVE_VEL
        ceil = True
        
    # Similar functions and variables for other directions (right, up, down)
    elif direction == "right":
        def sort_func(x): return x.col
        reverse = True
        delta = (MOVE_VEL, 0)
        def boundary_check(tile): return tile.col == COLS - 1
        def get_next_tile(tile): return tiles.get(f"{tile.row}{tile.col + 1}")
        def merge_check(
            tile, next_tile): return tile.x < next_tile.x - MOVE_VEL
        move_check = (
            lambda tile, next_tile: tile.x + RECT_WIDTH + MOVE_VEL < next_tile.x
        )
        ceil = False
    elif direction == "up":
        def sort_func(x): return x.row
        reverse = False
        delta = (0, -MOVE_VEL)
        def boundary_check(tile): return tile.row == 0
        def get_next_tile(tile): return tiles.get(f"{tile.row - 1}{tile.col}")
        def merge_check(
            tile, next_tile): return tile.y > next_tile.y + MOVE_VEL
        move_check = (
            lambda tile, next_tile: tile.y > next_tile.y + RECT_HEIGHT + MOVE_VEL
        )
        ceil = True
    elif direction == "down":
        def sort_func(x): return x.row
        reverse = True
        delta = (0, MOVE_VEL)
        def boundary_check(tile): return tile.row == ROWS - 1
        def get_next_tile(tile): return tiles.get(f"{tile.row + 1}{tile.col}")
        def merge_check(
            tile, next_tile): return tile.y < next_tile.y - MOVE_VEL
        move_check = (
            lambda tile, next_tile: tile.y + RECT_HEIGHT + MOVE_VEL < next_tile.y
        )
        ceil = False

    while updated:  # Loop until no more tiles can be moved
        clock.tick(FPS)  # Control game speed
        updated = False  # Reset update flag
        sorted_tiles = sorted(tiles.values(), key=sort_func, reverse=reverse)  # Sort tiles

        for i, tile in enumerate(sorted_tiles):  # Iterate through sorted tiles
            if boundary_check(tile):  # Check if tile is at grid boundary
                continue  # Skip this tile

            next_tile = get_next_tile(tile)  # Get next tile in the movement direction
            if not next_tile:  # If no tile is present in the direction
                tile.move(delta)  # Move the tile
            # Handle merging of tiles with the same value
            elif tile.value == next_tile.value and tile not in blocks and next_tile not in blocks:
                if merge_check(tile, next_tile):  # Check merge condition
                    tile.move(delta)  # Move the tile
                else:
                    next_tile.value *= 2  # Merge tiles by doubling the value
                    sorted_tiles.pop(i)  # Remove merged tile from list
                    blocks.add(next_tile)  # Add merged tile to set
            # Handle movement without merging
            elif move_check(tile, next_tile):
                tile.move(delta)  # Move the tile
            else:
                continue  # Move to the next tile

            tile.set_pos(ceil)  # Update tile position
            updated = True  # Set update flag

        update_tiles(window, tiles, sorted_tiles)  # Update tiles on the window

    return end_move(tiles)  # Check if the game has ended

# Function to check if the game has ended and add a new tile if possible
def end_move(tiles):
    if len(tiles) == 16:  # Check if grid is full
        return "lost"  # Game over (grid full)

    row, col = get_random_pos(tiles)  # Get random position for new tile
    tiles[f"{row}{col}"] = Tile(random.choice([2, 4]), row, col)  # Create new tile
    return "continue"  # Continue the game

# Function to update tile positions on the window
def update_tiles(window, tiles, sorted_tiles):
    tiles.clear()  # Clear current tiles
    for tile in sorted_tiles:
        tiles[f"{tile.row}{tile.col}"] = tile  # Update tile positions in dictionary

    draw(window, tiles)  # Redraw window with updated tiles

# Function to generate initial tiles for the game
def generate_tiles():
    tiles = {}
    for _ in range(2):  # Generate two initial tiles
        row, col = get_random_pos(tiles)  # Get random positions
        tiles[f"{row}{col}"] = Tile(2, row, col)  # Create new tile with value 2

    return tiles  # Return the initial tiles dictionary

# Main game function
def main(window):
    clock = pygame.time.Clock()  # Create a clock object to control game speed
    run = True  # Flag to control the main game loop

    tiles = generate_tiles()  # Generate initial tiles for the game

    while run:  # Main game loop
        clock.tick(FPS)  # Limit the game speed

        for event in pygame.event.get():  # Check for events (e.g., key presses, quit)
            if event.type == pygame.QUIT:  # If user closes the window
                run = False  # Exit the game loop and end the game
                break

            if event.type == pygame.KEYDOWN:  # If a key is pressed
                # Move tiles based on arrow key inputs
                if event.key == pygame.K_LEFT:
                    move_tiles(window, tiles, clock, "left")
                if event.key == pygame.K_RIGHT:
                    move_tiles(window, tiles, clock, "right")
                if event.key == pygame.K_UP:
                    move_tiles(window, tiles, clock, "up")
                if event.key == pygame.K_DOWN:
                    move_tiles(window, tiles, clock, "down")

        draw(window, tiles)  # Draw the game window with updated tiles

    pygame.quit()  # Quit Pygame when the game loop exits

# Entry point of the script
if __name__ == "__main__":
    main(WINDOW)  # Start the main game loop with the game window

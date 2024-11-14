# --- Colors ---
WHITE = (255, 255, 255)          # White
BLACK = (0, 0, 0)                # Black
RED = (255, 0, 0)                # Red
GREEN = (0, 255, 0)              # Green
BLUE = (0, 0, 255)               # Blue
YELLOW = (255, 255, 0)           # Yellow
ORANGE = (255, 165, 0)           # Orange
PURPLE = (128, 0, 128)           # Purple
PINK = (255, 192, 203)           # Pink
BROWN = (139, 69, 19)            # Brown
GRAY = (128, 128, 128)           # Gray
DARK_GRAY = (64, 64, 64)         # Dark Gray
LIGHT_GRAY = (192, 192, 192)     # Light Gray
GOLD = (255, 215, 0)             # Gold

# Specific game colors assigned to game elements
COLOR_EMPTY_CELL = WHITE
COLOR_INDESTRUCTIBLE_BLOCK = GRAY
COLOR_BREAKABLE_BRICK = BROWN
COLOR_PLAYER1 = GREEN
COLOR_PLAYER2 = BLUE
COLOR_ENEMY = RED
COLOR_BACKGROUND = WHITE
COLOR_BOMB = YELLOW


# --- Menu highlight ---
MENU_SELECTED = BLUE


# --- Game Board Configuration ---
CELL_SIZE = 45  # Size of each cell on the game board
WINDOW_SIZE = CELL_SIZE * 13  # Window size based on the cell size and board dimensions


# --- Initial Positions ---
INITIAL_ENEMY_POSITIONS = [(4, 5), (5, 6), (9, 8), (3, 10)]  # Starting positions for enemies
STARTING_PLAYER1_POSITION = (0, 0)  # Starting position for player 1
STARTING_PLAYER2_POSITION = (12, 12)  # Starting position for player 2


# --- Game Timing ---
MAX_GAME_TIME = 600  # Maximum game duration in seconds

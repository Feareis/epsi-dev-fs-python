import pygame
import random

# Import custom modules for game functionalities
import game_settings as gs


def generate_simple_board(board_height, board_width, bricks_position):
    """
    Creates a game board with empty cells, indestructible walls, and breakable bricks.

    :param board_height: The number of rows on the board.
    :param board_width: The number of columns on the board.
    :param bricks_position: A list of (x, y) tuples representing the positions of breakable bricks.
    :return: A 2D list representing the game board.
    """
    # Initialize the board as an empty list to store rows
    plate = []

    # Create the board layout with empty cells and indestructible walls in a checkerboard pattern
    for i in range(board_height):
        if i % 2 == 0:
            # Row with only empty cells (" ")
            row = [" " for _ in range(board_width)]
        else:
            # Row with indestructible walls ("X") on odd columns
            row = ["X" if j % 2 != 0 else " " for j in range(board_width)]
        plate.append(row)

    # Place breakable bricks at specified positions
    for (x, y) in bricks_position:
        # Check that the brick position is within the board boundaries
        if 0 <= x < board_height and 0 <= y < board_width:
            plate[x][y] = "B"  # "B" represents a breakable brick

    return plate


def clear_area(x, y, board_height, board_width, board):
    """
    Clears an area around a given position (x, y) on the game board, ensuring it is empty.

    :param board:
    :param board_width:
    :param board_height:
    :param x: The row index of the position to clear around.
    :param y: The column index of the position to clear around.
    :return: None
    """
    if 0 <= x < board_height and 0 <= y < board_width:
        board[x][y] = " "  # Clear the main position
    # Clear adjacent cells, with boundary checks
    if 0 <= x < board_height and y + 1 < board_width:
        board[x][y + 1] = " "  # Clear the cell to the right
    if x + 1 < board_height and 0 <= y < board_width:
        board[x + 1][y] = " "  # Clear the cell below
    if x + 1 < board_height and y + 1 < board_width:
        board[x + 1][y + 1] = " "  # Clear the cell diagonally down-right


def generate_random_board(board_height, board_width, wall_ratio=None, brick_ratio=None):
    """
    Creates a randomized game board with empty cells, indestructible walls, and breakable bricks.
    Ensures empty zones around the starting positions of players and enemies.

    :param board_height: The number of rows on the board.
    :param board_width: The number of columns on the board.
    :param wall_ratio: The ratio of indestructible walls ("X") on the board (default: random value 0-0.2).
    :param brick_ratio: The ratio of breakable bricks ("B") on the board (default: random value 0-0.4).
    :return: A 2D list representing the game board where:
             - " " represents an empty cell,
             - "X" represents an indestructible wall,
             - "B" represents a breakable brick.
    """
    # Set default ratios for indestructible and destructible blocks if not provided
    wall_ratio = wall_ratio or random.uniform(0, 0.2)
    brick_ratio = brick_ratio or random.uniform(0, 0.4)

    # Initialize the board
    board = []
    for i in range(board_height):
        row = []
        for j in range(board_width):
            random_value = random.random()
            if random_value < wall_ratio:
                row.append("X")  # Indestructible wall
            elif random_value < wall_ratio + brick_ratio:
                row.append("B")  # Breakable brick
            else:
                row.append(" ")  # Empty cell
        board.append(row)

    # Clear areas for player and enemy starting positions
    clear_area(*gs.STARTING_PLAYER1_POSITION, board_height, board_width, board)
    if hasattr(gs, 'STARTING_PLAYER2_POSITION'):
        clear_area(*gs.STARTING_PLAYER2_POSITION, board_height, board_width, board)
    for foe in gs.INITIAL_ENEMY_POSITIONS:
        clear_area(*foe, board_height, board_width, board)

    return board


def view_board(screen, board, enemy_positions, player1_position, player2_position=None, is_player1_alive=True, is_player2_alive=True):
    """
    Renders a game board on the screen, displaying players, enemies, indestructible walls,
    breakable bricks, and empty cells. Supports both single-player and two-player modes.

    :param screen: The Pygame display surface where the board will be drawn.
    :param board: A 2D list representing the game board, where each cell may contain:
                  - "X" for indestructible walls,
                  - "B" for breakable bricks,
                  - " " for empty spaces.
    :param player1_position: A tuple (row, col) representing the current position of player 1.
    :param enemy_positions: A list of (row, col) tuples indicating the positions of enemies on the board.
    :param player2_position: (Optional) A tuple (row, col) for the position of player 2, if in two-player mode.
    :param is_player1_alive: Boolean indicating if player 1 is active (only affects rendering in two-player mode).
    :param is_player2_alive: Boolean indicating if player 2 is active (only affects rendering in two-player mode).
    :return: None
    """
    # Define colors for each cell type
    colors = {
        "X": gs.COLOR_INDESTRUCTIBLE_BLOCK,
        "B": gs.COLOR_BREAKABLE_BRICK,
        " ": gs.COLOR_EMPTY_CELL
    }

    for i, row in enumerate(board):
        for j, case in enumerate(row):
            # Define the rectangle for the current cell
            rect = j * gs.CELL_SIZE, i * gs.CELL_SIZE, gs.CELL_SIZE, gs.CELL_SIZE

            # Determine the color based on the cell's content and entity presence
            if is_player1_alive and (i, j) == player1_position:
                color = gs.COLOR_PLAYER1
            elif player2_position and is_player2_alive and (i, j) == player2_position:
                color = gs.COLOR_PLAYER2
            elif (i, j) in enemy_positions:
                color = gs.COLOR_ENEMY
            else:
                color = colors.get(case, gs.COLOR_EMPTY_CELL)  # Default to empty cell color if case is unrecognized

            # Draw the rectangle with the determined color
            pygame.draw.rect(screen, color, rect)

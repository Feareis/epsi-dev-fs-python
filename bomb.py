import time
import game_settings as gs
import pygame

# Stores active bombs with their position and timestamp of when they were placed
bombs = []

def add_bomb(position):
    """
    Adds a bomb to the active bombs list, recording its position and placement time.

    This function logs the bomb's position on the board and the time at which it was placed,
    allowing future handling of its explosion timing.

    :param position: Tuple (x, y) indicating the bomb’s deposit position, typically the player’s current position.
    :return: None
    """
    bombs.append({"position": position, "time": time.time()})


def update_bombs(screen, board, enemy_positions, player_position, board_height, board_width):
    """
    Updates the status and display of bombs, handling their explosions when ready.

    Bombs ready to explode affect the game board by damaging adjacent areas and checking
    for player impact. Displays all active bombs on the screen.

    :param screen: Pygame surface for drawing bombs.
    :param board: The current state of the game board.
    :param enemy_positions: List of enemy positions on the board.
    :param player_position: Current player position on the board.
    :param board_height: Total number of lines on the game board.
    :param board_width: Total number of columns on the game board.
    :return: Boolean - True if the player is hit by an explosion, False otherwise.
    """
    current_time = time.time()
    to_explode = [bomb for bomb in bombs if current_time - bomb["time"] >= 2]

    player_hit = False  # Tracks if player is hit by an explosion
    for bomb in to_explode:
        if explode_bomb(bomb["position"], board, enemy_positions, player_position, board_height, board_width):
            player_hit = True
        bombs.remove(bomb)  # Remove bomb after it has exploded

    for bomb in bombs:  # Draws all active bombs on the screen
        x, y = bomb["position"]
        rect = (y * gs.TAILLE_CASE, x * gs.TAILLE_CASE, gs.TAILLE_CASE, gs.TAILLE_CASE)
        pygame.draw.rect(screen, gs.COULEUR_BOMB, rect)
    return player_hit


def explode_bomb(position, board, enemy_positions, player_position, board_height, board_width):
    """
    Handles the explosion effect of a bomb, affecting surrounding elements on the game board.

    :param position: Position of the bomb.
    :param board: Current game board.
    :param enemy_positions: List of enemy positions.
    :param player_position: Position of the player.
    :param board_height: Number of rows on the game board.
    :param board_width: Number of columns on the game board.
    :return: True if the player is hit by the explosion, False otherwise.
    """
    x, y = position
    explosion_area = [
        (x, y),
        (x + 1, y), (x + 2, y),
        (x - 1, y), (x - 2, y),
        (x, y + 1), (x, y + 2),
        (x, y - 1), (x, y - 2)
    ]

    player_hit = False
    for ex, ey in explosion_area:
        if not 0 <= ex < board_height and 0 <= ey < board_width:  # Ensures explosion is within board limits
            continue
        if (ex, ey) == player_position:  # Checks if player is hit
            player_hit = True
        if board[ex][ey] == "B":  # Destroys destructible walls
            board[ex][ey] = " "
        elif (ex, ey) in enemy_positions:  # Removes enemies in the blast radius
            enemy_positions.remove((ex, ey))

    return player_hit

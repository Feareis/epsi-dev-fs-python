import random
import math


# Dictionary mapping player moves to grid changes
moves = {
    "player1": {
        # Player 1: Up -> z | Down -> s | Left -> q | Right -> d
        "z": (-1, 0),
        "s": (1, 0),
        "q": (0, -1),
        "d": (0, 1),
    },
    "player2": {
        # Player 2: Up -> o | Down -> l | Left -> k | Right -> m
        "o": (-1, 0),
        "l": (1, 0),
        "k": (0, -1),
        "m": (0, 1),
    }
}

def move_player(player_position, direction, board, player_number=1, player2_position=None):
    """
    Moves a player based on the specified direction and player number, ensuring they stay within bounds
    and avoid obstacles and other players.

    :param player_position: Current position of the player as a tuple (x, y).
    :param direction: The movement direction key (str) corresponding to the player's controls.
    :param board: 2D list representing the game board.
    :param player_number: Specifies which player is moving (1 for player 1, 2 for player 2).
    :param player2_position: Position of the other player as a tuple (x, y), to avoid collision.
    :return: New position of the player as a tuple (nx, ny).
    """
    x, y = player_position

    # Determine the key to select the correct player's moves
    player_key = "player1" if player_number == 1 else "player2"

    # Check if the direction is valid for the selected player
    if direction in moves[player_key]:
        dx, dy = moves[player_key][direction]
        nx, ny = x + dx, y + dy

        # Ensure the new position is within bounds, is empty, and does not overlap with player 2
        if 0 <= nx < len(board) and 0 <= ny < len(board[0]) and board[nx][ny] == " " and (nx, ny) != player2_position:
            return nx, ny  # Return the new valid position

    # Return the current position if movement is not possible
    return x, y


def check_player_collision(player_position, enemy_positions):
    """
    Checks if the player has collided with any enemies.

    :param player_position: Tuple (x, y) representing the current position of the player.
    :param enemy_positions: List of tuples [(x1, y1), (x2, y2), ...] representing the positions of all enemies.
    :return: True if the player position matches any enemy position, False otherwise.
    """
    return player_position in enemy_positions


def check_player_collision_2p(player1_position, player2_position, enemy_positions, is_player1_alive, is_player2_alive):
    """
    Checks for collisions between each player and enemies, updating the player's status if a collision is detected.

    :param player1_position: Tuple (x, y) representing the current position of player 1.
    :param player2_position: Tuple (x, y) representing the current position of player 2.
    :param enemy_positions: List of tuples [(x1, y1), (x2, y2), ...] representing the positions of all enemies.
    :param is_player1_alive: Boolean indicating if player 1 is currently alive.
    :param is_player2_alive: Boolean indicating if player 2 is currently alive.
    :return: Updated status of player1_live and player2_live as a tuple (player1_live, player2_live).
    """
    # Check collisions for player 1
    if is_player1_alive and player1_position in enemy_positions:
        is_player1_alive = False
        print("Player 1 eliminated !")

    # Check collisions for player 2
    if is_player2_alive and player2_position in enemy_positions:
        is_player2_alive = False
        print("Player 2 eliminated !")

    return is_player1_alive, is_player2_alive


def check_game_end(is_player1_alive, is_player2_alive):
    """
    Checks if the game has ended by verifying if both players are no longer alive.

    :param is_player1_alive: Boolean indicating if player 1 is still alive.
    :param is_player2_alive: Boolean indicating if player 2 is still alive.
    :return: True if both players are no longer alive (game over), False otherwise.
    """
    return not is_player1_alive and not is_player2_alive


def move_foe(player_position, enemy_positions, board):
    """
    Moves an enemy towards the player if within a certain range; otherwise, moves randomly.

    :param player_position: Tuple (x, y) representing the player's position.
    :param enemy_positions: Tuple (x, y) representing the current position of the enemy.
    :param board: 2D list representing the game board where " " is an empty cell.
    :return: New position of the enemy as a tuple (nx, ny).
    """
    px, py = player_position
    fx, fy = enemy_positions

    # Check if player is within a 4-cell distance to trigger direct movement towards player
    if euclidean_distance(player_position, enemy_positions) <= 4:
        directions = []

        # Decide movement direction horizontally and vertically towards the player
        if px > fx:
            directions.append((1, 0))  # Move down
        elif px < fx:
            directions.append((-1, 0))  # Move up

        if py > fy:
            directions.append((0, 1))  # Move right
        elif py < fy:
            directions.append((0, -1))  # Move left

        # Randomize directions for unpredictable movement
        random.shuffle(directions)

        # Attempt to move in one of the chosen directions
        for dx, dy in directions:
            nx, ny = fx + dx, fy + dy
            # Check for bounds and ensure target cell is empty
            if 0 <= nx < len(board) and 0 <= ny < len(board[0]) and board[nx][ny] == " ":
                return nx, ny

    # Random movement if not close to player or if direct movement is blocked
    directions = list(moves["player1"].values())
    random.shuffle(directions)
    for dx, dy in directions:
        nx, ny = fx + dx, fy + dy
        # Check for bounds and ensure target cell is empty
        if 0 <= nx < len(board) and 0 <= ny < len(board[0]) and board[nx][ny] == " ":
            return nx, ny

    # Return current position if movement is impossible
    return enemy_positions


def update_foes_positions(player_position, foes, board):
    """
    Updates the positions of all enemies on the board, moving them towards the player if possible
    and avoiding overlapping positions with other enemies.

    :param player_position: Tuple (x, y) representing the player's position.
    :param foes: List of tuples [(x1, y1), (x2, y2), ...] representing the current positions of all enemies.
    :param board: 2D list representing the game board where " " is an empty cell.
    :return: Updated list of enemy positions after attempting to move them.
    """
    foes_positions = []
    busy_position = set(foes)  # Track occupied positions to avoid duplicates

    for foe_position in foes:
        # Get the new position for the current enemy based on the player's position
        new_enemy_position = move_foe(player_position, foe_position, board)

        # Check if the new position is already occupied by another enemy
        if new_enemy_position in busy_position:
            foes_positions.append(foe_position)  # Keep the enemy in the current position
        else:
            foes_positions.append(new_enemy_position)  # Update to the new position
            busy_position.add(new_enemy_position)  # Mark the new position as occupied

    return foes_positions


def move_foe_2p(player1_position, player2_position, enemy_positions, board, is_player1_alive, is_player2_alive):
    """
    Determines the next position for an enemy on the board, targeting the closest active player
    if within a certain range, or moving randomly otherwise.

    :param player1_position: Tuple (x, y) for player 1's position.
    :param player2_position: Tuple (x, y) for player 2's position.
    :param enemy_positions: Tuple (x, y) for the current position of the foe.
    :param board: 2D list representing the game board.
    :param is_player1_alive: Boolean indicating if player 1 is active.
    :param is_player2_alive: Boolean indicating if player 2 is active.
    :return: New position for the foe as a tuple (x, y).
    """
    # Determine the target player based on proximity and alive status
    if is_player1_alive and is_player2_alive:
        distance_p1_enemy = euclidean_distance(player1_position, enemy_positions)
        distance_p2_enemy = euclidean_distance(player2_position, enemy_positions)
        target_position = player1_position if distance_p1_enemy <= distance_p2_enemy else player2_position
    elif is_player1_alive:
        target_position = player1_position
    elif is_player2_alive:
        target_position = player2_position
    else:
        return enemy_positions  # No active players, foe remains in place

    # Move towards target player if within a certain range
    if euclidean_distance(target_position, enemy_positions) <= 4:
        px, py = target_position
        fx, fy = enemy_positions
        directions = []

        # Determine movement direction based on target position
        if px > fx:
            directions.append((1, 0))  # move down
        elif px < fx:
            directions.append((-1, 0))  # move up
        if py > fy:
            directions.append((0, 1))  # move right
        elif py < fy:
            directions.append((0, -1))  # move left

        # Shuffle to add randomness in case multiple directions are possible
        random.shuffle(directions)

        # Attempt to move towards the target position
        for dx, dy in directions:
            nx, ny = fx + dx, fy + dy
            # Check for bounds and ensure target cell is empty
            if 0 <= nx < len(board) and 0 <= ny < len(board[0]) and board[nx][ny] == " ":
                return nx, ny

    # If target is not close enough, move randomly
    directions = list(moves["player1"].values())
    random.shuffle(directions)
    for dx, dy in directions:
        nx, ny = enemy_positions[0] + dx, enemy_positions[1] + dy
        # Check for bounds and ensure target cell is empty
        if 0 <= nx < len(board) and 0 <= ny < len(board[0]) and board[nx][ny] == " ":
            return nx, ny

    # No valid move found, stay in the same position
    return enemy_positions


def update_foes_positions_2p(player1_position, player2_position, enemy_positions, board, is_player1_alive, is_player2_alive):
    """
    Updates the positions of all enemies on the board, ensuring no overlapping positions.

    :param player1_position: Tuple (x, y) for player 1's position.
    :param player2_position: Tuple (x, y) for player 2's position.
    :param enemy_positions: List of tuples representing the current positions of all enemies.
    :param board: 2D list representing the game board.
    :param is_player1_alive: Boolean indicating if player 1 is alive.
    :param is_player2_alive: Boolean indicating if player 2 is alive.
    :return: Updated list of enemy positions.
    """
    updated_enemy_positions = []
    occupied_enemy_positions = set(enemy_positions)  # Set to keep track of occupied positions

    for foe_position in enemy_positions:
        # Get new position for each enemy
        nw_foe_position = move_foe_2p(player1_position, player2_position, foe_position, board, is_player1_alive, is_player2_alive)

        # Check if the new position is occupied, if so, keep the enemy at the original position
        if nw_foe_position in occupied_enemy_positions:
            updated_enemy_positions.append(foe_position)
        else:
            updated_enemy_positions.append(nw_foe_position)  # Update to the new position
            occupied_enemy_positions.add(nw_foe_position)  # Mark new position as occupied

    return updated_enemy_positions


def euclidean_distance(position1, position2):
    """
    Calculates the Euclidean distance between two positions.

    :param position1: Tuple (x1, y1) representing the first position.
    :param position2: Tuple (x2, y2) representing the second position.
    :return: Euclidean distance as a float.
    """
    x1, y1 = position1
    x2, y2 = position2
    return math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)

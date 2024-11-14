import sqlite3
import os
import json

# Create the db directory if it doesn't exist
if not os.path.exists("db"):
    os.makedirs("db")

# Define paths for database files within the "db" directory
SCORE_DB_PATH = os.path.join("db", "scores.db")
GAME_DB_PATH = os.path.join("db", "game.db")

def initialize_scores_db():
    """
    Initializes the scores database by creating the 'high_scores' table if it does not exist.

    :return: The table stores player IDs, names, and their respective scores.
    """
    with sqlite3.connect(SCORE_DB_PATH) as conn:
        try:
            cursor = conn.cursor()
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS high_scores (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    player_name TEXT NOT NULL,
                    score INTEGER NOT NULL
                )
            ''')
            conn.commit()  # Commit the changes to create the table if it doesn't exist
        except sqlite3.Error as e:
            print(f"An error occurred: {e}")


def save_player_score(player_name, score):
    """
    Saves a player's score in the high_scores table.

    :param player_name: The name of the player.
    :param score: The score to be saved.
    :return: None
    """
    with sqlite3.connect(SCORE_DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute('''
                INSERT INTO high_scores (player_name, score) VALUES (?, ?)
            ''', (player_name, score))

        conn.commit()  # Commit the changes to create the table if it doesn't exist


def end_game_and_save_score(score):
    """
    Ends the game by prompting the player for their name and saving their score.

    :param score: The final score of the player.
    :return: None
    """
    player_name = input("Entrez votre nom : ")
    if not player_name.strip():
        player_name = "Joueur Inconnu"  # Assign a default name if input is empty
    save_player_score(player_name, score)


def get_top_player_scores(limit=5):
    """
    Retrieves the top scores from the high_scores table, ordered by score in descending order.

    :param limit: The maximum number of top scores to retrieve (default is 5).
    :return: A list of tuples containing player names and their scores.
    """
    with sqlite3.connect(SCORE_DB_PATH) as conn:
        cursor = conn.cursor()

        # Retrieve top scores ordered by descending score, limited by the specified limit
        cursor.execute('''
            SELECT player_name, score
            FROM high_scores
            ORDER BY score DESC
            LIMIT ?
        ''', (limit,))

        scores = cursor.fetchall()  # Fetch all results as a list of tuples
    return scores


def initialize_game_db():
    """
    Initializes the game database by creating the 'game_save' table if it does not exist.
    This table stores essential game data for saving and restoring game states.

    :return: None
    """
    with sqlite3.connect(GAME_DB_PATH) as conn:
        cursor = conn.cursor()

        # Create 'game_save' table with columns for player position, enemies, score, grid size, and game state
        cursor.execute('''
                CREATE TABLE IF NOT EXISTS game_save (
                    id INTEGER PRIMARY KEY, 
                    player_position TEXT, 
                    foes_positions TEXT, 
                    score INTEGER, 
                    nb_line INTEGER, 
                    nb_column INTEGER, 
                    game_plate TEXT
                )
            ''')

        conn.commit()  # Commit the changes to create the table if it doesn't exist


def save_single_game_state(player_position, enemy_positions, score, board_height, board_width, board):
    """
    Saves the current game state by storing player position, foes positions, score, grid size, and game plate.
    Deletes any previous save to maintain a single saved game state.

    :param player_position: The position of the player in the game.
    :param enemy_positions: The positions of foes (enemies) in the game.
    :param score: The current score of the player.
    :param board_height: The number of lines in the game grid.
    :param board_width: The number of columns in the game grid.
    :param board: The state of the game grid.
    :return: None
    """
    with sqlite3.connect(GAME_DB_PATH) as conn:
        try:
            cursor = conn.cursor()

            # Delete any existing save to ensure only one game save exists
            cursor.execute('DELETE FROM game_save')

            # Insert the current game state into the game_save table
            cursor.execute('''
                INSERT INTO game_save (id, player_position, enemy_positions, score, board_height, board_width, board) 
                VALUES (?, ?, ?, ?, ?, ?, ?)
            ''', (
                1,  # ID is set to 1 for the single game save slot
                str(player_position),
                str(enemy_positions),
                score,
                board_height,
                board_width,
                str(board)
            ))

            conn.commit()  # Commit the changes to save the current game state
        except sqlite3.Error as e:
            print(f"An error occurred while saving the game state: {e}")


def load_game():
    """
    Loads the saved game state from the database if it exists.

    :return: A tuple containing player position, enemy positions, score, board height, board width, and game board.
             Returns None if no saved game state is found.
    """
    with sqlite3.connect(GAME_DB_PATH) as conn:
        cursor = conn.cursor()

        # Retrieve saved game state from the game_save table where id = 1
        cursor.execute('''
            SELECT player_position, enemy_positions, score, board_height, board_width, board 
            FROM game_save 
            WHERE id = 1
        ''')

        result = cursor.fetchone()  # Fetch the first row of the result set

    if result:
        # Convert JSON strings back to original data structures
        player_position = json.loads(result[0])
        enemy_positions = json.loads(result[1])
        score = result[2]
        board_height = result[3]
        board_width = result[4]
        board = json.loads(result[5])

        return player_position, enemy_positions, score, board_height, board_width, board

    return None  # Return None if no game state is found

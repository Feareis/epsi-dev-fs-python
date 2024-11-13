import sqlite3
import os

SCORE_DB_PATH = os.path.join("db", "scores.db")
GAME_DB_PATH = os.path.join("db", "game.db")

def initialize_scores_db():
    conn = sqlite3.connect(SCORE_DB_PATH)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS high_scores (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            player_name TEXT NOT NULL,
            score INTEGER NOT NULL
        )
    ''')
    conn.commit()
    conn.close()


def save_score(player_name, score):
    conn = sqlite3.connect("db/scores.db")  # DB Name
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO high_scores (player_name, score) VALUES (?, ?)
        ''', (player_name, score))
    conn.commit()
    conn.close()


def game_end(score):
    player_name = input("Entrez votre nom : ")
    save_score(player_name, score)  # Sauvegarde du score du joueur


def get_top_scores(limit=5):
    conn = sqlite3.connect("db/scores.db")  # DB Name
    cursor = conn.cursor()
    cursor.execute('''
        SELECT player_name, score
        FROM high_scores 
        ORDER BY score 
        DESC LIMIT ?
        ''', (limit,))
    scores = cursor.fetchall()
    conn.close()
    return scores


def initialize_game_db():
    conn = sqlite3.connect(GAME_DB_PATH)
    cursor = conn.cursor()
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
    conn.commit()
    conn.close()


def save_game(player_position, foes_positions, score, nb_line, nb_column, game_plate):
    conn = sqlite3.connect(GAME_DB_PATH)
    cursor = conn.cursor()
    # Supprimer la sauvegarde précédente
    cursor.execute('DELETE FROM game_save')
    cursor.execute('''
        INSERT INTO game_save (id, player_position, foes_positions, score, nb_line, nb_column, game_plate) 
        VALUES (?, ?, ?, ?, ?, ?, ?)
    ''', (
            1,
            str(player_position),
            str(foes_positions),
            score,
            nb_line,
            nb_column,
            str(game_plate)
        ))
    conn.commit()
    conn.close()

def load_game():
    conn = sqlite3.connect(GAME_DB_PATH)
    cursor = conn.cursor()
    cursor.execute('''
        SELECT player_position, foes_positions, score, nb_line, nb_column, game_plate 
        FROM game_save 
        WHERE id = 1
    ''')
    result = cursor.fetchone()
    conn.close()
    if result:
        player_position = eval(result[0])
        foes_positions = eval(result[1])
        score = result[2]
        nb_line = result[3]
        nb_column = result[4]
        game_plate = eval(result[5])
        return player_position, foes_positions, score, nb_line, nb_column, game_plate
    return None


# db game_2p ???
"""
def initialize_game_2p_db():
    conn = sqlite3.connect(GAME_DB_PATH)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS game_save (
            id INTEGER PRIMARY KEY, 
            player1_position TEXT, 
            player2_position TEXT, 
            foes_positions TEXT, 
            score_p1 INTEGER, 
            score_p2 INTEGER, 
            nb_line INTEGER, 
            nb_column INTEGER, 
            game_plate TEXT
        )
    ''')
    conn.commit()
    conn.close()


def save_game_2p(player1_position, player2_position, foes_positions, score_p1, score_p2, nb_line, nb_column, game_plate):
    conn = sqlite3.connect(GAME_DB_PATH)
    cursor = conn.cursor()
    # Supprimer la sauvegarde précédente
    cursor.execute('DELETE FROM game_save')
    cursor.execute('''
        INSERT INTO game_save (id, player1_position, player2_position, foes_positions, score_p1, score_p2, nb_line, nb_column, game_plate)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', (
            1,
            str(player1_position),
            str(player2_position),
            str(foes_positions),
            score_p1,
            score_p2,
            nb_line,
            nb_column,
            str(game_plate)
        ))
    conn.commit()
    conn.close()

def load_game_2p():
    conn = sqlite3.connect(GAME_DB_PATH)
    cursor = conn.cursor()
    cursor.execute('''
        SELECT player1_position, player2_position, foes_positions, score_p1, score_p2, nb_line, nb_column, game_plate
        FROM game_save 
        WHERE id = 1
    ''')
    result = cursor.fetchone()
    conn.close()
    if result:
        player1_position = eval(result[0])
        player2_position = eval(result[1])
        foes_positions = eval(result[2])
        score_p1 = result[3]
        score_p2 = result[4]
        nb_line = result[5]
        nb_column = result[6]
        game_plate = eval(result[7])
        return player1_position, player2_position, foes_positions, score_p1, score_p2, nb_line, nb_column, game_plate
    return None
"""
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
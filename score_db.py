import sqlite3


def initialize_db():
    conn = sqlite3.connect("bomberman_scores.db")
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
    conn = sqlite3.connect("bomberman_scores.db")  # DB Name
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO high_scores (player_name, score) VALUES (?, ?)
        ''', (player_name, score))
    conn.commit()
    conn.close()


def get_top_scores(limit=3):
    conn = sqlite3.connect("bomberman_scores.db")  # DB Name
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


def game_end(score):
    player_name = input("Entrez votre nom : ")
    save_score(player_name, score)  # Sauvegarde du score du joueur

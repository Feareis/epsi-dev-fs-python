import time
import game_settings as gs
import pygame


bombs = []  # Liste pour stocker les bombes posées avec leur position et heure de pose


def add_bomb(position):
    # Ajoute une bombe à la liste avec sa position et l'heure actuelle de pose ((x, y), time)
    bombs.append({"position": position, "time": time.time()})
    # print(f"Bombe posée à {position}")


def update_bombs(screen, game_plate, foes, player_position, nb_line, nb_column):
    # Met à jour les bombes en vérifiant si elles doivent exploser et retourne True si le joueur est touché
    current_time = time.time()
    # Liste des bombes qui doivent exploser (celles posées depuis plus de 2 secondes)
    to_explode = [bomb for bomb in bombs if current_time - bomb["time"] >= 2]

    player_hit = False
    # Parcourt les bombes qui doivent exploser
    for bomb in to_explode:
        # Déclenche l'explosion et vérifie si elle touche le joueur
        if explode_bomb(bomb["position"], game_plate, foes, player_position, nb_line, nb_column):
            player_hit = True  # Indique que le joueur est touché par une explosion
        bombs.remove(bomb)  # Supprime la bombe de la liste après explosion
    for bomb in bombs:  # Affiche toutes les bombes sur le plateau, même celles qui n'ont pas encore explosé
        x, y = bomb["position"]  # Position de la bombe
        rect = (y * gs.TAILLE_CASE, x * gs.TAILLE_CASE, gs.TAILLE_CASE, gs.TAILLE_CASE)  # Rectangle de la bombe
        pygame.draw.rect(screen, gs.COULEUR_BOMB, rect)  # Dessine la bombe en jaune
    return player_hit  # Retourne True si le joueur est touché par une explosion


def explode_bomb(position, game_plate, foes, player_position, nb_line, nb_column):
    x, y = position  # Coordonnées de la bombe
    explosion_area = [(x, y), (x + 1, y), (x + 2, y), (x - 1, y), (x - 2, y), (x, y + 1), (x, y + 2), (x, y - 1), (x, y - 2)]  # zone d'explosion : la position de la bombe et les 2 cases adjacentes
    player_hit = False
    for ex, ey in explosion_area:  # Parcourt chaque case dans la zone d'explosion
        if 0 <= ex < nb_line and 0 <= ey < nb_column:  # Vérifie si les coordonnées sont dans les limites du plateau
            if (ex, ey) == player_position:  # Vérifie si le joueur est dans la zone d'explosion
                player_hit = True  # Indique que le joueur a été touché par l'explosion
            if game_plate[ex][ey] == "B":  # Vérifie si une brique cassable est dans la zone d'explosion
                game_plate[ex][ey] = " "  # Remplace la brique cassable par une case vide
            elif (ex, ey) in foes:  # Vérifie si un ennemi ou plusieurs ennemis est dans la zone d'explosion
                foes.remove((ex, ey))  # Retire l'ennemi de la liste des ennemis

    return player_hit  # Retourne True si le joueur est touché par l'explosion

import pygame
import game_settings as gs


TAILLE_CASE = 40


def starting_plate(nb_line, nb_column, bricks):
    plate = []

    # Création du plateau avec des cases vides, et murs indestructibles en alternance sur les lignes, colonnes impaires
    for i in range(nb_line):
        if i % 2 == 0:
            ligne = [" " for _ in range(nb_column)]
        else:
            ligne = ["X" if j % 2 != 0 else " " for j in range(nb_column)]
        plate.append(ligne)

    # Ajout des briques au plateau de jeu
    for (x, y) in bricks:
        # On vérifie que les coordonnées sont valides
        if 0 <= x < nb_line and 0 <= y < nb_column:
            plate[x][y] = "B"
    return plate  # Plateau en 2D


def view_plate(screen, plate, player_position, foes):
    for i in range(len(plate)):  # Parcourt chaque ligne du plateau (axe vertical ou coordonnée y)
        for j in range(len(plate[i])):  # Parcourt chaque case de la ligne actuelle (axe horizontal ou coordonnée x)
            # Calcule les coordonnées en pixels pour dessiner chaque case à l’écran
            x, y = j * TAILLE_CASE, i * TAILLE_CASE

            # Vérifie si la position actuelle correspond à celle du joueur
            if (i, j) == player_position:
                pygame.draw.rect(screen, gs.COULEUR_JOUEUR, (x, y, TAILLE_CASE, TAILLE_CASE))

            # Vérifie si la position actuelle correspond à celle d'un ennemi
            elif (i, j) in foes:
                pygame.draw.rect(screen, gs.COULEUR_ENNEMI, (x, y, TAILLE_CASE, TAILLE_CASE))

            # Vérifie si la case actuelle est un mur indestructible
            elif plate[i][j] == "X":
                pygame.draw.rect(screen, gs.COULEUR_CASE_INDESTRUCTIBLE, (x, y, TAILLE_CASE, TAILLE_CASE))

            # Vérifie si la case actuelle est une brique cassable
            elif plate[i][j] == "B":
                pygame.draw.rect(screen, gs.COULEUR_BRIQUE_CASSABLE, (x, y, TAILLE_CASE, TAILLE_CASE))

            # Affiche une case vide si elle ne contient ni joueur, ni ennemi, ni mur, ni brique cassable
            else:
                pygame.draw.rect(screen, gs.COULEUR_CASE_VIDE, (x, y, TAILLE_CASE, TAILLE_CASE))

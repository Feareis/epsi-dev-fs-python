import pygame
import game_settings as gs


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
    return plate


def view_plate(screen, plate, player_position, foes):
    for i, row in enumerate(plate):  # Parcourt chaque ligne du plateau (i -> index de la ligne, row -> contenu de la ligne)
        for j, case in enumerate(row):  # Parcourt chaque case de la ligne (j -> index de la case, case -> contenu de la case)

            # Défini le rectangle pour la case actuelle
            rect = j * gs.TAILLE_CASE, i * gs.TAILLE_CASE, gs.TAILLE_CASE, gs.TAILLE_CASE

            # Vérifie si la position actuelle correspond à celle du joueur
            if (i, j) == player_position:
                pygame.draw.rect(screen, gs.COULEUR_JOUEUR, rect)

            # Vérifie si la position actuelle correspond à celle d'un ennemi
            elif (i, j) in foes:
                pygame.draw.rect(screen, gs.COULEUR_ENNEMI, rect)

            # Vérifie si la case actuelle est un mur indestructible
            elif case == "X":
                pygame.draw.rect(screen, gs.COULEUR_CASE_INDESTRUCTIBLE, rect)

            # Vérifie si la case actuelle est une brique cassable
            elif case == "B":
                pygame.draw.rect(screen, gs.COULEUR_BRIQUE_CASSABLE, rect)

            # Affiche une case vide si elle ne contient ni joueur, ni ennemi, ni mur, ni brique cassable
            else:
                pygame.draw.rect(screen, gs.COULEUR_CASE_VIDE, rect)

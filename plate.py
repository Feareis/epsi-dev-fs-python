import pygame
import random
import game_settings as gs


player1_live = True
player2_live = True


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


def random_plate(nb_line, nb_column, iratio=None, dratio=None):

    # Ratios aléatoires pour les murs indestructibles et cassables si non fournis
    iratio = iratio or random.uniform(0, 0.2)
    dratio = dratio or random.uniform(0, 0.4)

    plate = []
    for i in range(nb_line):
        row = []
        for j in range(nb_column):
            random_value = random.random()
            if random_value < iratio:
                row.append("X")  # Mur indestructible
            elif random_value < iratio + dratio:
                row.append("B")  # Brique cassable
            else:
                row.append(" ")  # Case vide
        plate.append(row)

    # Assurer une zone vide autour de la position initiale du joueur
    x, y = gs.STARTING_PLAYER1_POSITION
    if 0 <= x < nb_line and 0 <= y < nb_column:
        plate[x][y] = " "  # Position initiale du joueur
        if y + 1 < nb_column:
            plate[x][y + 1] = " "
        if x + 1 < nb_line:
            plate[x + 1][y] = " "
        if x + 1 < nb_line and y + 1 < nb_column:
            plate[x + 1][y + 1] = " "

    # Assurer une zone vide autour de la position initiale du joueur 2 (si elle existe dans game_settings)
    if hasattr(gs, 'STARTING_PLAYER2_POSITION'):
        x2, y2 = gs.STARTING_PLAYER2_POSITION
        if 0 <= x2 < nb_line and 0 <= y2 < nb_column:
            plate[x2][y2] = " "
            if y2 - 1 >= 0:
                plate[x2][y2 - 1] = " "
            if x2 - 1 >= 0:
                plate[x2 - 1][y2] = " "
            if x2 - 1 >= 0 and y2 - 1 >= 0:
                plate[x2 - 1][y2 - 1] = " "

    # Assurer une zone vide autour de la position initiale des ennemis
    for foe in gs.INITIAL_FOES_POSITIONS:
        fx, fy = foe
        if 0 <= fx < nb_line and 0 <= fy < nb_column:
            plate[fx][fy] = " "
            if fy + 1 < nb_column:
                plate[fx][fy + 1] = " "
            if fx + 1 < nb_line:
                plate[fx + 1][fy] = " "
            if fx + 1 < nb_line and fy + 1 < nb_column:
                plate[fx + 1][fy + 1] = " "

    return plate


def view_plate(screen, plate, player1_position, foes, player2_position=None):
    for i, row in enumerate(plate):  # Parcourt chaque ligne du plateau (i -> index de la ligne, row -> contenu de la ligne)
        for j, case in enumerate(row):  # Parcourt chaque case de la ligne (j -> index de la case, case -> contenu de la case)

            # Défini le rectangle pour la case actuelle
            rect = j * gs.TAILLE_CASE, i * gs.TAILLE_CASE, gs.TAILLE_CASE, gs.TAILLE_CASE

            # Vérifie si la position actuelle correspond à celle du joueur
            if player1_live and (i, j) == player1_position:
                pygame.draw.rect(screen, gs.COULEUR_JOUEUR1, rect)

            # Vérifie si la position actuelle correspond à celle du joueur 2, si défini
            elif player2_position and player2_live and (i, j) == player2_position:
                pygame.draw.rect(screen, gs.COULEUR_JOUEUR2, rect)

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


def view_plate_2p(screen, plate, player1_position, player2_position, foes):
    for i, row in enumerate(plate):  # Parcourt chaque ligne du plateau (i -> index de la ligne, row -> contenu de la ligne)
        for j, case in enumerate(row):  # Parcourt chaque case de la ligne (j -> index de la case, case -> contenu de la case)

            # Défini le rectangle pour la case actuelle
            rect = j * gs.TAILLE_CASE, i * gs.TAILLE_CASE, gs.TAILLE_CASE, gs.TAILLE_CASE

            # Vérifie si la position actuelle correspond à celle du joueur
            if (i, j) == player1_position:
                pygame.draw.rect(screen, gs.COULEUR_JOUEUR1, rect)

            # Vérifie si la position actuelle correspond à celle du joueur
            elif (i, j) == player2_position:
                pygame.draw.rect(screen, gs.COULEUR_JOUEUR2, rect)

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

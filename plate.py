def starting_plate(nb_line, nb_column, bricks):
    plate = []

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


def view_plate(plate, player_position, foes):
    for i in range(len(plate)):  # position x
        for j in range(len(plate[i])):  # position y
            if (i, j) == player_position:  # Si la position correspond, on affiche le joueur
                print("P", end=" ")  # Affichage du joueur
            elif (i, j) in foes:
                print("E", end=" ")  # Affichage du/des ennemi(s)
            else:
                print(plate[i][j], end=" ")  # Affichage d'une case vide ou d'un mur indestructible si il y a
        print()

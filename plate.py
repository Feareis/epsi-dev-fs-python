def starting_plate(nb_line, nb_column):
    plate = []
    for i in range(nb_line):
        if i % 2 == 0:  # Si il s'agit d'une ligne impaire
            line = []
            for _ in range(nb_column):
                line.append(" ")  # Case vide
        else:
            line = []
            for j in range(nb_column):
                if j % 2 != 0:  # Si il s'agit d'une colonne impaire
                    line.append("X")  # Mur indestructible
                else:
                    line.append(" ")  # Case vide
        plate.append(line)
    return plate  # Plateau en 2D

def view_plate(plate):
    for line in plate:
        print(" ".join(line))
# Haut -> z | Bas -> s | Gauche -> q | Droite -> d
moves = {
    "z": (-1, 0),
    "s": (1, 0),
    "q": (0, -1),
    "d": (0, 1)
}


def move_player(player_position, direction, plate):
    x, y = player_position

    # Si la direction est correcte, on additionne les coordonnées de mouvement à la position actuelle du joueur
    if direction in moves:
        dx, dy = moves[direction]
        nx, ny = x + dx, y + dy
        # On vérifie de ne pas sortir des limites du plateau et qu'on ne va pas sur une case indestructible
        if 0 <= nx < len(plate) and 0 <= ny < len(plate[0]) and plate[nx][ny] == " ":
            return nx, ny

    # Si le déplacement est impossible, on reste à la même position
    return x, y
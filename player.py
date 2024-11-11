import random
import math

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


def check_collision(player_position, foes):
    return player_position in foes


def move_foe(player_position, foe_position, plate):
    px, py = player_position
    fx, fy = foe_position
    if distance_euclidienne(player_position, foe_position) <= 4:
        dx, dy = 0, 0

        # horizontal
        if px > fx:
            dx = 1  # vers le bas
        elif px < fx:
            dx = -1  # vers le haut
        # vertical
        if py > fy:
            dy = 1  # vers la droite
        elif py < fy:
            dy = -1  # vers la gauche

        # Essayer de se déplacer en direction du joueur
        directions = [(dx, 0), (0, dy)]
        random.shuffle(directions)  # Mélange les directions pour rendre le mouvement imprévisible
        for dx, dy in directions:
            ndx, ndy = fx + dx, fy + dy
            # On vérifie de ne pas sortir des limites du plateau et qu'on ne va pas sur une case indestructible
            if 0 <= ndx < len(plate) and 0 <= ndy < len(plate[0]) and plate[ndx][ndy] == " ":
                return ndx, ndy
    else:
        # Sinon l'ennemi se déplace normalement et aléatoirement
        directions = list(moves.values())
        random.shuffle(directions)  # Mélange les directions pour rendre le mouvement imprévisible
        for dx, dy in directions:
            nx, ny = fx + dx, fy + dy
            # On vérifie de ne pas sortir des limites du plateau et qu'on ne va pas sur une case indestructible
            if 0 <= nx < len(plate) and 0 <= ny < len(plate[0]) and plate[nx][ny] == " ":
                return nx, ny

    # Si le déplacement est impossible, on reste à la même position
    return foe_position


def distance_euclidienne(player_position, foe_position):
    px, py = player_position
    fx, fy = foe_position
    return math.sqrt((px - py) ** 2 + (fx - fy) ** 2)

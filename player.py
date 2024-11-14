import random
import math


move = {
    # Joueur 1 : Haut -> z | Bas -> s | Gauche -> q | Droite -> d
    "z": (-1, 0),
    "s": (1, 0),
    "q": (0, -1),
    "d": (0, 1),
}

moves_p2 = {
    # Joueur 2 : Haut -> o | Bas -> l | Gauche -> k | Droite -> m
    "o": (-1, 0),
    "l": (1, 0),
    "k": (0, -1),
    "m": (0, 1),
}

def move_player(player_position, direction, plate, player_number=None, player2_position=None):

    x, y = player_position

    # Choisir le dictionnaire de mouvements en fonction du joueur
    if player_number is None:
        moves = move
    else:
        moves = moves_p2

    # Si la direction est correcte, on additionne les coordonnées de mouvement à la position actuelle du joueur
    if direction in moves:
        dx, dy = moves[direction]
        nx, ny = x + dx, y + dy
        # On vérifie de ne pas sortir des limites du plateau et qu'on ne va pas sur une case indestructible
        if 0 <= nx < len(plate) and 0 <= ny < len(plate[0]) and plate[nx][ny] == " " and (nx, ny) != player2_position:
            return nx, ny

    # Si le déplacement est impossible, on reste à la même position
    return x, y


def check_player_collision(player_position, foes):
    return player_position in foes


def check_player_collision_2p(player1_position, player2_position, foes, player1_live, player2_live):
    if player1_live and player1_position in foes:  # Vérifie les collisions pour le joueur 1
        player1_live = False
        print("Joueur 1 éliminé !")

    if player2_live and player2_position in foes:  # Vérifie les collisions pour le joueur 2
        player2_live = False
        print("Joueur 2 éliminé !")

    return player1_live, player2_live


def check_game_end(player1_live, player2_live):
    return not player1_live and not player2_live


def move_foe(player_position, foe_position, plate):
    px, py = player_position
    fx, fy = foe_position
    if distance_euclidienne(player_position, foe_position) <= 4:
        directions = []
        # horizontal
        if px > fx:
            directions.append((1, 0))  # vers le bas
        elif px < fx:
            directions.append((-1, 0))  # vers le haut
        # vertical
        if py > fy:
            directions.append((0, 1))  # vers la droite
        elif py < fy:
            directions.append((0, -1))  # vers la gauche

        # Mélange les directions pour choisir aléatoirement le déplacement de l'ennemi
        random.shuffle(directions)

        for dx, dy in directions:
            nx, ny = fx + dx, fy + dy
            # On vérifie de ne pas sortir des limites du plateau et qu'on ne va pas sur une case indestructible
            if 0 <= nx < len(plate) and 0 <= ny < len(plate[0]) and plate[nx][ny] == " ":
                return nx, ny

    # Sinon l'ennemi se déplace normalement et aléatoirement
    directions = list(move.values())
    random.shuffle(directions)  # Mélange les directions pour rendre le mouvement imprévisible
    for dx, dy in directions:
        nx, ny = fx + dx, fy + dy
        # On vérifie de ne pas sortir des limites du plateau et qu'on ne va pas sur une case indestructible
        if 0 <= nx < len(plate) and 0 <= ny < len(plate[0]) and plate[nx][ny] == " ":
            return nx, ny

    # Si le déplacement est impossible, on reste à la même position
    return foe_position


def update_foes_positions(player_position, foes, plate):
    foes_positions = []
    busy_position = set(foes)  # Gère les doublons
    for foe_position in foes:
        nw_foe_position = move_foe(player_position, foe_position, plate)
        if nw_foe_position in busy_position:  # Si la position est occupée, on bouge pas
            foes_positions.append(foe_position)
        else:  # Sinon on met à jour la position de l'ennemi
            foes_positions.append(nw_foe_position)
            busy_position.add(nw_foe_position)
    return foes_positions


def move_foe_2p(player1_position, player2_position, foe_position, plate, player1_live, player2_live):
    if player1_live and player2_live:
        de_p1 = distance_euclidienne(player1_position, foe_position)
        de_p2 = distance_euclidienne(player2_position, foe_position)
        if de_p1 <= de_p2:  # Choisir la position du joueur le plus proche
            target_position = player1_position
        else:
            target_position = player2_position
    elif player1_live:
        target_position = player1_position
    elif player2_live:
        target_position = player2_position
    else:
        return foe_position

    if distance_euclidienne(target_position, foe_position) <= 4:  # Utiliser le joueur cible si la distance est inférieure ou égale à 4
        px, py = target_position
        fx, fy = foe_position
        directions = []
        # horizontal
        if px > fx:
            directions.append((1, 0))  # vers le bas
        elif px < fx:
            directions.append((-1, 0))  # vers le haut
        # vertical
        if py > fy:
            directions.append((0, 1))  # vers la droite
        elif py < fy:
            directions.append((0, -1))  # vers la gauche

        # Mélange les directions pour choisir aléatoirement le déplacement de l'ennemi
        random.shuffle(directions)

        for dx, dy in directions:
            nx, ny = fx + dx, fy + dy
            # On vérifie de ne pas sortir des limites du plateau et qu'on ne va pas sur une case indestructible
            if 0 <= nx < len(plate) and 0 <= ny < len(plate[0]) and plate[nx][ny] == " ":
                return nx, ny

    # Sinon l'ennemi se déplace normalement et aléatoirement
    directions = list(move.values())
    random.shuffle(directions)  # Mélange les directions pour rendre le mouvement imprévisible
    for dx, dy in directions:
        nx, ny = foe_position[0] + dx, foe_position[1] + dy
        # On vérifie de ne pas sortir des limites du plateau et qu'on ne va pas sur une case indestructible
        if 0 <= nx < len(plate) and 0 <= ny < len(plate[0]) and plate[nx][ny] == " ":
            return nx, ny

    # Si le déplacement est impossible, on reste à la même position
    return foe_position


def update_foes_positions_2p(player1_position, player2_position, foes, plate, player1_live, player2_live):
    foes_positions = []
    busy_position = set(foes)  # Gère les doublons
    for foe_position in foes:
        nw_foe_position = move_foe_2p(player1_position, player2_position, foe_position, plate, player1_live, player2_live)
        if nw_foe_position in busy_position:  # Si la position est occupée, on bouge pas
            foes_positions.append(foe_position)
        else:  # Sinon on met à jour la position de l'ennemi
            foes_positions.append(nw_foe_position)
            busy_position.add(nw_foe_position)
    return foes_positions


def distance_euclidienne(pos1, pos2):
    px, py = pos1
    fx, fy = pos2
    return math.sqrt((px-py)**2+(fx-fy)**2)

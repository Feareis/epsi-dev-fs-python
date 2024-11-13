import pygame

# Configuration initiale pour Pygame
pygame.init()

# Exemple de configuration pour le plateau et les positions initiales des joueurs
plate = [[' ' for _ in range(10)] for _ in range(10)]
player1_position = (0, 0)  # Position initiale du joueur 1
player2_position = (9, 9)  # Position initiale du joueur 2

# Joueur 1 : Haut -> z | Bas -> s | Gauche -> q | Droite -> d
# Joueur 2 : Haut -> o | Bas -> l | Gauche -> k | Droite -> m

moves_j1 = {
    "z": (-1, 0),
    "s": (1, 0),
    "q": (0, -1),
    "d": (0, 1),
}

moves_j2 = {
    "o": (-1, 0),
    "l": (1, 0),
    "k": (0, -1),
    "m": (0, 1),
}


def move_player(player_position, direction, plate, moves):
    x, y = player_position
    if direction in moves:
        dx, dy = moves[direction]
        nx, ny = x + dx, y + dy
        # Vérification des limites du plateau et si la case est vide
        if 0 <= nx < len(plate) and 0 <= ny < len(plate[0]) and plate[nx][ny] == " ":
            return nx, ny
    # Retourne la position d'origine si le mouvement est impossible
    return player_position


# Boucle de jeu
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            # Gérer le mouvement du joueur 1
            if event.unicode in moves_j1:
                player1_position = move_player(player1_position, event.unicode, plate, moves_j1)
            # Gérer le mouvement du joueur 2
            elif event.unicode in moves_j2:
                player2_position = move_player(player2_position, event.unicode, plate, moves_j2)

    # Affichage des positions pour debug
    print(f"Player 1 Position: {player1_position}")
    print(f"Player 2 Position: {player2_position}")

# Quitter Pygame
pygame.quit()

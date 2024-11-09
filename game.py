import plate
import player
import pygame
import game_settings as gs


"""
Initialisation de Pygame
"""

pygame.init()  # Initialisation de la bibliothèque Pygame
TAILLE_FENETRE = 520  # Définition de la taille de la fenêtre (dimensions carrées)
screen = pygame.display.set_mode((TAILLE_FENETRE, TAILLE_FENETRE))
pygame.display.set_caption("Bomberman")  # Titre de la fenêtre du jeu


"""
Paramètres du jeu
"""

nb_line = 13  # Dimensions du plateau de jeu (nombre de lignes)
nb_column = 13  # Dimensions du plateau de jeu (nombre de colonnes)
foes = [(4, 5), (5, 6), (9, 8), (3, 10)]  # Positions des ennemis sur le plateau
game_plate = plate.starting_plate(nb_line, nb_column, bricks=[(0, 4), (4, 6), (11, 13), (2, 7), (2, 7)])  # Création du plateau de jeu
player_position = (0, 0)  # Position initiale du joueur


"""
Boucle de jeu
"""

run = True
while run:
    for event in pygame.event.get():  # Gestion des événements de Pygame (fermeture de la fenêtre et appui sur les touches)
        if event.type == pygame.QUIT:
            run = False  # Quitte la boucle si l'événement de fermeture est détecté
        elif event.type == pygame.KEYDOWN:  # Gestion des mouvements du joueur en fonction de la touche appuyée
            if event.key == pygame.K_z:
                player_position = player.move_player(player_position, "z", game_plate)
            elif event.key == pygame.K_s:
                player_position = player.move_player(player_position, "s", game_plate)
            elif event.key == pygame.K_q:
                player_position = player.move_player(player_position, "q", game_plate)
            elif event.key == pygame.K_d:
                player_position = player.move_player(player_position, "d", game_plate)

            if player.check_collision(player_position, foes):  # Vérifie si le joueur entre en collision avec un ennemi
                print("Perdu !")
                run = False

    # Dessine le plateau et les éléments
    screen.fill(gs.COULEUR_FOND)  # couleurs background
    plate.view_plate(screen, game_plate, player_position, foes)  # Dessine le plateau de jeu et les éléments (joueur, ennemis, murs) à l'écran
    pygame.display.flip()  # Met à jour l'affichage de Pygame pour montrer les éléments récemment dessinés

pygame.quit()  # Quand la boucle de jeu est finie, quitte Pygame

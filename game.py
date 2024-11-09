import plate
import player
import bomb
import pygame
import game_settings as gs

"""
Initialisation de Pygame
"""

pygame.init()  # Initialisation de la bibliothèque Pygame
TAILLE_FENETRE = gs.TAILLE_CASE * 13  # Définition de la taille de la fenêtre (taille plateau de jeu)
screen = pygame.display.set_mode((TAILLE_FENETRE, TAILLE_FENETRE))
pygame.display.set_caption("Bomberman")  # Titre de la fenêtre du jeu

font = pygame.font.Font(None, 36)  # Définir la police d'affichage pour le score


"""
Paramètres du jeu
"""

nb_line, nb_column = 13, 13  # Dimensions du plateau de jeu (nombre de lignes et de colonnes)
foes = [(4, 5), (5, 6), (9, 8), (3, 10)]  # Positions des ennemis sur le plateau
game_plate = plate.starting_plate(nb_line, nb_column, bricks=[(0, 4), (4, 6), (11, 13), (2, 7), (2, 7)])  # Création du plateau de jeu
player_position = (0, 0)  # Position initiale du joueur

score = 100  # Le joueur commence avec 100 points
dscore = 1

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
                score -= dscore
            elif event.key == pygame.K_s:
                player_position = player.move_player(player_position, "s", game_plate)
                score -= dscore
            elif event.key == pygame.K_q:
                player_position = player.move_player(player_position, "q", game_plate)
                score -= dscore
            elif event.key == pygame.K_d:
                player_position = player.move_player(player_position, "d", game_plate)
                score -= dscore
            elif event.key == pygame.K_b:  # Ajoute une bombe avec la touche "b"
                bomb.add_bomb(player_position)

            if player.check_collision(player_position, foes):  # Vérifie si le joueur entre en collision avec un ennemi
                print("Perdu !")
                run = False

    # Dessine le plateau et les éléments
    screen.fill(gs.COULEUR_FOND)  # couleurs background
    plate.view_plate(screen, game_plate, player_position, foes)  # Dessine le plateau de jeu et les éléments (joueur, ennemis, murs) à l'écran

    score_text = font.render(f"Score: {score}", True, (0, 0, 0))  # affiche le score en cours
    screen.blit(score_text, (10, 10))  # destination d'affichage -> top left

    # Si le score tombe à 0, la partie est perdue
    if score == 0:
        print("Perdu !")
        run = False

    # Met à jour les bombes, gère leur affichage et leur explosion
    if bomb.update_bombs(screen, game_plate, foes, player_position, nb_line, nb_column):
        print("Perdu !")
        run = False

    pygame.display.flip()  # Met à jour l'affichage de Pygame pour montrer les éléments récemment dessinés

pygame.quit()  # Quand la boucle de jeu est finie, quitte Pygame

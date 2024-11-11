import plate
import player
import bomb
import pygame
import game_settings as gs
import score_db


def run_game():
    """
    Initialisation de Pygame
    """

    pygame.init()  # Initialisation de la bibliothèque Pygame
    TAILLE_FENETRE = gs.TAILLE_FENETRE
    screen = pygame.display.set_mode((TAILLE_FENETRE, TAILLE_FENETRE), pygame.RESIZABLE)
    pygame.display.set_caption("Bomberman")  # Titre de la fenêtre du jeu

    font = pygame.font.Font(None, 36)  # Définir la police d'affichage pour le score


    """
    Initialisation de Pygame
    """

    score_db.initialize_db()


    """
    Paramètres du jeu
    """

    nb_line, nb_column = 13, 13  # Dimensions du plateau de jeu (nombre de lignes et de colonnes)
    foes = [(4, 5), (5, 6), (9, 8), (3, 10)]  # Positions des ennemis sur le plateau
    # game_plate = plate.starting_plate(nb_line, nb_column, bricks=[(0, 4), (4, 6), (11, 13), (2, 7), (2, 7)])  # Création du plateau de jeu fixe
    game_plate = plate.random_plate(nb_line, nb_column)  # Plateau random avec ratio
    player_position = gs.STARTING_PLAYER_POSITION  # Position initiale du joueur

    score = 1000  # Le joueur commence avec 1000 points
    dscore = 1

    # Délai entre les déplacements des ennemis (ms)
    foes_move_delay = 1000
    last_foe_move_time = pygame.time.get_ticks()


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

        # Vérifie si le délai de déplacement des ennemis est écoulé
        ct = pygame.time.get_ticks()
        if ct - last_foe_move_time > foes_move_delay:  # si (temps actuel - dernier mouvement > delai de mouvement enemi)
            foes = [player.move_foe(foe, game_plate) for foe in foes]  # Met à jour toute les positions
            last_foe_move_time = ct  # Met à jour le dernier moment de déplacement des ennemis

        # Dessine le plateau et les éléments
        screen.fill(gs.COULEUR_FOND)  # couleurs background
        plate.view_plate(screen, game_plate, player_position, foes)  # Dessine le plateau de jeu et les éléments (joueur, ennemis, murs) à l'écran

        if not foes:
            print("Gagné !")  # # Si il n'y a plus d'ennemis, la partie est gagné
            score_db.game_end(score)
            run = False

        # Score
        if score > 0:
            score_text = font.render(f"Score: {score}", True, (0, 0, 0))  # affiche le score en cours
            screen.blit(score_text, (10, 10))  # destination d'affichage -> top left
        else:
            print("Perdu !")  # Si le score tombe à 0, la partie est perdue
            run = False

        # Met à jour les bombes, gère leur affichage et leur explosion
        if bomb.update_bombs(screen, game_plate, foes, player_position, nb_line, nb_column):
            print("Perdu !")
            run = False

        pygame.display.flip()  # Met à jour l'affichage de Pygame pour montrer les éléments récemment dessinés

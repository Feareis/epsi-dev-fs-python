import menu
import plate
import player
import bomb
import pygame
import game_settings as gs
import db


global player1_live, player2_live

def run_game_2p():
    global player1_live, player2_live
    pygame.init()  # Initialisation de la bibliothèque Pygame


    """
    Initialisation des paramètres de la fenêtres
    """
    screen = pygame.display.set_mode((gs.TAILLE_FENETRE, gs.TAILLE_FENETRE), pygame.RESIZABLE)
    pygame.display.set_caption("Bomberman")  # Titre de la fenêtre du jeu
    # font = pygame.font.Font(None, 36)  # Définir la police d'affichage pour le score


    """
    Initialisation des db
    """
    db.initialize_scores_db()
    # db.initialize_game_2p_db() -> à voir


    """
    Paramètres du jeu
    """
    nb_line, nb_column = 13, 13  # Dimensions du plateau de jeu (nombre de lignes et de colonnes)
    foes = gs.INITIAL_FOES_POSITIONS  # Positions des ennemis sur le plateau
    # game_plate = plate.starting_plate(nb_line, nb_column, bricks=[(0, 4), (4, 6), (11, 13), (2, 7), (2, 7)])  # Création du plateau de jeu fixe
    game_plate = plate.random_plate(nb_line, nb_column)  # Plateau random avec ratio
    player1_position = gs.STARTING_PLAYER1_POSITION  # Position initiale du joueur 1
    player2_position = (nb_line - 1, nb_column - 1)  # Position initiale du joueur 2
    score_j1 = 1000  # Le joueur 1 commence avec 1000 points
    score_j2 = 1000  # Le joueur 2 commence avec 1000 points
    player1_live = True
    player2_live = True
    dscore = 1  # décrémentation de score
    foes_move_delay = 1000  # Délai entre les déplacements des ennemis (ms)
    last_foe_move_time = pygame.time.get_ticks()  # Initialisation du tick de deplacement (temps écoulé depuis le dernier mouvement)


    """
    Boucle de jeu
    """
    run = True
    while run:
        for event in pygame.event.get():  # Gestion des événements de Pygame (fermeture de la fenêtre et appui sur les touches)
            if event.type == pygame.QUIT:
                run = False  # Quitte la boucle si l'événement de fermeture est détecté
            elif event.type == pygame.KEYDOWN:  # Gestion des mouvements du joueur en fonction de la touche appuyée
                if event.key == pygame.K_ESCAPE:
                    choice = menu.pause_2p_menu()
                    if choice == "Reprendre":
                        continue
                    elif choice == "Options":
                        print("Options")
                    elif choice == "Menu principal":
                        run = False  # Quitte la partie pour revenir au menu principal sans sauvegarde

                keys = pygame.key.get_pressed()

                # Déplacements du Joueur 1
                if keys[pygame.K_z]:
                    player1_position = player.move_player(player1_position, "z", game_plate)
                    score_j1 -= dscore
                elif keys[pygame.K_s]:
                    player1_position = player.move_player(player1_position, "s", game_plate)
                    score_j1 -= dscore
                elif keys[pygame.K_q]:
                    player1_position = player.move_player(player1_position, "q", game_plate)
                    score_j1 -= dscore
                elif keys[pygame.K_d]:
                    player1_position = player.move_player(player1_position, "d", game_plate)
                    score_j1 -= dscore
                if keys[pygame.K_e]:
                    bomb.add_bomb(player1_position)

                # Déplacements du Joueur 2
                if keys[pygame.K_o]:
                    player2_position = player.move_player(player2_position, "o", game_plate, 2)
                    score_j2 -= dscore
                elif keys[pygame.K_l]:
                    player2_position = player.move_player(player2_position, "l", game_plate, 2)
                    score_j2 -= dscore
                elif keys[pygame.K_k]:
                    player2_position = player.move_player(player2_position, "k", game_plate, 2)
                    score_j2 -= dscore
                elif keys[pygame.K_m]:
                    player2_position = player.move_player(player2_position, "m", game_plate, 2)
                    score_j2 -= dscore
                if keys[pygame.K_i]:
                    bomb.add_bomb(player2_position)

        # vérification des collision j/j - e/j
        player1_live = player.check_elemination(player1_position, foes, player1_live)
        player2_live = player.check_elemination(player2_position, foes, player2_live)

        # Vérifie si le délai de déplacement des ennemis est écoulé
        ct = pygame.time.get_ticks()
        if ct - last_foe_move_time > foes_move_delay:  # si (temps actuel - dernier mouvement > delai de mouvement enemi)
            foes = [player.move_foe(player1_position, foe, game_plate) for foe in foes]  # Met à jour toute les positions ennemis
            last_foe_move_time = ct  # Met à jour le dernier moment de déplacement des ennemis

            # vérification des collision j/j - e/j
            player1_live = player.check_elemination(player1_position, foes, player1_live)
            player2_live = player.check_elemination(player2_position, foes, player2_live)

        # Dessine le plateau et les éléments
        screen.fill(gs.COULEUR_FOND)  # couleurs background
        plate.view_plate(screen, game_plate, player1_position, foes, player2_position)  # Dessine le plateau de jeu et les éléments (joueur, ennemis, murs) à l'écran

        if not foes:
            print("Gagné !")  # Si il n'y a plus d'ennemis, la partie est gagné
            run = False

        # Met à jour les bombes, gère leur affichage et leur explosion
        if bomb.update_bombs(screen, game_plate, foes, player1_position, nb_line, nb_column):
            player1_live = False
        if bomb.update_bombs(screen, game_plate, foes, player2_position, nb_line, nb_column):
            player2_live = False

        pygame.display.flip()  # Met à jour l'affichage de Pygame pour montrer les éléments récemment dessinés

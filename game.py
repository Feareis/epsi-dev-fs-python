import menu
import plate
import player
import bomb
import pygame
import game_settings as gs
import time
import db


def run_game(load_saved=False):
    pygame.init()  # Initialisation de la bibliothèque Pygame


    """
    Initialisation des paramètres de la fenêtres
    """
    screen = pygame.display.set_mode((gs.TAILLE_FENETRE, gs.TAILLE_FENETRE), pygame.RESIZABLE)
    pygame.display.set_caption("Bomberman")  # Titre de la fenêtre du jeu
    font = pygame.font.Font(None, 36)  # Définir la police d'affichage pour le score


    """
    Initialisation des db
    """
    db.initialize_scores_db()
    db.initialize_game_db()


    """
    Paramètres du jeu
    """
    # Temps maximum de jeu : 10 minutes
    max_game_time = 600
    start_time = time.time()

    if load_saved:
        loaded_game = db.load_game()
        if loaded_game:
            player_position, foes, score, nb_line, nb_column, game_plate = loaded_game
        else:
            return
    else:
        nb_line, nb_column = menu.size_menu() # Dimensions du plateau de jeu (nombre de lignes et de colonnes)
        foes = gs.INITIAL_FOES_POSITIONS  # Positions des ennemis sur le plateau
        # game_plate = plate.starting_plate(nb_line, nb_column, bricks=[(0, 4), (4, 6), (11, 13), (2, 7), (2, 7)])  # Création du plateau de jeu fixe
        game_plate = plate.random_plate(nb_line, nb_column)  # Plateau random avec ratio
        player_position = gs.STARTING_PLAYER1_POSITION  # Position initiale du joueur
        score = 1000  # Le joueur 1 commence avec 1000 points

    dscore = 1  # décrémentation de score
    foes_move_delay = 1000  # Délai entre les déplacements des ennemis (ms)
    last_foe_move_time = pygame.time.get_ticks()  # Initialisation du tick de deplacement (temps écoulé depuis le dernier mouvement)


    """
    Boucle de jeu
    """
    run = True
    while run:
        # Calcul du temps restant
        temp_time = time.time() - start_time
        remaining_time = max(0, int(max_game_time - temp_time))

        # Vérifie si le temps est écoulé
        if remaining_time <= 0:
            print("Temps écoulé !")
            run = False

        # Formate le temps restant en minutes et secondes
        minutes, seconds = divmod(remaining_time, 60)
        time_text = f"Temps : {minutes:02d}:{seconds:02d}"

        # Affichage du temps en haut à droite
        time_display = font.render(time_text, True, gs.BLACK)
        screen.blit(time_display, (gs.TAILLE_FENETRE // 2 - time_display.get_width() // 2, 100))

        for event in pygame.event.get():  # Gestion des événements de Pygame (fermeture de la fenêtre et appui sur les touches)
            if event.type == pygame.QUIT:
                run = False  # Quitte la boucle si l'événement de fermeture est détecté
            elif event.type == pygame.KEYDOWN:  # Gestion des mouvements du joueur en fonction de la touche appuyée
                if event.key == pygame.K_ESCAPE:
                    choice = menu.pause_menu()
                    if choice == "Reprendre":
                        continue
                    elif choice == "Sauvegarder la partie":
                        db.save_game(player_position, foes, score, nb_line, nb_column, game_plate)
                        run = False
                    elif choice == "Options":
                        menu.options_menu(game_mode="game")
                    elif choice == "Menu principal":
                        run = False  # Quitte la partie pour revenir au menu principal sans sauvegarde


                elif event.key in [pygame.K_z, pygame.K_s, pygame.K_q, pygame.K_d]:
                    direction = event.unicode
                    player_position = player.move_player(player_position, direction, game_plate)
                    score -= dscore
                elif event.key == pygame.K_b:
                    bomb.add_bomb(player_position)

        if player.check_player_collision(player_position, foes):  # Vérifie si le joueur entre en collision avec un ennemi ou l'inverse
            print("Perdu !")
            run = False

        # Vérifie si le délai de déplacement des ennemis est écoulé
        ct = pygame.time.get_ticks()
        if ct - last_foe_move_time > foes_move_delay:  # si (temps actuel - dernier mouvement > delai de mouvement enemi)
            foes = [player.move_foe(player_position, foe, game_plate) for foe in foes]  # Met à jour toute les positions ennemis
            last_foe_move_time = ct  # Met à jour le dernier moment de déplacement des ennemis

            if player.check_player_collision(player_position, foes):  # Vérifie si le joueur entre en collision avec un ennemi ou l'inverse
                print("Perdu !")
                run = False

        # Dessine le plateau et les éléments
        screen.fill(gs.COULEUR_FOND)  # couleurs background
        plate.view_plate(screen, game_plate, player_position, foes)  # Dessine le plateau de jeu et les éléments (joueur, ennemis, murs) à l'écran

        if not foes:
            print("Gagné !")  # # Si il n'y a plus d'ennemis, la partie est gagné
            db.game_end(score)
            run = False

        # Score
        if score > 0:
            score_text = font.render(f"Score: {score}", True, gs.BLACK)  # affiche le score en cours
            screen.blit(score_text, (10, 10))  # destination d'affichage -> top left
        else:
            print("Perdu !")  # Si le score tombe à 0, la partie est perdue
            run = False

        # Met à jour les bombes, gère leur affichage et leur explosion
        if bomb.update_bombs(screen, game_plate, foes, player_position, nb_line, nb_column):
            print("Perdu !")
            run = False

        pygame.display.flip()  # Met à jour l'affichage de Pygame pour montrer les éléments récemment dessinés

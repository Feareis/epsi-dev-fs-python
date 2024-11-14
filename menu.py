import pygame
import sys
import game
import game_2p
import db
import game_settings as gs

'''
Initialisation de Pygame
'''
pygame.init()


'''
Configuration de la fenêtre
'''
screen = pygame.display.set_mode((gs.TAILLE_FENETRE, gs.TAILLE_FENETRE), pygame.RESIZABLE)


'''
Configuration des couleurs et fonts
'''
WHITE = gs.WHITE
BLACK = gs.BLACK
font = pygame.font.Font(None, 36)


def draw_menu(title, options):
    selected_option = 0
    while True:
        screen.fill(WHITE)

        # Afficher le titre du menu
        title_text = font.render(title, True, BLACK)
        screen.blit(title_text, (gs.TAILLE_FENETRE // 2 - title_text.get_width() // 2, 50))

        # Afficher chaque option
        for i, option in enumerate(options):
            if option == " ":
                continue  # Ignore une option vide " "
            if i == selected_option:
                color = gs.SELECTED
            else:
                color = BLACK
            option_text = font.render(option, True, color)
            screen.blit(option_text, (gs.TAILLE_FENETRE // 2 - option_text.get_width() // 2, 150 + i * 40))

        pygame.display.flip()

        # Gestion des événements
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    selected_option = (selected_option - 1) % len(options)
                    while options[selected_option] == " ":
                        selected_option = (selected_option - 1) % len(options)
                elif event.key == pygame.K_DOWN:
                    selected_option = (selected_option + 1) % len(options)
                    while options[selected_option] == " ":
                        selected_option = (selected_option + 1) % len(options)
                elif event.key == pygame.K_RETURN:
                    return options[selected_option]  # Retourne l'option sélectionnée

def show_scores():
    screen.fill(WHITE)
    title = font.render("- Meilleurs Scores (Solo uniquement) -", True, BLACK)
    screen.blit(title, (gs.TAILLE_FENETRE // 2 - title.get_width() // 2, 50))

    # Affiche les meilleurs scores depuis la base de données
    top_scores = db.get_top_scores()
    for i, (name, score) in enumerate(top_scores, start=1):
        score_text = font.render(f"{i}. {name} - {score} points", True, BLACK)
        screen.blit(score_text, (gs.TAILLE_FENETRE // 2 - score_text.get_width() // 2, 100 + i * 30))

    pygame.display.flip()

    # appui sur une touche pour revenir au menu
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                waiting = False  # Quitte l'affichage des scores si une touche est pressée

def display_main_menu():
    options = ["Nouvelle Partie", "Charger une partie", "Meilleurs Scores", "Options", " ", "Quitter"]
    while True:
        choice = draw_menu("- Menu -", options)
        if choice == "Nouvelle Partie":
            new_game_menu()  # Envoie vers le menu nouvelle partie
        elif choice == "Charger une partie":
            load_game_menu()  # Affiche le menu de restauration d'une partie solo
        elif choice == "Meilleurs Scores":
            show_scores()  # Affiche les scores
        elif choice == "Options":
            options_menu()  # Affiche les options (non utilisable)
        elif choice == "Quitter":
            pygame.quit()  # Ferme la fenêtre
            sys.exit()


def pause_menu():
    options = ["Reprendre", "Sauvegarder la partie", "Options", " ", "Menu principal"]
    return draw_menu("- Pause -", options)


def pause_2p_menu():
    options = ["Reprendre", "Options", " ", "Menu principal"]
    return draw_menu("- Pause -", options)


def new_game_menu():
    options = ["Solo", "Multi", " ", "Menu principale"]
    choice = draw_menu("- Nouvelle Partie -", options)
    if choice == "Solo":
        game.run_game()
    elif choice == "Multi":
        game_2p.run_game_2p()  # Utilise le module multi-joueur
    elif choice == "Menu principale":
        return  # Retourne au menu principal sans action supplémentaire

def load_game_menu():
    options = ["Charger une partie - Solo", " ", "Menu principale"]
    choice = draw_menu("- Charger une partie -", options)

    if choice == "Charger une partie - Solo":
        game.run_game(load_saved=True)
    elif choice == "Menu principale":
        return  # Retourne au menu principal sans faire d'actions supplémentaires


def options_menu(game_mode="game"):
    options = ["Langues", "Keybinds", " ", "Retour"]
    choice = draw_menu("- Options -", options)

    if choice == "Langues":
        print("Langue")
    elif choice == "Touche":
        print("Keybinds")
    elif choice == "Retour":
        # Retourne au bon menu de pause en fonction du mode de jeu
        if game_mode == "game":
            return pause_menu()  # Retourne au menu pause de game
        elif game_mode == "game_2p":
            return pause_2p_menu()  # Retourne au menu pause de game_2p


def size_menu():
    # Initialisation de Pygame
    pygame.init()
    pygame.display.set_caption("Bomberman")

    # Paramètres de taille initiale
    nb_line = 13
    nb_column = 13
    selected = "lines"  # Définit si on ajuste les lignes ou les colonnes

    while True:
        screen.fill(WHITE)

        # Afficher les instructions
        title_text = font.render("- Taille du plateau -", True, BLACK)
        screen.blit(title_text, (gs.TAILLE_FENETRE // 2 - title_text.get_width() // 2, 50))

        # Afficher les options Lignes et Colonnes sur la même ligne avec espace
        line_color = gs.SELECTED if selected == "lines" else BLACK
        column_color = gs.SELECTED if selected == "columns" else BLACK

        # Rendu des textes
        line_text = font.render(f"Lignes: {nb_line}", True, line_color)
        column_text = font.render(f"Colonnes: {nb_column}", True, column_color)

        # Positionnement pour un affichage côte à côte
        line_text_x = (gs.TAILLE_FENETRE // 2) - line_text.get_width() - 20
        column_text_x = (gs.TAILLE_FENETRE // 2) + 20

        screen.blit(line_text, (line_text_x, 150))
        screen.blit(column_text, (column_text_x, 150))

        # Afficher le texte d'instructions
        instructions_text = font.render("[Enter] pour valider la saisie", True, BLACK)
        screen.blit(instructions_text, (gs.TAILLE_FENETRE // 2 - instructions_text.get_width() // 2, 300))

        pygame.display.flip()

        # Gestion des événements
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                # Ajuste le nombre de lignes ou de colonnes
                if event.key == pygame.K_UP:
                    if selected == "lines":
                        nb_line += 1
                    elif selected == "columns":
                        nb_column += 1
                elif event.key == pygame.K_DOWN:
                    if selected == "lines":
                        nb_line -= 1
                    elif selected == "columns":
                        nb_column -= 1
                elif event.key == pygame.K_RIGHT:
                    if selected == "lines":
                        selected = "columns"  # Passe à la sélection des colonnes
                elif event.key == pygame.K_LEFT:
                    if selected == "columns":
                        selected = "lines"  # Passe à la sélection des lignes
                elif event.key == pygame.K_RETURN:
                    # Retourne la taille choisie une fois validée
                    return nb_line, nb_column


if __name__ == "__main__":
    display_main_menu()

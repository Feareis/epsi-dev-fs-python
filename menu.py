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
pygame.display.set_caption("Bomberman")


'''
Configuration des couleurs et fonts
'''
WHITE = gs.WHITE
BLACK = gs.BLACK
SELECTED = gs.BLUE
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
            if i == selected_option:
                color = SELECTED
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
                elif event.key == pygame.K_DOWN:
                    selected_option = (selected_option + 1) % len(options)
                elif event.key == pygame.K_RETURN:
                    return options[selected_option]  # Retourne l'option sélectionnée

def show_scores():
    screen.fill(WHITE)
    title = font.render("- Meilleurs Scores -", True, BLACK)
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

def main_menu():
    options = ["Nouvelle Partie", "Meilleurs Scores", "Options", "Quitter"]
    while True:
        choice = draw_menu("- Menu -", options)
        if choice == "Nouvelle Partie":
            new_game_menu()  # Envoie vers le menu nouvelle partie
        elif choice == "Meilleurs Scores":
            show_scores()  # Affiche les scores
        elif choice == "Options":
            print("Options")  # Affiche les options
        elif choice == "Quitter":
            pygame.quit()  # Ferme la fenêtre
            sys.exit()


def pause_menu():
    options = ["Reprendre", "Sauvegarder la partie", "Options", "Menu principal"]
    return draw_menu("- Pause -", options)


def pause_2p_menu():
    options = ["Reprendre", "Options", "Menu principal"]
    return draw_menu("- Pause -", options)


def new_game_menu():
    options = ["Solo", "Multi", "Options", "Menu principale"]
    choice = draw_menu("- Nouvelle Partie -", options)
    if choice == "Solo":
        game.run_game()
    elif choice == "Multi":
        game_2p.run_game_2p()  # Utilise le module multi-joueur
    elif choice == "Options":
        options_menu()  # Affiche les options (non utilisable)
    elif choice == "Menu principale":
        return  # Retourne au menu principal sans action supplémentaire

def load_game_menu():
    options = ["Charger une partie - Solo", "Charger une partie - Multi", "Retour", "Menu principale"]
    choice = draw_menu("- harger une partie -", options)

    if choice == "Charger une partie - Solo":
        game.run_game(load_saved=True)
    elif choice == "Retour":
        new_game_menu()  # Retourne au menu précédent
    elif choice == "Menu principale":
        return  # Retourne au menu principal sans faire d'actions supplémentaires


def options_menu():
    options = ["Langues", "Keybinds", "Menu principale"]
    choice = draw_menu("- Options -", options)

    if choice == "Langues":
        print("Langue")
    elif choice == "Keybinds":
        print("Keybinds")
    elif choice == "Menu principale":
        return  # Retourne au menu principal sans faire d'actions supplémentaires



if __name__ == "__main__":
    main_menu()

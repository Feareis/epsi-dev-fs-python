import pygame
import sys
import game
import db
import game_settings as gs
from game_settings import TAILLE_FENETRE

'''
Initialisation de Pygame
'''
pygame.init()


'''
Configuration de la fenêtre
'''
screen = pygame.display.set_mode((TAILLE_FENETRE, TAILLE_FENETRE), pygame.RESIZABLE)
pygame.display.set_caption("Bomberman")


'''
Configuration des couleurs et fonts
'''
WHITE = gs.WHITE
BLACK = gs.BLACK
SELECTED = gs.BLUE
font = pygame.font.Font(None, 36)


def draw_menu(title, options, transparent=False):
    selected_option = 0
    if transparent:
        overlay = pygame.Surface((TAILLE_FENETRE, TAILLE_FENETRE))
        overlay.set_alpha(150)  # Définir la transparence (0 = totalement transparent, 255 = opaque)
        overlay.fill((0, 0, 0))  # Couleur de fond du menu semi-transparent
    while True:
        screen.fill(WHITE)

        # Afficher le titre du menu
        title_text = font.render(title, True, BLACK)
        screen.blit(title_text, (TAILLE_FENETRE // 2 - title_text.get_width() // 2, 50))

        # Afficher chaque option
        for i, option in enumerate(options):
            if i == selected_option:
                color = SELECTED
            else:
                color = BLACK
            option_text = font.render(option, True, color)
            screen.blit(option_text, (TAILLE_FENETRE // 2 - option_text.get_width() // 2, 150 + i * 40))

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
    screen.blit(title, (TAILLE_FENETRE // 2 - title.get_width() // 2, 50))

    # Affiche les meilleurs scores depuis la base de données
    top_scores = db.get_top_scores()
    for i, (name, score) in enumerate(top_scores, start=1):
        score_text = font.render(f"{i}. {name} - {score} points", True, BLACK)
        screen.blit(score_text, (TAILLE_FENETRE // 2 - score_text.get_width() // 2, 100 + i * 30))

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
    options = ["Nouvelle Partie", "Charger une partie", "Meilleurs Scores", "Options", "Quitter"]
    while True:
        choice = draw_menu("- Menu -", options)
        if choice == "Nouvelle Partie":
            game.run_game()  # Crée une nouvelle partie
        elif choice == "Charger une partie":
            game.run_game()  # Charge une partie
        elif choice == "Meilleurs Scores":
            show_scores()  # Affiche les scores
        elif choice == "Options":
            print("Options")  # Affiche les options
        elif choice == "Quitter":
            pygame.quit()  # Ferme la fenêtre
            sys.exit()


def pause_menu():
    options = ["Reprendre", "Sauvegarder la partie", "Options", "Menu principal"]
    return draw_menu("- Pause -", options, transparent=True)


if __name__ == "__main__":
    main_menu()

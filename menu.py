import pygame
import sys
import game
import score_db
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

# Options de menu
options = ["Nouvelle Partie", "Meilleurs Scores", "Options", "Quitter"]
selected_option = 0  # Option actuellement sélectionnée

def draw_menu():
    screen.fill(WHITE)
    title = font.render("Menu", True, BLACK)
    screen.blit(title, (TAILLE_FENETRE // 2 - title.get_width() // 2, 50))

    for i, option in enumerate(options):
        color = SELECTED if i == selected_option else BLACK
        option_text = font.render(option, True, color)
        screen.blit(option_text, (TAILLE_FENETRE // 2 - option_text.get_width() // 2, 150 + i * 40))

    pygame.display.flip()

def show_scores():
    screen.fill(WHITE)
    title = font.render("Meilleurs Scores", True, BLACK)
    screen.blit(title, (TAILLE_FENETRE // 2 - title.get_width() // 2, 50))

    # Affiche les meilleurs scores depuis la base de données
    top_scores = score_db.get_top_scores()
    for i, (name, score) in enumerate(top_scores, start=1):
        score_text = font.render(f"{i}. {name} - {score} points", True, BLACK)
        screen.blit(score_text, (TAILLE_FENETRE // 2 - score_text.get_width() // 2, 100 + i * 30))

    pygame.display.flip()

    # Attend un appui sur une touche pour revenir au menu principal
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                waiting = False  # Quitte l'affichage des scores si une touche est pressée

def main_menu():
    global selected_option
    running = True

    while running:
        draw_menu()

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
                    if options[selected_option] == "Nouvelle Partie":
                        game.run_game()  # Lance le jeu en appelant une fonction run_game dans game.py
                    elif options[selected_option] == "Meilleurs Scores":
                        show_scores()  # Affiche les meilleurs scores
                    elif options[selected_option] == "Quitter":
                        pygame.quit()
                        sys.exit()

if __name__ == "__main__":
    main_menu()

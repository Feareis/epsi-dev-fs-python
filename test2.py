import pygame
import sys
import game_settings as gs


def draw_size_menu():
    # Initialisation de Pygame
    pygame.init()
    screen = pygame.display.set_mode((gs.TAILLE_FENETRE, gs.TAILLE_FENETRE), pygame.RESIZABLE)
    pygame.display.set_caption("Bomberman")

    font = pygame.font.Font(None, 36)
    WHITE = gs.WHITE
    BLACK = gs.BLACK

    # Paramètres de taille initiale
    nb_line = 10
    nb_column = 10
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


# Exemple d'appel de la fonction pour obtenir la taille du plateau
if __name__ == "__main__":
    nb_line, nb_column = draw_size_menu()
    print(f"Taille choisie - Lignes: {nb_line}, Colonnes: {nb_column}")

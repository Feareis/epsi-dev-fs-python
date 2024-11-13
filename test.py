import pygame
import game_settings as gs
import plate

# Initialisation de Pygame
pygame.init()

# Configuration de la fenêtre
screen = pygame.display.set_mode((gs.TAILLE_FENETRE, gs.TAILLE_FENETRE), pygame.RESIZABLE)
pygame.display.set_caption("Test de génération aléatoire du plateau")

def main():
    # Générer un plateau aléatoire
    nb_line = 13  # Nombre de lignes du plateau
    nb_column = 13  # Nombre de colonnes du plateau
    game_plate = plate.random_plate(nb_line, nb_column)

    # Initialiser les positions des joueurs et des ennemis
    player1_position = gs.STARTING_PLAYER1_POSITION
    player2_position = gs.STARTING_PLAYER2_POSITION
    foes = [(3, 3), (5, 5), (7, 7)]  # Positions des ennemis pour le test

    # Boucle principale d'affichage
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Remplir l'écran de la couleur de fond
        screen.fill(gs.WHITE)

        # Utiliser la fonction view_plate_2p pour afficher le plateau et les personnages
        plate.view_plate_2p(screen, game_plate, player1_position, player2_position, foes)

        # Mettre à jour l'affichage
        pygame.display.flip()

    # Quitter Pygame proprement
    pygame.quit()

if __name__ == "__main__":
    main()

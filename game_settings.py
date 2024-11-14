"""
Couleurs
"""
WHITE = (255, 255, 255)          # Blanc
BLACK = (0, 0, 0)                # Noir
RED = (255, 0, 0)                # Rouge
GREEN = (0, 255, 0)              # Vert
BLUE = (0, 0, 255)               # Bleu
YELLOW = (255, 255, 0)           # Jaune
ORANGE = (255, 165, 0)           # Orange
PURPLE = (128, 0, 128)           # Violet
PINK = (255, 192, 203)           # Rose
BROWN = (139, 69, 19)            # Marron
GRAY = (128, 128, 128)           # Gris
DARK_GRAY = (64, 64, 64)         # Gris foncé
LIGHT_GRAY = (192, 192, 192)     # Gris clair
GOLD = (255, 215, 0)             # Or

COULEUR_CASE_VIDE = WHITE
COULEUR_CASE_INDESTRUCTIBLE = GRAY
COULEUR_BRIQUE_CASSABLE = BROWN
COULEUR_JOUEUR1 = GREEN
COULEUR_JOUEUR2 = BLUE
COULEUR_ENNEMI = RED
COULEUR_FOND = WHITE
COULEUR_BOMB = YELLOW

# Menu
SELECTED = BLUE


"""
Case Size
"""
TAILLE_CASE = 45  # Taille des cases du plateau


"""
Windows Size
"""
TAILLE_FENETRE = TAILLE_CASE * 13


"""
Position
"""
INITIAL_FOES_POSITIONS = [(4, 5), (5, 6), (9, 8), (3, 10)]
STARTING_PLAYER1_POSITION = (0, 0)
STARTING_PLAYER2_POSITION = (12, 12)


"""
Autre
"""
MAX_GAME_TIME = 600

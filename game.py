import plate
import player

nb_line = 13
nb_column = 13
foes = [(4, 5), (5, 6), (9, 8), (3, 11)]
game_plate = plate.starting_plate(nb_line, nb_column, bricks=[(0, 4), (4, 6), (11, 13), (2, 7), (2, 7)])
player_position = (0, 0)  # Position initiale du joueur


run = True
while run:
    plate.view_plate(game_plate, player_position, foes)
    direction = input("Déplacer (z=haut, s=bas, q=gauche, d=droite, b=bombe) : ").lower()

    if direction in ["z", "s", "q", "d"]:
        player_position = player.move_player(player_position, direction, game_plate)
        if player.check_collision(player_position, foes):
            print("Perdu !")
            run = False
    print("\n")

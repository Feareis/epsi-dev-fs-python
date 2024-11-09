import plate
import player

nb_line = 13
nb_column = 13
game_plate = plate.starting_plate(nb_line, nb_column)
player_position = (0, 0)  # Position initiale du joueur


run = True
while run:
    plate.view_plate(game_plate, player_position)
    direction = input("Déplacer (z=haut, s=bas, q=gauche, d=droite, b=bombe) ou Quitter (e=exit) : ").lower()

    if direction in ["z", "s", "q", "d"]:
        player_position = player.move_player(player_position, direction, game_plate)
    elif direction == "e":
        run = False
    print("\n")

import time
import pygame

# Import custom modules for game functionalities
import menu
import plate
import player
import bomb
import db
import game_settings as gs

# Set the maximum game time using the constant from game settings
max_game_time = gs.MAX_GAME_TIME


def get_remaining_time(start_time, max_time):
    """
    Calculates the remaining game time based on the start time.

    :param start_time: The start time of the game (in seconds since epoch).
    :param max_time: The maximum allowed game time in seconds.
    :return: The remaining time in seconds as an integer, or 0 if the time has elapsed.
    """
    elapsed_time = time.time() - start_time  # Calculate the elapsed time since the game started
    return max(0, int(max_time - elapsed_time))  # Calculate remaining time and ensure it doesn't go below zero


def run_game_2p():
    """
    Main function to initialize and run the 2 player game loop.

    :return: None
    """

    # --- Pygame initialization and window settings ---
    pygame.init()
    screen = pygame.display.set_mode((gs.WINDOW_SIZE, gs.WINDOW_SIZE), pygame.RESIZABLE)
    pygame.display.set_caption("Bomberman")  # Game window title
    font = pygame.font.Font(None, 36)  # Font for displaying score and time

    # --- Database initialization ---
    db.initialize_scores_db()

    # --- Game parameters ---
    board_height, board_width = 13, 13  # Game board dimensions (number of rows and columns)
    enemy_positions = gs.INITIAL_ENEMY_POSITIONS  # Initial enemy positions
    game_plate = plate.random_plate(board_height, board_width)  # Random game board setup

    # Initial positions and scores
    player1_position = gs.STARTING_PLAYER1_POSITION  # Starting position for player 1
    player2_position = (board_height - 1, board_width - 1)  # Starting position for player 2
    score_j1, score_j2 = 1000, 1000  # Initial scores for both players

    # Player status and timing parameters
    player1_live, player2_live = True, True
    score_decrement = 1  # Points deducted per move
    enemy_move_delay = 1000  # Enemy movement delay in milliseconds
    last_enemy_move = pygame.time.get_ticks()  # Track last enemy move time
    start_time = time.time()  # Start time for the game

    # --- Main game loop ---
    run = True
    while run:
        # --- Event handling ---
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False  # Exit if window is closed

            elif event.type == pygame.KEYDOWN:
                # Pause menu
                if event.key == pygame.K_ESCAPE:
                    choice = menu.display_2p_pause_menu()
                    if choice == "Resume":
                        continue
                    elif choice == "Options":
                        menu.display_options_menu(game_mode="game_2p")
                    elif choice == "Main Menu":
                        run = False  # Exit to main menu without saving

                keys = pygame.key.get_pressed()

                # Player 1 movement
                if keys[pygame.K_z]:
                    player1_position = player.move_player(player1_position, "z", game_plate, 1, player2_position=player2_position)
                    score_j1 -= score_decrement
                elif keys[pygame.K_s]:
                    player1_position = player.move_player(player1_position, "s", game_plate, 1, player2_position=player2_position)
                    score_j1 -= score_decrement
                elif keys[pygame.K_q]:
                    player1_position = player.move_player(player1_position, "q", game_plate, 1, player2_position=player2_position)
                    score_j1 -= score_decrement
                elif keys[pygame.K_d]:
                    player1_position = player.move_player(player1_position, "d", game_plate, 1, player2_position=player2_position)
                    score_j1 -= score_decrement
                if keys[pygame.K_e]:  # Player 1 places a bomb
                    bomb.add_bomb(player1_position)

                # Player 2 movement
                if keys[pygame.K_o]:
                    player2_position = player.move_player(player2_position, "o", game_plate, 2, player2_position=player1_position)
                    score_j2 -= score_decrement
                elif keys[pygame.K_l]:
                    player2_position = player.move_player(player2_position, "l", game_plate, 2, player2_position=player1_position)
                    score_j2 -= score_decrement
                elif keys[pygame.K_k]:
                    player2_position = player.move_player(player2_position, "k", game_plate, 2, player2_position=player1_position)
                    score_j2 -= score_decrement
                elif keys[pygame.K_m]:
                    player2_position = player.move_player(player2_position, "m", game_plate, 2, player2_position=player1_position)
                    score_j2 -= score_decrement
                if keys[pygame.K_i]:  # Player 2 places a bomb
                    bomb.add_bomb(player2_position)

        # --- Collision checks ---
        player1_live, player2_live = player.check_player_collision_2p(player1_position, player2_position, enemy_positions, player1_live, player2_live)
        if player.check_game_end(player1_live, player2_live):
            print("Collective defeat !")
            run = False


        # --- Enemy movement timing ---
        current_time = pygame.time.get_ticks()
        if current_time - last_enemy_move > enemy_move_delay:
            enemy_positions = player.update_foes_positions_2p(player1_position, player2_position, enemy_positions, game_plate, player1_live, player2_live)
            last_enemy_move = current_time
            player1_live, player2_live = player.check_player_collision_2p(player1_position, player2_position, enemy_positions, player1_live, player2_live)
            if player.check_game_end(player1_live, player2_live):
                print("Collective defeat !")
                run = False

        # --- Draw game board and elements ---
        screen.fill(gs.COLOR_BACKGROUND)  # Background color
        plate.view_plate_2p(screen, game_plate, player1_position, player2_position, enemy_positions, player1_live, player2_live)

        # Victory conditions
        if not enemy_positions:
            if not player1_live:
                print("Victory for player 2 !")
            elif not player2_live:
                print("Victory for player 1 !")
            run = False

        # --- Time handling ---
        remaining_time = get_remaining_time(start_time, max_game_time)
        if remaining_time <= 0:
            print("Draw !")
            run = False
        minutes, seconds = divmod(remaining_time, 60)

        # Display remaining time at the top left
        time_display = font.render(f"Temps : {minutes:02d}:{seconds:02d}", True, gs.BLACK)
        screen.blit(time_display, (10, 10))

        # --- Bomb updates ---
        if bomb.update_bombs(screen, game_plate, enemy_positions, player1_position, board_height, board_width):
            player1_live = False
        if bomb.update_bombs(screen, game_plate, enemy_positions, player2_position, board_height, board_width):
            player2_live = False

        # --- Update Pygame display ---
        pygame.display.flip()

    # --- Clean up resources after the game loop ---
    pygame.quit()  # Clean up Pygame resources

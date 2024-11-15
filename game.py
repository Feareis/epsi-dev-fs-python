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


def run_game(load_saved=False):
    """
    Main function to initialize and run the game loop.

    :param load_saved: Boolean indicating if a saved game state should be loaded (default is False).
    :return: None
    """

    # --- Pygame initialization and window settings ---
    pygame.init()
    screen = pygame.display.set_mode((gs.WINDOW_SIZE, gs.WINDOW_SIZE), pygame.RESIZABLE)
    pygame.display.set_caption("Bomberman")  # Game window title
    font = pygame.font.Font(None, 36)  # Font for displaying score and time

    # --- Database initialization ---
    db.initialize_scores_db()
    db.initialize_game_db()

    # --- Game parameters and board setup ---
    if load_saved:
        loaded_game = db.load_game()
        if loaded_game:
            player_position, enemy_positions, score, board_height, board_width, board = loaded_game
        else:
            return  # End if no saved game is found
    else:
        board_height, board_width = menu.display_size_menu() # Board dimensions (number of rows and columns)
        enemy_positions = gs.INITIAL_ENEMY_POSITIONS  # Initial enemy positions
        board = plate.generate_random_board(board_height, board_width)  # Random game board
        player_position = gs.STARTING_PLAYER1_POSITION  # Initial player position
        score = 1000  # Initial player score

    # --- Timing parameters ---
    start_time = time.time()  # Game start time
    score_decrement = 1  # Score decrement per move
    enemy_move_delay = 1000  # Delay in milliseconds for enemy movement
    last_enemy_move_time = pygame.time.get_ticks()  # Last enemy movement tick initialization

    # --- Main game loop ---
    run = True
    while run:
        # --- Pygame event handling ---
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False  # Exit loop if the window is closed

            elif event.type == pygame.KEYDOWN:
                # Pause menu and options
                if event.key == pygame.K_ESCAPE:
                    choice = menu.display_1p_pause_menu()

                    if choice == "Resume":
                        continue  # Continue game without changes
                    elif choice == "Save Game":
                        db.save_single_game_state(player_position, enemy_positions, score, board_height, board_width, board)
                        run = False  # Exit after saving
                    elif choice == "Options":
                        menu.display_options_menu(game_mode="game")
                    elif choice == "Main Menu":
                        run = False  # Exit to the main menu without saving

                # Player movement
                elif event.key in [pygame.K_z, pygame.K_s, pygame.K_q, pygame.K_d]:
                    direction = event.unicode  # Get the direction from key press
                    new_position = player.move_player(player_position, direction, board)

                    # Verify that move_player returns a valid position before updating
                    if new_position:
                        player_position = new_position
                        score -= score_decrement  # Decrease score with each move

                # Place a bomb
                elif event.key == pygame.K_b:
                    bomb.add_bomb(player_position)  # Place a bomb at the player's position

        # --- Collision checks and game-over conditions ---
        if player.check_player_collision(player_position, enemy_positions):
            print("Defeated !")
            run = False

        # --- Enemy movement after delay ---
        ct = pygame.time.get_ticks()
        if ct - last_enemy_move_time > enemy_move_delay:
            enemy_positions = player.update_foes_positions(player_position, enemy_positions, board)
            last_enemy_move_time = ct
            if player.check_player_collision(player_position, enemy_positions):
                print("Defeated !")
                run = False

        # --- Drawing the board elements ---
        screen.fill(gs.COLOR_BACKGROUND)  # Background color
        plate.view_board(screen, board, enemy_positions, player_position)  # Draw the game board with player and enemies

        # --- Victory condition ---
        if not enemy_positions:
            print("Victory !")
            db.end_game_and_save_score(score)
            run = False

        # --- Remaining time management ---
        remaining_time = get_remaining_time(start_time, max_game_time)
        if remaining_time <= 0:
            print("Defeated !")
            run = False
        minutes, seconds = divmod(remaining_time, 60)  # Convert remaining time to minutes and seconds

        # Display remaining time at the top right
        time_display = font.render(f"Temps : {minutes:02d}:{seconds:02d}", True, gs.BLACK)
        screen.blit(time_display, ((gs.WINDOW_SIZE // 2) + 20, 10))

        # --- Display score ---
        if score > 0:
            score_text = font.render(f"Score: {score}", True, gs.BLACK)
            screen.blit(score_text, (10, 10))  # Display at the top left
        else:
            print("Defeated !")
            run = False

        # --- Bomb handling ---
        if bomb.update_bombs(screen, board, enemy_positions, player_position, board_height, board_width):
            print("Defeated !")
            run = False

        # --- Update Pygame display ---
        pygame.display.flip()

    # --- Clean up resources after the game loop ---
    pygame.quit()  # Clean up Pygame resources

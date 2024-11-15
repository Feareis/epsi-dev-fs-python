import pygame
import sys

# Import custom modules for game functionalities
import game
import game_2p
import db
import game_settings as gs


# --- Pygame Initialization and Configuration ---
pygame.init()
screen = pygame.display.set_mode((gs.WINDOW_SIZE, gs.WINDOW_SIZE))
font = pygame.font.Font(None, 36)
WHITE = gs.WHITE
BLACK = gs.BLACK


# --- Menu Functions ---
def display_menu(title, options):
    """
    Displays a menu with a title and a list of selectable options, allowing
    the user to navigate through options with UP and DOWN keys and select with ENTER.

    :param title: The title displayed at the top of the menu (str).
    :param options: A list of menu options (str) to display. Use a single space " " for empty options.
    :return: The selected option as a string when ENTER is pressed.
    """
    selected_option = 0

    def get_next_valid_option(current, direction):
        """
        Adjusts the selection index to skip over empty options.

        :param current: The current index of the selection (int).
        :param direction: The direction to move in the options list (int, 1 for down, -1 for up).
        :return: The adjusted index pointing to a non-empty option (int).
        """
        while options[current] == " ":
            current = (current + direction) % len(options)
        return current

    while True:
        # Check if the screen surface is still available
        if not pygame.display.get_surface():
            quit_game()
            return None  # Exit the menu if the display surface is quit

        # Clear screen and render title
        screen.fill(WHITE)
        title_text = font.render(title, True, BLACK)
        screen.blit(title_text, (gs.WINDOW_SIZE // 2 - title_text.get_width() // 2, 50))

        # Display each option, highlighting the selected one
        for i, option in enumerate(options):
            if option == " ":
                continue  # Skip empty options
            color = gs.MENU_SELECTED if i == selected_option else BLACK
            option_text = font.render(option, True, color)
            screen.blit(option_text, (gs.WINDOW_SIZE // 2 - option_text.get_width() // 2, 150 + i * 40))

        pygame.display.flip()

        # Event handling for menu navigation
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    selected_option = get_next_valid_option((selected_option - 1) % len(options), -1)
                elif event.key == pygame.K_DOWN:
                    selected_option = get_next_valid_option((selected_option + 1) % len(options), 1)
                elif event.key == pygame.K_RETURN:
                    return options[selected_option]  # Return the selected option


def display_high_scores():
    """
    Displays the top high scores from the database on the screen.
    Allows the user to return to the main menu by pressing any key.

    :return: None
    """
    screen.fill(WHITE)

    # Render the title for the scores display
    title = font.render("- High Scores (Solo Only) -", True, BLACK)
    screen.blit(title, (gs.WINDOW_SIZE // 2 - title.get_width() // 2, 50))

    # Fetch and display top scores from the database
    top_scores = db.get_top_player_scores()
    for i, (name, score) in enumerate(top_scores, start=1):
        score_text = font.render(f"{i}. {name} - {score} points", True, BLACK)
        y_position = 100 + i * 30
        screen.blit(score_text, (gs.WINDOW_SIZE // 2 - score_text.get_width() // 2, y_position))

    pygame.display.flip()

    # Wait for any key press to return to the main menu
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                waiting = False  # Exit scores display on any key press


def display_main_menu():
    """
    Displays the main menu and handles user selections.

    The options include:
    - "New game": Opens the new game menu
    - "Load game": Opens the load game menu
    - "Top scores": Displays the high scores
    - "Options": Opens the options menu (if available)
    - "Exit": Exits the game

    :return: None
    """
    while True:
        choice = display_menu("- Menu -", gs.MAIN_MENU_OPTIONS)
        if choice == gs.MENU_NEW_GAME_OPTION:
            display_new_game_menu()  # Redirects to the new game menu
        elif choice == gs.MENU_LOAD_GAME_OPTION:
            display_load_game_menu()  # Opens the load game menu
        elif choice == gs.MENU_HIGH_SCORES_OPTION:
            display_high_scores()  # Displays high scores
        elif choice == gs.MENU_OPTIONS_OPTION:
            display_options_menu()  # Opens options menu
        elif choice == gs.MENU_QUIT_OPTION:
            quit_game()  # Cleanly exits the game


def quit_game():
    """
    Exits Pygame and closes the program.

    :return: None
    """
    pygame.quit()
    sys.exit()


def display_1p_pause_menu():
    """
    Displays the pause menu for single-player mode and allows the player to choose an action.

    The options include:
    - Resume: Continues the current game.
    - Save game: Saves the current game state.
    - Options: Opens the game options menu.
    - Main Menu: Returns to the main menu, exiting the current game.

    :return: The selected option as a string.
    """
    return display_menu("- Pause -", gs.SOLO_PAUSE_MENU)


def display_2p_pause_menu():
    """
    Displays the pause menu for multiplayer mode, allowing players to choose an action.

    The options include:
    - Resume: Continues the multiplayer game.
    - Options: Opens the options menu (e.g., for keybindings).
    - Main Menu: Returns to the main menu, ending the current multiplayer session.

    :return: The selected option as a string.
    """
    return display_menu("- Pause -", gs.MULTI_PAUSE_MENU)


def display_new_game_menu():
    """
    Displays the "New Game" menu, allowing the player to choose between single-player and multiplayer modes.

    The options include:
    - Solo player game: Starts a new single-player game.
    - Multi player game: Starts a new multiplayer game.
    - Main Menu: Returns to the main menu without starting a new game.

    :return: None
    """
    choice = display_menu("- New Game -", gs.NEW_GAME_MENU)
    if choice == gs.MENU_SOLO_PLAYER_GAME:
        game.run_game()
    elif choice == gs.MENU_MULTI_PLAYER_GAME:
        game_2p.run_game_2p()  # Launches the multiplayer module
    elif choice == gs.MENU_MAIN_MENU_OPTION:
        return  # Returns to the main menu without starting a new game


def display_load_game_menu():
    """
    Displays the "Load Game" menu, allowing the player to load a previously saved game.

    The options include:
    - Solo - Load game: Loads a saved single-player game.
    - Main Menu: Returns to the main menu without loading a game.

    :return: None
    """
    choice = display_menu("- Load Game -", gs.LOAD_GAME_MENU)

    if choice == gs.MENU_LOAD_SOLO_PLAYER_GAME:
        game.run_game(load_saved=True)  # Loads a saved single-player game
    elif choice == gs.MENU_MAIN_MENU_OPTION:
        return  # Returns to the main menu without starting a new game


def display_options_menu(game_mode="game"):
    """
    Displays the options menu, allowing the player to configure settings such as language and keybindings.

    The options include:
    - Language: Opens the language settings (not yet implemented).
    - Keybindings: Opens the keybinding configuration (not yet implemented).
    - Back: Returns to the appropriate pause menu based on the game mode (single-player or multiplayer).

    :param game_mode: Specifies the game mode context ("game" for single-player or "game_2p" for multiplayer),
                      to return to the correct pause menu.
    :return: None
    """
    choice = display_menu("- Options -", gs.OPTION_MENU)

    if choice == gs.MENU_LANGUAGES_OPTION:
        print("Languages")  # Placeholder for language settings
    elif choice == gs.MENU_KEYBINDING_OPTION:
        print("Keybindings")  # Placeholder for keybinding settings
    elif choice == gs.MENU_BACK_OPTION:
        # Returns to the appropriate pause menu based on the game mode
        if game_mode == "game":
            return display_1p_pause_menu()  # Returns to the single-player pause menu
        elif game_mode == "game_2p":
            return display_2p_pause_menu()  # Returns to the multiplayer pause menu


def display_size_menu():
    """
    Displays the size selection menu for the game board, allowing the player to adjust
    the number of rows (lines) and columns using arrow keys.

    The options include:
    - UP/DOWN arrows: Increase or decrease the number of rows or columns, depending on the selection.
    - LEFT/RIGHT arrows: Switch between adjusting rows (lines) or columns.
    - ENTER: Confirm the selection and return the chosen board size.

    :return: A tuple (board_height, board_width) representing the selected number of rows and columns.
    """
    # --- Pygame initialization and window settings ---
    pygame.init()
    pygame.display.set_caption("Bomberman")

    # Initial board size parameters
    board_height, board_width = 13, 13
    selected = gs.MENU_HEIGHT_OPTION  # Defines if adjusting rows or columns

    while True:
        screen.fill(WHITE)

        # Display title
        title_text = font.render("- Board Size -", True, BLACK)
        screen.blit(title_text, (gs.WINDOW_SIZE // 2 - title_text.get_width() // 2, 50))

        # Highlight colors for selection
        height_color = gs.MENU_SELECTED if selected == gs.MENU_HEIGHT_OPTION else BLACK
        width_color = gs.MENU_SELECTED if selected == gs.MENU_WIDTH_OPTION else BLACK

        # Render lines and columns text with respective colors
        line_text = font.render(f"Lines: {board_height}", True, height_color)
        column_text = font.render(f"Columns: {board_width}", True, width_color)

        # Position elements for side-by-side display
        line_text_x = (gs.WINDOW_SIZE // 2) - line_text.get_width() - 20
        column_text_x = (gs.WINDOW_SIZE // 2) + 20

        screen.blit(line_text, (line_text_x, 150))
        screen.blit(column_text, (column_text_x, 150))

        # Display instructions
        instructions_text = font.render("[Enter] to confirm your entry", True, BLACK)
        screen.blit(instructions_text, (gs.WINDOW_SIZE // 2 - instructions_text.get_width() // 2, 300))

        pygame.display.flip()

        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                # Adjust number of rows or columns
                if event.key == pygame.K_UP:
                    if selected == gs.MENU_HEIGHT_OPTION:
                        board_height += 1
                    elif selected == gs.MENU_WIDTH_OPTION:
                        board_width += 1
                elif event.key == pygame.K_DOWN:
                    if selected == gs.MENU_HEIGHT_OPTION:
                        board_height -= 1
                    elif selected == gs.MENU_WIDTH_OPTION:
                        board_width -= 1
                elif event.key == pygame.K_RIGHT:
                    selected = gs.MENU_WIDTH_OPTION if selected == gs.MENU_HEIGHT_OPTION else selected  # Switch to columns
                elif event.key == pygame.K_LEFT:
                    selected = gs.MENU_HEIGHT_OPTION if selected == gs.MENU_WIDTH_OPTION else selected  # Switch to lines
                elif event.key == pygame.K_RETURN:
                    return board_height, board_width  # Return the selected board size


if __name__ == "__main__":
    display_main_menu()

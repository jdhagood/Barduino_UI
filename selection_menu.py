import curses

def make_selection_menu(header, menu_options):
    """
    Creates a menu UI with the provided header and menu options.
    
    Args:
        header (str): The header text displayed at the top of the menu.
        menu_options (list): A list of tuples where each tuple contains a menu label (str)
                             and a function to call (function) when that option is selected.

    Returns:
        function: A function that displays the menu in a `curses` window.
    """
    def menu_function(stdscr):
        # Initialize colors
        curses.init_pair(1, curses.COLOR_RED, curses.COLOR_BLACK)
        curses.init_pair(2, curses.COLOR_GREEN, curses.COLOR_BLACK)
        curses.init_pair(3, curses.COLOR_BLACK, curses.COLOR_GREEN)

        RED_AND_BLACK = curses.color_pair(1)
        GREEN_AND_BLACK = curses.color_pair(2)
        BLACK_AND_GREEN = curses.color_pair(3)

        # Dimensions for the options window
        menu_height = 2
        for (option, _) in menu_options:
            menu_height += 1 + option.count("\n")
        menu_width = max(len(item[0]) for item in menu_options) + 4  # +4 for padding
        start_y, start_x = header.count("\n") + 1, 1  # Position of the menu
        options_win = curses.newwin(menu_height, menu_width, start_y, start_x)

        current_row = 0

        while True:
            # Clear and refresh the main screen
            stdscr.clear()
            stdscr.addstr(header + "\n", RED_AND_BLACK)
            stdscr.refresh()

            # Draw menu options inside the options window
            options_win.clear()
            returns = 0
            for i, (label, _) in enumerate(menu_options):
                if i == current_row:
                    options_win.addstr(i + 1 + returns, 1, label, BLACK_AND_GREEN)  # Highlight current row
                else:
                    options_win.addstr(i + 1 + returns, 1, label, GREEN_AND_BLACK)  # Normal text
                returns += label.count("\n")
            options_win.box()
            options_win.refresh()

            # Handle key input
            key = stdscr.getch()
            if key == curses.KEY_UP and current_row > 0:
                current_row -= 1
            elif key == curses.KEY_DOWN and current_row < len(menu_options) - 1:
                current_row += 1
            elif key == ord("\n"):  # Enter key
                should_exit = menu_options[current_row][1](stdscr)
                if should_exit:  # Exit if the selected function returns True
                    return False

    return menu_function
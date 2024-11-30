import curses
import time

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
        menu_height = len(menu_options) + 2  # +2 for padding inside the box
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
            for i, (label, _) in enumerate(menu_options):
                if i == current_row:
                    options_win.addstr(i + 1, 1, label, BLACK_AND_GREEN)  # Highlight current row
                else:
                    options_win.addstr(i + 1, 1, label, GREEN_AND_BLACK)  # Normal text
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

def make_info_window(header, content):
    """
    Creates an info window with scrollable content and a back button.

    Args:
        header (str): The header text displayed at the top of the info window.
        content (str): The content to display in the info window.

    Returns:
        function: A function that displays the info window in a `curses` window.
    """
    def info_function(stdscr):
        # Initialize colors
        curses.init_pair(1, curses.COLOR_RED, curses.COLOR_BLACK)
        curses.init_pair(2, curses.COLOR_WHITE, curses.COLOR_BLACK)

        RED_AND_BLACK = curses.color_pair(1)
        WHITE_AND_BLACK = curses.color_pair(2)

        # Split content into lines for scrolling
        content_lines = content.splitlines()
        max_lines = len(content_lines)

        # Dimensions
        height, width = stdscr.getmaxyx()
        content_height = height - 4  # Reserve space for header and instructions
        start_row = 0  # Scrolling start position

        while True:
            # Clear and refresh the screen
            stdscr.clear()
            stdscr.addstr(0, 0, header, RED_AND_BLACK)
            stdscr.addstr(2, 0, "Use UP/DOWN to scroll, 'b' to go back.", WHITE_AND_BLACK)

            # Display content lines within the scroll range
            for i in range(content_height):
                line_index = start_row + i
                if line_index < max_lines:
                    stdscr.addstr(4 + i, 0, content_lines[line_index][:width - 1])  # Clip to window width

            stdscr.refresh()

            # Handle user input
            key = stdscr.getch()
            if key == curses.KEY_UP and start_row > 0:
                start_row -= 1
            elif key == curses.KEY_DOWN and start_row < max_lines - content_height:
                start_row += 1
            elif key == ord('b'):  # Back button
                return  False # Return to the caller (main menu)

    return info_function

def drink_making_menu(stdscr):
    """
    Menu for making a new drink with:
    - Enter Name: Name input stays on the main screen and blinks when selected.
    - Sliding bars for six ingredients, adjustable from 0% to 100%.
    - Save and Exit options.
    """
    # Initialize colors
    curses.init_pair(1, curses.COLOR_RED, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_GREEN, curses.COLOR_BLACK)
    curses.init_pair(3, curses.COLOR_GREEN, curses.COLOR_WHITE)
    curses.init_pair(4, curses.COLOR_BLACK, curses.COLOR_GREEN)

    RED_AND_BLACK = curses.color_pair(1)
    GREEN_AND_BLACK = curses.color_pair(2)
    GREEN_AND_WHITE = curses.color_pair(3)
    BLACK_AND_GREEN = curses.color_pair(4)

    header = r"""
 _______             __            __              __       __            __                           
/       \           /  |          /  |            /  \     /  |          /  |                          
$$$$$$$  |  ______  $$/  _______  $$ |   __       $$  \   /$$ |  ______  $$ |   __   ______    ______  
$$ |  $$ | /      \ /  |/       \ $$ |  /  |      $$$  \ /$$$ | /      \ $$ |  /  | /      \  /      \ 
$$ |  $$ |/$$$$$$  |$$ |$$$$$$$  |$$ |_/$$/       $$$$  /$$$$ | $$$$$$  |$$ |_/$$/ /$$$$$$  |/$$$$$$  |
$$ |  $$ |$$ |  $$/ $$ |$$ |  $$ |$$   $$<        $$ $$ $$/$$ | /    $$ |$$   $$<  $$    $$ |$$ |  $$/ 
$$ |__$$ |$$ |      $$ |$$ |  $$ |$$$$$$  \       $$ |$$$/ $$ |/$$$$$$$ |$$$$$$  \ $$$$$$$$/ $$ |      
$$    $$/ $$ |      $$ |$$ |  $$ |$$ | $$  |      $$ | $/  $$ |$$    $$ |$$ | $$  |$$       |$$ |      
$$$$$$$/  $$/       $$/ $$/   $$/ $$/   $$/       $$/      $$/  $$$$$$$/ $$/   $$/  $$$$$$$/ $$/       
"""
    def return_percent_bar(num):
        """Returns a visual representation of a percentage bar."""
        return "<" + "▇" * num + (10 - num) * " " + ">"

    menu_options = [
        "Enter Name: ",
        "Amount 1: ",
        "Amount 2: ",
        "Amount 3: ",
        "Amount 4: ",
        "Amount 5: ",
        "Amount 6: ",
        "Save Drink",
        "Exit"
    ]
    name = "Unnamed"
    amounts = [0] * 6
    current_row = 0

    def show_screen(selected=False):
        """Displays the menu screen."""
        stdscr.clear()
        stdscr.addstr(header + "\n", RED_AND_BLACK)

        for i, title in enumerate(menu_options):
            line = title
            if title.startswith("Amount"):
                index = int(title.split()[1][0]) - 1
                line += return_percent_bar(amounts[index])
            elif title == "Enter Name: ":
                line += name

            if i == current_row:
                if selected:
                    stdscr.addstr(line + "\n", GREEN_AND_WHITE)
                else:
                    stdscr.addstr(line + "\n", BLACK_AND_GREEN)  # Highlight current row
            else:
                stdscr.addstr(line + "\n", GREEN_AND_BLACK)

        stdscr.refresh()

    def input_name():
        """Allows the user to type a name directly on the menu."""
        nonlocal name
        curses.curs_set(1)  # Show the cursor
        name = ""
        while True:
            show_screen(selected=True)  # Blink background while editing
            key = stdscr.getch()
            if key == ord('\n'):  # Finish editing on Enter
                break
            elif key == 127 or key == curses.KEY_BACKSPACE:  # Handle backspace
                name = name[:-1]
            elif key >= 32 and key <= 126:  # Printable ASCII
                name += chr(key)
        show_screen()
        curses.curs_set(0)  # Hide the cursor

    def set_amount(index):
        """Adjust the percentage for a specific amount bar."""
        while True:
            show_screen(selected=True)
            key = stdscr.getch()
            if key == curses.KEY_UP and amounts[index] < 10:
                amounts[index] += 1
            elif key == curses.KEY_DOWN and amounts[index] > 0:
                amounts[index] -= 1
            elif key == ord('\n'):  # Exit adjustment mode
                break

    while True:
        show_screen()
        key = stdscr.getch()

        if key == curses.KEY_UP and current_row > 0:
            current_row -= 1
        elif key == curses.KEY_DOWN and current_row < len(menu_options) - 1:
            current_row += 1
        elif key == ord('\n'):  # Select the current option
            if current_row == 0:  # Enter Name
                input_name()
            elif 1 <= current_row <= 6:  # Adjust Amount bars
                set_amount(current_row - 1)
            elif current_row == 7:  # Save Drink
                # Add saving logic here
                stdscr.clear()
                stdscr.addstr("Drink saved!\nPress any key to return to the menu.", GREEN_AND_BLACK)
                stdscr.getch()
            elif current_row == 8:  # Exit
                break

    curses.endwin()


# ASCII header
header = r"""
 _______                             __            __                     
/       \                           /  |          /  |                    
$$$$$$$  |  ______    ______    ____$$ | __    __ $$/  _______    ______  
$$ |__$$ | /      \  /      \  /    $$ |/  |  /  |/  |/       \  /      \ tm
$$    $$<  $$$$$$  |/$$$$$$  |/$$$$$$$ |$$ |  $$ |$$ |$$$$$$$  |/$$$$$$  |
$$$$$$$  | /    $$ |$$ |  $$/ $$ |  $$ |$$ |  $$ |$$ |$$ |  $$ |$$ |  $$ |
$$ |__$$ |/$$$$$$$ |$$ |      $$ \__$$ |$$ \__$$ |$$ |$$ |  $$ |$$ \__$$ |
$$    $$/ $$    $$ |$$ |      $$    $$ |$$    $$/ $$ |$$ |  $$ |$$    $$/ 
$$$$$$$/   $$$$$$$/ $$/        $$$$$$$/  $$$$$$/  $$/ $$/   $$/  $$$$$$/                                                                      
"""

# Menu options
start_menu = make_selection_menu("Start", [
    ["Start", lambda _: 0],
    ["Back", lambda _: 1]
])

info_menu = make_info_window("INFO", "This is information about the Barduino.")

main_menu = make_selection_menu(header, [
    ["Start", start_menu],
    ["Make New Drink", drink_making_menu],
    ["Info", info_menu],
    ["Exit", lambda _: True]
])

def main(stdscr):
    curses.curs_set(0)  # Hide cursor
    main_menu(stdscr)

if __name__ == "__main__":
    curses.wrapper(main)

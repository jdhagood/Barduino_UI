import curses
import save_and_load

import curses

def saved_drink_editing_menu(stdscr):
    """
    Menu for editing drinks using curses.
    """
    # Initialize color pairs
    curses.init_pair(1, curses.COLOR_RED, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_GREEN, curses.COLOR_BLACK)
    curses.init_pair(3, curses.COLOR_GREEN, curses.COLOR_WHITE)
    curses.init_pair(4, curses.COLOR_BLACK, curses.COLOR_GREEN)

    RED_AND_BLACK = curses.color_pair(1)
    GREEN_AND_BLACK = curses.color_pair(2)
    GREEN_AND_WHITE = curses.color_pair(3)
    BLACK_AND_GREEN = curses.color_pair(4)

    header = "Drink Editing Menu"
    drinks_and_amounts = []
    current_row = 0

    def make_menu_options():
        """
        Generates menu options from drinks and liquids.
        """
        drinks_and_amounts.clear()
        drinks = save_and_load.load_drinks()
        liquids = save_and_load.load_liquids()

        if not drinks:
            return ["No drinks found. Press 'Back' to return."]
        
        menu_options = ["Back"]
        for drink_name, amounts in drinks.items():
            drinks_and_amounts.append([drink_name, amounts])
            title = f"{drink_name}\n"
            for liquid, amount in zip(liquids, amounts):
                bar = f"<{'▇' * amount + ' ' * (10 - amount)}>"
                title += f"  {liquid}: {bar}\n"
            menu_options.append(title.strip())
        return menu_options

    def show_screen():
        """
        Displays the menu screen.
        """
        stdscr.clear()
        stdscr.addstr(f"{header.center(curses.COLS)}\n", RED_AND_BLACK)
        stdscr.addstr("-" * curses.COLS + "\n", GREEN_AND_BLACK)

        for i, line in enumerate(menu_options):
            if i == current_row:
                stdscr.addstr(line + "\n", BLACK_AND_GREEN)  # Highlight the current row
            else:
                stdscr.addstr(line + "\n", GREEN_AND_BLACK)

        stdscr.refresh()

    # Initialize menu
    menu_options = make_menu_options()

    while True:
        show_screen()
        key = stdscr.getch()

        if key == curses.KEY_UP and current_row > 0:
            current_row -= 1
        elif key == curses.KEY_DOWN and current_row < len(menu_options) - 1:
            current_row += 1
        elif key == ord('\n'):  # Enter key
            if current_row == 0:  # "Back" selected
                return  # Exit the menu
            elif len(drinks_and_amounts) > 0:  # Ensure valid drink selection
                drink_name, amounts = drinks_and_amounts[current_row - 1]
                drink_making_menu(stdscr, drink_name, amounts)
                # Refresh menu after potential changes
                menu_options = make_menu_options()
                current_row = 0

    

def liquid_editing_menu(stdscr):
    """
    Menu for editing liquid names
    """
    curses.init_pair(1, curses.COLOR_RED, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_GREEN, curses.COLOR_BLACK)
    curses.init_pair(3, curses.COLOR_GREEN, curses.COLOR_WHITE)
    curses.init_pair(4, curses.COLOR_BLACK, curses.COLOR_GREEN)

    RED_AND_BLACK = curses.color_pair(1)
    GREEN_AND_BLACK = curses.color_pair(2)
    GREEN_AND_WHITE = curses.color_pair(3)
    BLACK_AND_GREEN = curses.color_pair(4)

    header = r"Liquid Editing Menu"
    liquids = save_and_load.load_liquids()
    menu_options = [f"Liquid {n}: " for n in range(len(liquids))] + ["Save & Exit"]

    current_row = 0
    def show_screen(selected=False):
        """Displays the menu screen."""
        stdscr.clear()
        stdscr.addstr(header + "\n", RED_AND_BLACK)

        for i, title in enumerate(menu_options):
            line = title
            if i < len(liquids):
                line += liquids[i]

            if i == current_row:
                if selected:
                    stdscr.addstr(line + "\n", GREEN_AND_WHITE)
                else:
                    stdscr.addstr(line + "\n", BLACK_AND_GREEN)  # Highlight current row
            else:
                stdscr.addstr(line + "\n", GREEN_AND_BLACK)

        stdscr.refresh()
    
    def input_drink_name(index):
        """Allows the user to type a name directly on the menu."""
        liquids[index] = ""
        while True:
            show_screen(selected=True)  # Blink background while editing
            key = stdscr.getch()
            if key == ord('\n'):  # Finish editing on Enter
                break
            elif key == 127 or key == curses.KEY_BACKSPACE:  # Handle backspace
                liquids[index] = liquids[index][:-1]
            elif key >= 32 and key <= 126:  # Printable ASCII
                liquids[index] += chr(key)
        show_screen()
    
    while True:
        show_screen()
        key = stdscr.getch()

        if key == curses.KEY_UP and current_row > 0:
            current_row -= 1
        elif key == curses.KEY_DOWN and current_row < len(menu_options) - 1:
            current_row += 1
        elif key == ord('\n'):  # Select the current option
            if current_row == len(menu_options) -1: #exit
                save_and_load.save_liquids(liquids)
                return False
            else:
                input_drink_name(current_row)


        


def drink_making_menu(stdscr, name = "Unnamed", amounts = [0] * 6):
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
    liquids = save_and_load.load_liquids()
    menu_options = ["Enter Name: "] + [liquid + ": " for liquid in liquids] + ["Save Drink", "Delete/Exit"]
    current_row = 0

    def show_screen(selected=False):
        """Displays the menu screen."""
        stdscr.clear()
        stdscr.addstr(header + "\n", RED_AND_BLACK)

        for i, title in enumerate(menu_options):
            line = title
            if 1 <= i and i <=6:
                line += return_percent_bar(amounts[i - 1])
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
                save_and_load.add_drink(name, amounts)
                break #return to the previous menu
            elif current_row == 8:  # Exit\delete
                save_and_load.remove_drink(name)
                break

    curses.endwin()
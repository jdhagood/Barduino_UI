import curses
import save_and_load

def saved_drink_editing_menu(stdscr):
    """
    Menu for editing drinks using curses.
    """
    # Initialize colors
    curses.init_pair(1, curses.COLOR_RED, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_GREEN, curses.COLOR_BLACK)
    curses.init_pair(3, curses.COLOR_GREEN, curses.COLOR_WHITE)
    curses.init_pair(4, curses.COLOR_RED, curses.COLOR_WHITE)
    curses.init_pair(5, curses.COLOR_BLACK, curses.COLOR_GREEN)
    curses.init_pair(6, curses.COLOR_BLACK, curses.COLOR_MAGENTA)

    RED_AND_BLACK = curses.color_pair(1)
    GREEN_AND_BLACK = curses.color_pair(2)
    GREEN_AND_WHITE = curses.color_pair(3)
    RED_AND_WHITE = curses.color_pair(4)
    BLACK_AND_GREEN = curses.color_pair(5)
    BLACK_AND_MAGENTA = curses.color_pair(6)

    header = r""" ________  _______   ______  ________        _______   _______   ______  __    __  __    __   ______  
/        |/       \ /      |/        |      /       \ /       \ /      |/  \  /  |/  |  /  | /      \ 
$$$$$$$$/ $$$$$$$  |$$$$$$/ $$$$$$$$/       $$$$$$$  |$$$$$$$  |$$$$$$/ $$  \ $$ |$$ | /$$/ /$$$$$$  |
$$ |__    $$ |  $$ |  $$ |     $$ |         $$ |  $$ |$$ |__$$ |  $$ |  $$$  \$$ |$$ |/$$/  $$ \__$$/ 
$$    |   $$ |  $$ |  $$ |     $$ |         $$ |  $$ |$$    $$<   $$ |  $$$$  $$ |$$  $$<   $$      \ 
$$$$$/    $$ |  $$ |  $$ |     $$ |         $$ |  $$ |$$$$$$$  |  $$ |  $$ $$ $$ |$$$$$  \   $$$$$$  |
$$ |_____ $$ |__$$ | _$$ |_    $$ |         $$ |__$$ |$$ |  $$ | _$$ |_ $$ |$$$$ |$$ |$$  \ /  \__$$ |
$$       |$$    $$/ / $$   |   $$ |         $$    $$/ $$ |  $$ |/ $$   |$$ | $$$ |$$ | $$  |$$    $$/ 
$$$$$$$$/ $$$$$$$/  $$$$$$/    $$/          $$$$$$$/  $$/   $$/ $$$$$$/ $$/   $$/ $$/   $$/  $$$$$$/"""
    drinks_and_amounts = []
    current_row = 0

    def make_menu_options():
        """
        Generates menu options from drinks and liquids.
        """
        drinks_and_amounts.clear()
        drinks = save_and_load.load_drinks()
        liquids = save_and_load.load_liquids()
        max_liquid_name_length = max([len(liquid) for liquid in liquids])

        if not drinks:
            return ["No drinks found. Press 'Back' to return."]
        
        menu_options = []
        for drink_name, amounts in drinks.items():
            drinks_and_amounts.append([drink_name, amounts])
            title = f"{drink_name}\n"
            for liquid, amount in zip(liquids, amounts):
                bar = f"[{'■' * amount + ' ' * (10 - amount)}]"
                title += f"  {liquid}:{" "*(max_liquid_name_length - len(liquid))} {bar}\n"
            menu_options.append(title)
        menu_options += ["Back"]
        return menu_options

    def show_screen():
        """
        Displays the menu screen.
        """
        NUM_DRINKS = 3
        stdscr.clear()
        stdscr.addstr(f"{header.center(curses.COLS)}\n", RED_AND_BLACK)
        stdscr.addstr("-" * curses.COLS + "\n", GREEN_AND_BLACK)

        for i, line in enumerate(menu_options):
            if NUM_DRINKS*(current_row//NUM_DRINKS) <= i and i < NUM_DRINKS*(current_row//NUM_DRINKS) + NUM_DRINKS:
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
            if current_row == len(menu_options)-1:  # "Back" selected
                return  # Exit the menu
            elif len(drinks_and_amounts) > 0:  # Ensure valid drink selection
                drink_name, amounts = drinks_and_amounts[current_row]
                save_and_load.remove_drink(drink_name)
                new_drink_making_menu(stdscr, drink_name, amounts)
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
    curses.init_pair(4, curses.COLOR_RED, curses.COLOR_WHITE)
    curses.init_pair(5, curses.COLOR_BLACK, curses.COLOR_GREEN)
    curses.init_pair(6, curses.COLOR_BLACK, curses.COLOR_MAGENTA)

    RED_AND_BLACK = curses.color_pair(1)
    GREEN_AND_BLACK = curses.color_pair(2)
    GREEN_AND_WHITE = curses.color_pair(3)
    RED_AND_WHITE = curses.color_pair(4)
    BLACK_AND_GREEN = curses.color_pair(5)
    BLACK_AND_MAGENTA = curses.color_pair(6)

    header = r""" ________  _______   ______  ________        __        ______   ______   __    __  ______  _______    ______  
/        |/       \ /      |/        |      /  |      /      | /      \ /  |  /  |/      |/       \  /      \ 
$$$$$$$$/ $$$$$$$  |$$$$$$/ $$$$$$$$/       $$ |      $$$$$$/ /$$$$$$  |$$ |  $$ |$$$$$$/ $$$$$$$  |/$$$$$$  |
$$ |__    $$ |  $$ |  $$ |     $$ |         $$ |        $$ |  $$ |  $$ |$$ |  $$ |  $$ |  $$ |  $$ |$$ \__$$/ 
$$    |   $$ |  $$ |  $$ |     $$ |         $$ |        $$ |  $$ |  $$ |$$ |  $$ |  $$ |  $$ |  $$ |$$      \ 
$$$$$/    $$ |  $$ |  $$ |     $$ |         $$ |        $$ |  $$ |_ $$ |$$ |  $$ |  $$ |  $$ |  $$ | $$$$$$  |
$$ |_____ $$ |__$$ | _$$ |_    $$ |         $$ |_____  _$$ |_ $$ / \$$ |$$ \__$$ | _$$ |_ $$ |__$$ |/  \__$$ |
$$       |$$    $$/ / $$   |   $$ |         $$       |/ $$   |$$ $$ $$< $$    $$/ / $$   |$$    $$/ $$    $$/ 
$$$$$$$$/ $$$$$$$/  $$$$$$/    $$/          $$$$$$$$/ $$$$$$/  $$$$$$  | $$$$$$/  $$$$$$/ $$$$$$$/   $$$$$$/  
                                                                   $$$/                                      """
    liquids = save_and_load.load_liquids()
    menu_options = [f"Liquid {n}: " for n in range(len(liquids))] + ["Save & Exit"]

    current_row = 0
    def show_screen(selected=False):
        """Displays the menu screen."""
        stdscr.clear()
        stdscr.addstr(header + "\n", RED_AND_BLACK)
        stdscr.addstr("-" * curses.COLS + "\n", GREEN_AND_BLACK)

        for i, title in enumerate(menu_options):
            line = title
            if i < len(liquids):
                line += liquids[i]

            if i == current_row:
                if selected:
                    stdscr.addstr(line + "\n", BLACK_AND_MAGENTA)
                else:
                    stdscr.addstr(line + "\n", BLACK_AND_GREEN)  # Highlight current row
            else:
                stdscr.addstr(line + "\n", GREEN_AND_BLACK)

        stdscr.refresh()
    
    def input_drink_name(index):
        """Allows the user to type a name directly on the menu."""
        while True:
            show_screen(selected=True)  # Blink background while editing
            key = stdscr.getch()

            if key == ord('\n'):  # Finish editing on Enter
                break
            elif key in (127, curses.KEY_BACKSPACE, 8):  # Handle backspace (127, curses.KEY_BACKSPACE, or 8)
                if len(liquids[index]) > 0:
                    liquids[index] = liquids[index][:-1]
            elif 32 <= key <= 126:  # Printable ASCII
                liquids[index] += chr(key)

            show_screen()  # Refresh the screen to reflect updates
    
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


        


def new_drink_making_menu(stdscr, name = "", amounts = [0]*6):
    """
    Menu for making a new drink with:
    - Enter Name: Name input stays on the main screen and blinks when selected.
    - Sliding bars for six ingredients, adjustable from 0% to 100%.
    - Save and Exit options.
    """
    amounts = amounts[::]
    # Initialize colors
    curses.init_pair(1, curses.COLOR_RED, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_GREEN, curses.COLOR_BLACK)
    curses.init_pair(3, curses.COLOR_GREEN, curses.COLOR_WHITE)
    curses.init_pair(4, curses.COLOR_RED, curses.COLOR_WHITE)
    curses.init_pair(5, curses.COLOR_BLACK, curses.COLOR_GREEN)
    curses.init_pair(6, curses.COLOR_BLACK, curses.COLOR_MAGENTA)

    RED_AND_BLACK = curses.color_pair(1)
    GREEN_AND_BLACK = curses.color_pair(2)
    GREEN_AND_WHITE = curses.color_pair(3)
    RED_AND_WHITE = curses.color_pair(4)
    BLACK_AND_GREEN = curses.color_pair(5)
    BLACK_AND_MAGENTA = curses.color_pair(6)

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
        return "[" + "■" * num + (10 - num) * " " + "]"

    liquids = save_and_load.load_liquids()
    max_liquid_length = max([len(liquid) for liquid in liquids])
    menu_options = ["Enter Name: "] + [liquid + ": " + " "*(max_liquid_length-len(liquid)) for liquid in liquids] + ["Save Drink", "Delete/Exit"]
    current_row = 0

    def show_screen(selected=False):
        """Displays the menu screen."""
        stdscr.clear()
        stdscr.addstr(header + "\n", RED_AND_BLACK)
        stdscr.addstr("-" * curses.COLS + "\n", GREEN_AND_BLACK)
        for i, title in enumerate(menu_options):
            line = title
            if 1 <= i and i <=6:
                line += return_percent_bar(amounts[i - 1])
            elif title == "Enter Name: ":
                line += name

            if i == current_row:
                if selected:
                    stdscr.addstr(line + "\n", BLACK_AND_MAGENTA)
                else:
                    stdscr.addstr(line + "\n", BLACK_AND_GREEN)  # Highlight current row
            else:
                stdscr.addstr(line + "\n", GREEN_AND_BLACK)

        stdscr.refresh()

    def input_name():
        """Allows the user to type a name directly on the menu."""
        nonlocal name
        while True:
            show_screen(selected=True)  # Blink background while editing
            key = stdscr.getch()
            if key == ord('\n'):  # Finish editing on Enter
                break
            elif key in (127, curses.KEY_BACKSPACE, 8):  # Handle backspace
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
                save_and_load.add_drink(name, amounts)
                break #return to the previous menu
            elif current_row == 8:  # Exit\delete
                save_and_load.remove_drink(name)
                break

    curses.endwin()
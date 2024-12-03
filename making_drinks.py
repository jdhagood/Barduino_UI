import time
import curses
from selection_menu import make_selection_menu
from pico_control import ping_pico, led_off, led_on
import pico_control
import save_and_load

def connecting(stdscr):
    """
    Menu to display connection status with animation.
    Non-blocking input is used to ensure the animation runs smoothly.
    """
    # Initialize colors
    curses.init_pair(1, curses.COLOR_RED, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_GREEN, curses.COLOR_BLACK)
    curses.init_pair(3, curses.COLOR_GREEN, curses.COLOR_WHITE)
    curses.init_pair(4, curses.COLOR_RED, curses.COLOR_WHITE)

    RED_AND_BLACK = curses.color_pair(1)
    GREEN_AND_BLACK = curses.color_pair(2)

    # Headers for animation
    headers = ["""  ______    ______   __    __  __    __  ________   ______   ________  ______  __    __   ______  
 /      \  /      \ /  \  /  |/  \  /  |/        | /      \ /        |/      |/  \  /  | /      \ 
/$$$$$$  |/$$$$$$  |$$  \ $$ |$$  \ $$ |$$$$$$$$/ /$$$$$$  |$$$$$$$$/ $$$$$$/ $$  \ $$ |/$$$$$$  |
$$ |  $$/ $$ |  $$ |$$$  \$$ |$$$  \$$ |$$ |__    $$ |  $$/    $$ |     $$ |  $$$  \$$ |$$ | _$$/ 
$$ |      $$ |  $$ |$$$$  $$ |$$$$  $$ |$$    |   $$ |         $$ |     $$ |  $$$$  $$ |$$ |/    |
$$ |   __ $$ |  $$ |$$ $$ $$ |$$ $$ $$ |$$$$$/    $$ |   __    $$ |     $$ |  $$ $$ $$ |$$ |$$$$ |
$$ \__/  |$$ \__$$ |$$ |$$$$ |$$ |$$$$ |$$ |_____ $$ \__/  |   $$ |    _$$ |_ $$ |$$$$ |$$ \__$$ |
$$    $$/ $$    $$/ $$ | $$$ |$$ | $$$ |$$       |$$    $$/    $$ |   / $$   |$$ | $$$ |$$    $$/ 
 $$$$$$/   $$$$$$/  $$/   $$/ $$/   $$/ $$$$$$$$/  $$$$$$/     $$/    $$$$$$/ $$/   $$/  $$$$$$/  """, 
 """  ______    ______   __    __  __    __  ________   ______   ________  ______  __    __   ______     
 /      \  /      \ /  \  /  |/  \  /  |/        | /      \ /        |/      |/  \  /  | /      \    
/$$$$$$  |/$$$$$$  |$$  \ $$ |$$  \ $$ |$$$$$$$$/ /$$$$$$  |$$$$$$$$/ $$$$$$/ $$  \ $$ |/$$$$$$  |   
$$ |  $$/ $$ |  $$ |$$$  \$$ |$$$  \$$ |$$ |__    $$ |  $$/    $$ |     $$ |  $$$  \$$ |$$ | _$$/    
$$ |      $$ |  $$ |$$$$  $$ |$$$$  $$ |$$    |   $$ |         $$ |     $$ |  $$$$  $$ |$$ |/    |   
$$ |   __ $$ |  $$ |$$ $$ $$ |$$ $$ $$ |$$$$$/    $$ |   __    $$ |     $$ |  $$ $$ $$ |$$ |$$$$ |   
$$ \__/  |$$ \__$$ |$$ |$$$$ |$$ |$$$$ |$$ |_____ $$ \__/  |   $$ |    _$$ |_ $$ |$$$$ |$$ \__$$ |__ 
$$    $$/ $$    $$/ $$ | $$$ |$$ | $$$ |$$       |$$    $$/    $$ |   / $$   |$$ | $$$ |$$    $$//  |
 $$$$$$/   $$$$$$/  $$/   $$/ $$/   $$/ $$$$$$$$/  $$$$$$/     $$/    $$$$$$/ $$/   $$/  $$$$$$/ $$/ """, 
 """  ______    ______   __    __  __    __  ________   ______   ________  ______  __    __   ______         
 /      \  /      \ /  \  /  |/  \  /  |/        | /      \ /        |/      |/  \  /  | /      \        
/$$$$$$  |/$$$$$$  |$$  \ $$ |$$  \ $$ |$$$$$$$$/ /$$$$$$  |$$$$$$$$/ $$$$$$/ $$  \ $$ |/$$$$$$  |       
$$ |  $$/ $$ |  $$ |$$$  \$$ |$$$  \$$ |$$ |__    $$ |  $$/    $$ |     $$ |  $$$  \$$ |$$ | _$$/        
$$ |      $$ |  $$ |$$$$  $$ |$$$$  $$ |$$    |   $$ |         $$ |     $$ |  $$$$  $$ |$$ |/    |       
$$ |   __ $$ |  $$ |$$ $$ $$ |$$ $$ $$ |$$$$$/    $$ |   __    $$ |     $$ |  $$ $$ $$ |$$ |$$$$ |       
$$ \__/  |$$ \__$$ |$$ |$$$$ |$$ |$$$$ |$$ |_____ $$ \__/  |   $$ |    _$$ |_ $$ |$$$$ |$$ \__$$ |__  __ 
$$    $$/ $$    $$/ $$ | $$$ |$$ | $$$ |$$       |$$    $$/    $$ |   / $$   |$$ | $$$ |$$    $$//  |/  |
 $$$$$$/   $$$$$$/  $$/   $$/ $$/   $$/ $$$$$$$$/  $$$$$$/     $$/    $$$$$$/ $$/   $$/  $$$$$$/ $$/ $$/ """, 
 """  ______    ______   __    __  __    __  ________   ______   ________  ______  __    __   ______             
 /      \  /      \ /  \  /  |/  \  /  |/        | /      \ /        |/      |/  \  /  | /      \            
/$$$$$$  |/$$$$$$  |$$  \ $$ |$$  \ $$ |$$$$$$$$/ /$$$$$$  |$$$$$$$$/ $$$$$$/ $$  \ $$ |/$$$$$$  |           
$$ |  $$/ $$ |  $$ |$$$  \$$ |$$$  \$$ |$$ |__    $$ |  $$/    $$ |     $$ |  $$$  \$$ |$$ | _$$/            
$$ |      $$ |  $$ |$$$$  $$ |$$$$  $$ |$$    |   $$ |         $$ |     $$ |  $$$$  $$ |$$ |/    |           
$$ |   __ $$ |  $$ |$$ $$ $$ |$$ $$ $$ |$$$$$/    $$ |   __    $$ |     $$ |  $$ $$ $$ |$$ |$$$$ |           
$$ \__/  |$$ \__$$ |$$ |$$$$ |$$ |$$$$ |$$ |_____ $$ \__/  |   $$ |    _$$ |_ $$ |$$$$ |$$ \__$$ |__  __  __ 
$$    $$/ $$    $$/ $$ | $$$ |$$ | $$$ |$$       |$$    $$/    $$ |   / $$   |$$ | $$$ |$$    $$//  |/  |/  |
 $$$$$$/   $$$$$$/  $$/   $$/ $$/   $$/ $$$$$$$$/  $$$$$$/     $$/    $$$$$$/ $$/   $$/  $$$$$$/ $$/ $$/ $$/ """]
    animation_speed = 0.5  # Time interval for animation updates (in seconds)

    # Set the terminal to non-blocking mode
    stdscr.nodelay(True)

    last_time = time.time()
    connecting_index = 0
    connected = False
    while not connected:
        # Animation logic
        if time.time() - last_time >= animation_speed:
            connected = ping_pico()
            last_time = time.time()
            stdscr.clear()
            stdscr.addstr(0, 0, headers[connecting_index], RED_AND_BLACK)
            stdscr.addstr("\n\nMake sure that you are connected to the same wifi network as the Barduino.\n\nHold 'b' to exit", GREEN_AND_BLACK)
            stdscr.refresh()
            connecting_index = (connecting_index + 1) % len(headers)

        # Non-blocking key input
        stdscr.nodelay(True)
        key = stdscr.getch()
        if key == ord('b'):  # Exit the function on 'b' key press
            stdscr.nodelay(False) #Change back to defalut blocking
            return False

        # Small sleep to prevent excessive CPU usage
        time.sleep(0.01)
    stdscr.nodelay(False)
    return True

sub_led_control_menu = make_selection_menu(""" __        ________  _______          ______    ______   __    __  ________  _______    ______   __       
/  |      /        |/       \        /      \  /      \ /  \  /  |/        |/       \  /      \ /  |      
$$ |      $$$$$$$$/ $$$$$$$  |      /$$$$$$  |/$$$$$$  |$$  \ $$ |$$$$$$$$/ $$$$$$$  |/$$$$$$  |$$ |      
$$ |      $$ |__    $$ |  $$ |      $$ |  $$/ $$ |  $$ |$$$  \$$ |   $$ |   $$ |__$$ |$$ |  $$ |$$ |      
$$ |      $$    |   $$ |  $$ |      $$ |      $$ |  $$ |$$$$  $$ |   $$ |   $$    $$< $$ |  $$ |$$ |      
$$ |      $$$$$/    $$ |  $$ |      $$ |   __ $$ |  $$ |$$ $$ $$ |   $$ |   $$$$$$$  |$$ |  $$ |$$ |      
$$ |_____ $$ |_____ $$ |__$$ |      $$ \__/  |$$ \__$$ |$$ |$$$$ |   $$ |   $$ |  $$ |$$ \__$$ |$$ |_____ 
$$       |$$       |$$    $$/       $$    $$/ $$    $$/ $$ | $$$ |   $$ |   $$ |  $$ |$$    $$/ $$       |
$$$$$$$$/ $$$$$$$$/ $$$$$$$/         $$$$$$/   $$$$$$/  $$/   $$/    $$/    $$/   $$/  $$$$$$/  $$$$$$$$/ """, [
    ["on", led_on],
    ["off", led_off],
    ["exit", lambda _: 1]
])

def led_control_menu(stdscr):
    connected = connecting(stdscr)
    if connected:
        sub_led_control_menu(stdscr)

def drink_selection_menu(stdscr):
    # Initialize colors
    curses.init_pair(1, curses.COLOR_RED, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_GREEN, curses.COLOR_BLACK)
    curses.init_pair(3, curses.COLOR_GREEN, curses.COLOR_WHITE)
    curses.init_pair(4, curses.COLOR_BLACK, curses.COLOR_GREEN)

    RED_AND_BLACK = curses.color_pair(1)
    GREEN_AND_BLACK = curses.color_pair(2)
    GREEN_AND_WHITE = curses.color_pair(3)
    BLACK_AND_GREEN = curses.color_pair(4)

    header = """ _______   _______   ______  __    __  __    __         ______   ________  __        ________   ______   ________  ______   ______   __    __ 
/       \ /       \ /      |/  \  /  |/  |  /  |       /      \ /        |/  |      /        | /      \ /        |/      | /      \ /  \  /  |
$$$$$$$  |$$$$$$$  |$$$$$$/ $$  \ $$ |$$ | /$$/       /$$$$$$  |$$$$$$$$/ $$ |      $$$$$$$$/ /$$$$$$  |$$$$$$$$/ $$$$$$/ /$$$$$$  |$$  \ $$ |
$$ |  $$ |$$ |__$$ |  $$ |  $$$  \$$ |$$ |/$$/        $$ \__$$/ $$ |__    $$ |      $$ |__    $$ |  $$/    $$ |     $$ |  $$ |  $$ |$$$  \$$ |
$$ |  $$ |$$    $$<   $$ |  $$$$  $$ |$$  $$<         $$      \ $$    |   $$ |      $$    |   $$ |         $$ |     $$ |  $$ |  $$ |$$$$  $$ |
$$ |  $$ |$$$$$$$  |  $$ |  $$ $$ $$ |$$$$$  \         $$$$$$  |$$$$$/    $$ |      $$$$$/    $$ |   __    $$ |     $$ |  $$ |  $$ |$$ $$ $$ |
$$ |__$$ |$$ |  $$ | _$$ |_ $$ |$$$$ |$$ |$$  \       /  \__$$ |$$ |_____ $$ |_____ $$ |_____ $$ \__/  |   $$ |    _$$ |_ $$ \__$$ |$$ |$$$$ |
$$    $$/ $$ |  $$ |/ $$   |$$ | $$$ |$$ | $$  |      $$    $$/ $$       |$$       |$$       |$$    $$/    $$ |   / $$   |$$    $$/ $$ | $$$ |
$$$$$$$/  $$/   $$/ $$$$$$/ $$/   $$/ $$/   $$/        $$$$$$/  $$$$$$$$/ $$$$$$$$/ $$$$$$$$/  $$$$$$/     $$/    $$$$$$/  $$$$$$/  $$/   $$/ """
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
            return ["No drinks found"]
        
        menu_options = []
        for drink_name, amounts in drinks.items():
            drinks_and_amounts.append([drink_name, amounts])
            title = f"{drink_name}\n"
            for liquid, amount in zip(liquids, amounts):
                bar = f"[{'■' * amount + ' ' * (10 - amount)}]"
                title += f"  {liquid}:{" "*(max_liquid_name_length - len(liquid))} {bar}\n"
            menu_options.append(title)
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
            drink_name, amounts = drinks_and_amounts[current_row]
            return drink_name, amounts


def drink_making_menu(stdscr):
    # Initialize colors
    curses.init_pair(1, curses.COLOR_RED, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_GREEN, curses.COLOR_BLACK)
    curses.init_pair(3, curses.COLOR_GREEN, curses.COLOR_WHITE)
    curses.init_pair(4, curses.COLOR_BLACK, curses.COLOR_GREEN)

    RED_AND_BLACK = curses.color_pair(1)
    GREEN_AND_BLACK = curses.color_pair(2)
    GREEN_AND_WHITE = curses.color_pair(3)
    BLACK_AND_GREEN = curses.color_pair(4)

    header = """ _______   _______   ______  __    __  __    __        _______   _______   ________  _______  
/       \ /       \ /      |/  \  /  |/  |  /  |      /       \ /       \ /        |/       \ 
$$$$$$$  |$$$$$$$  |$$$$$$/ $$  \ $$ |$$ | /$$/       $$$$$$$  |$$$$$$$  |$$$$$$$$/ $$$$$$$  |
$$ |  $$ |$$ |__$$ |  $$ |  $$$  \$$ |$$ |/$$/        $$ |__$$ |$$ |__$$ |$$ |__    $$ |__$$ |
$$ |  $$ |$$    $$<   $$ |  $$$$  $$ |$$  $$<         $$    $$/ $$    $$< $$    |   $$    $$/ 
$$ |  $$ |$$$$$$$  |  $$ |  $$ $$ $$ |$$$$$  \        $$$$$$$/  $$$$$$$  |$$$$$/    $$$$$$$/  
$$ |__$$ |$$ |  $$ | _$$ |_ $$ |$$$$ |$$ |$$  \       $$ |      $$ |  $$ |$$ |_____ $$ |      
$$    $$/ $$ |  $$ |/ $$   |$$ | $$$ |$$ | $$  |      $$ |      $$ |  $$ |$$       |$$ |      
$$$$$$$/  $$/   $$/ $$$$$$/ $$/   $$/ $$/   $$/       $$/       $$/   $$/ $$$$$$$$/ $$/       """
    current_row = 0
    selected_drink = None
    amounts = None
    how_many = 1
    menu_options = [
        "Select Drink: ",
        "How Many Drinks: ",
        "Make Drink",
        "Back"
    ]

    def show_screen(selected=False):
        """Displays the menu screen."""
        stdscr.clear()
        stdscr.addstr(header + "\n", RED_AND_BLACK)
        stdscr.addstr("-" * curses.COLS + "\n", GREEN_AND_BLACK)

        for i, title in enumerate(menu_options):
            line = title
            if line == "Select Drink: ":
                if selected_drink:
                    line += selected_drink
                else:
                    line += "<Please Select Drink>"
            elif line == "How Many Drinks: ":
                line += str(how_many)
            if i == current_row:
                if selected:
                    stdscr.addstr(line + "\n", GREEN_AND_WHITE)
                else:
                    stdscr.addstr(line + "\n", BLACK_AND_GREEN)  # Highlight current row
            else:
                stdscr.addstr(line + "\n", GREEN_AND_BLACK)

        stdscr.refresh()

    def set_how_many_drinks():
        nonlocal how_many
        while True:
            show_screen(selected=True)
            key = stdscr.getch()
            if key == curses.KEY_UP and how_many < 6:
                how_many += 1
            elif key == curses.KEY_DOWN and how_many > 1:
                how_many -= 1
            elif key == ord('\n'):
                break

    while True:
        show_screen()
        key = stdscr.getch()

        if key == curses.KEY_UP and current_row > 0:
            current_row -= 1
        elif key == curses.KEY_DOWN and current_row < len(menu_options) - 1:
            current_row += 1
        elif key == ord('\n'):  # Select the current option
            if menu_options[current_row] == "Back":
                return
            elif menu_options[current_row] == "Make Drink":
                if amounts and selected_drink:
                    make_drinks(stdscr, how_many, amounts)
            elif menu_options[current_row] == "How Many Drinks: ":
                set_how_many_drinks()
            elif menu_options[current_row] == "Select Drink: ":
                selected_drink, amounts = drink_selection_menu(stdscr)
            
def make_drinks(stdscr, how_many, amounts):
    # Initialize colors
    curses.init_pair(1, curses.COLOR_RED, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_GREEN, curses.COLOR_BLACK)
    curses.init_pair(3, curses.COLOR_GREEN, curses.COLOR_WHITE)
    curses.init_pair(4, curses.COLOR_BLACK, curses.COLOR_GREEN)

    RED_AND_BLACK = curses.color_pair(1)
    GREEN_AND_BLACK = curses.color_pair(2)
    GREEN_AND_WHITE = curses.color_pair(3)
    BLACK_AND_GREEN = curses.color_pair(4)

    is_connected = connecting()
    if not is_connected:
        return

    loading_header = \
""" __         ______    ______   _______          ______   __    __  _______    ______  
/  |       /      \  /      \ /       \        /      \ /  |  /  |/       \  /      \ 
$$ |      /$$$$$$  |/$$$$$$  |$$$$$$$  |      /$$$$$$  |$$ |  $$ |$$$$$$$  |/$$$$$$  |
$$ |      $$ |  $$ |$$ |__$$ |$$ |  $$ |      $$ |  $$/ $$ |  $$ |$$ |__$$ |$$ \__$$/ 
$$ |      $$ |  $$ |$$    $$ |$$ |  $$ |      $$ |      $$ |  $$ |$$    $$/ $$      \ 
$$ |      $$ |  $$ |$$$$$$$$ |$$ |  $$ |      $$ |   __ $$ |  $$ |$$$$$$$/   $$$$$$  |
$$ |_____ $$ \__$$ |$$ |  $$ |$$ |__$$ |      $$ \__/  |$$ \__$$ |$$ |      /  \__$$ |
$$       |$$    $$/ $$ |  $$ |$$    $$/       $$    $$/ $$    $$/ $$ |      $$    $$/ 
$$$$$$$$/  $$$$$$/  $$/   $$/ $$$$$$$/         $$$$$$/   $$$$$$/  $$/        $$$$$$/ """

    cups_loaded = 0
    last_time = 0
    stdscr.nodelay(True)
    while cups_loaded < how_many:
        stdscr.clear()
        stdscr.addstr(loading_header + "\n", RED_AND_BLACK)
        stdscr.addstr("Put cup in front of sensor\n\n Hold 'b' to cancel", GREEN_AND_BLACK)
        if time.time-last_time() > 0.2:
            cup_detected = pico_control.detect_cup() #implement this
            if cup_detected:
                cups_loaded += 1
                if cups_loaded != how_many:
                    pico_control.advance_table() #implement this

            key = stdscr.getch()
            if key == ord('b'):  # Exit the function on 'b' key press
                stdscr.nodelay(False) #Change back to defalut blocking
                return False

    stdscr.nodelay(False)

    making_drinks_header = """ __       __   ______   __    __  ______  __    __   ______         _______   _______   ______  __    __  __    __   ______  
/  \     /  | /      \ /  |  /  |/      |/  \  /  | /      \       /       \ /       \ /      |/  \  /  |/  |  /  | /      \ 
$$  \   /$$ |/$$$$$$  |$$ | /$$/ $$$$$$/ $$  \ $$ |/$$$$$$  |      $$$$$$$  |$$$$$$$  |$$$$$$/ $$  \ $$ |$$ | /$$/ /$$$$$$  |
$$$  \ /$$$ |$$ |__$$ |$$ |/$$/    $$ |  $$$  \$$ |$$ | _$$/       $$ |  $$ |$$ |__$$ |  $$ |  $$$  \$$ |$$ |/$$/  $$ \__$$/ 
$$$$  /$$$$ |$$    $$ |$$  $$<     $$ |  $$$$  $$ |$$ |/    |      $$ |  $$ |$$    $$<   $$ |  $$$$  $$ |$$  $$<   $$      \ 
$$ $$ $$/$$ |$$$$$$$$ |$$$$$  \    $$ |  $$ $$ $$ |$$ |$$$$ |      $$ |  $$ |$$$$$$$  |  $$ |  $$ $$ $$ |$$$$$  \   $$$$$$  |
$$ |$$$/ $$ |$$ |  $$ |$$ |$$  \  _$$ |_ $$ |$$$$ |$$ \__$$ |      $$ |__$$ |$$ |  $$ | _$$ |_ $$ |$$$$ |$$ |$$  \ /  \__$$ |
$$ | $/  $$ |$$ |  $$ |$$ | $$  |/ $$   |$$ | $$$ |$$    $$/       $$    $$/ $$ |  $$ |/ $$   |$$ | $$$ |$$ | $$  |$$    $$/ 
$$/      $$/ $$/   $$/ $$/   $$/ $$$$$$/ $$/   $$/  $$$$$$/        $$$$$$$/  $$/   $$/ $$$$$$/ $$/   $$/ $$/   $$/  $$$$$$/  """

    drink_positions = [i for i in range(how_many)]

    for _ in range(6): #spin the table around 6 positions
        for liquid_pos, amount in enumerate(amounts):
            if liquid_pos in drink_positions:
                pico_control.pour(liquid_pos, amount)
        
        pico_control.advance_table()
        drink_positions = [(i + 1) % 6 for i in drink_positions]
    

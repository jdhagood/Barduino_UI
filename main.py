import curses
from edit_drinks_menu import new_drink_making_menu, liquid_editing_menu, saved_drink_editing_menu
from selection_menu import make_selection_menu
from info_window import info_window
from making_drinks import led_control_menu, drink_making_menu

# ASCII header
header = r""" _______                             __            __                     
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

drink_menu_header = r""" _______   _______   ______  __    __  __    __         ______    ______   __    __  ________  ______   ______  
/       \ /       \ /      |/  \  /  |/  |  /  |       /      \  /      \ /  \  /  |/        |/      | /      \ 
$$$$$$$  |$$$$$$$  |$$$$$$/ $$  \ $$ |$$ | /$$/       /$$$$$$  |/$$$$$$  |$$  \ $$ |$$$$$$$$/ $$$$$$/ /$$$$$$  |
$$ |  $$ |$$ |__$$ |  $$ |  $$$  \$$ |$$ |/$$/        $$ |  $$/ $$ |  $$ |$$$  \$$ |$$ |__      $$ |  $$ | _$$/ 
$$ |  $$ |$$    $$<   $$ |  $$$$  $$ |$$  $$<         $$ |      $$ |  $$ |$$$$  $$ |$$    |     $$ |  $$ |/    |
$$ |  $$ |$$$$$$$  |  $$ |  $$ $$ $$ |$$$$$  \        $$ |   __ $$ |  $$ |$$ $$ $$ |$$$$$/      $$ |  $$ |$$$$ |
$$ |__$$ |$$ |  $$ | _$$ |_ $$ |$$$$ |$$ |$$  \       $$ \__/  |$$ \__$$ |$$ |$$$$ |$$ |       _$$ |_ $$ \__$$ |
$$    $$/ $$ |  $$ |/ $$   |$$ | $$$ |$$ | $$  |      $$    $$/ $$    $$/ $$ | $$$ |$$ |      / $$   |$$    $$/ 
$$$$$$$/  $$/   $$/ $$$$$$/ $$/   $$/ $$/   $$/        $$$$$$/   $$$$$$/  $$/   $$/ $$/       $$$$$$/  $$$$$$/  """
drink_editing_menu = make_selection_menu(drink_menu_header, [
    ["Make New Drink", new_drink_making_menu],
    ["Edit Drinks", saved_drink_editing_menu],
    ["Edit Liquids", liquid_editing_menu],
    ["Back", lambda _: 1]
])

main_menu = make_selection_menu(header, [
    ("Make Drinks", drink_making_menu),
    ("Drink Config", drink_editing_menu),
    ("Info", info_window),
    ("Exit", lambda _: True)
])

def main(stdscr):
    curses.curs_set(0)  # Hide cursor
    main_menu(stdscr)

if __name__ == "__main__":
    curses.wrapper(main)

import curses
from edit_drinks_menu import drink_making_menu, liquid_editing_menu, saved_drink_editing_menu
from selection_menu import make_selection_menu
from info_window import make_info_window
import save_and_load


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
    ["Start\n Start \n Start", lambda _: 0],
    ["Back", lambda _: 1]
])

drink_editing_menu = make_selection_menu("Edit Drinks", [
    ["Make New Drink", drink_making_menu],
    ["Edit Drinks", saved_drink_editing_menu],
    ["Edit Liquids", liquid_editing_menu],
    ["Back", lambda _: 1]
])

#The Drink editing menu
# def drink_editing_menu(stdscr):
#     choices = [["Back", lambda _: 1],
#                ["New Drink", drink_making_menu],
#                ["Edit Liquids", lambda _: 0]]
#     liquids = save_and_load.load_liquids()
#     drinks = save_and_load.load_drinks()
#     print(drinks)
#     for drink, amounts in drinks.items():
#         title = drink + "\n"
#         for i, amount in enumerate(amounts):
#             title += liquids[i] + ": " + "<" + "▇" * amount + (10 - amount) * " "  ">" + "\n"
#         choices.append([title, drink_making_menu(stdscr, drink, amounts)])
#     a = make_selection_menu("Drink Editing", choices)
#     a(stdscr)

info_menu = make_info_window("INFO", "This is information about the Barduino.")

main_menu = make_selection_menu(header, [
    ["Start \n Start ", start_menu],
    ["Edit Drinks", drink_editing_menu],
    ["Info", info_menu],
    ["Exit", lambda _: True]
])

def main(stdscr):
    curses.curs_set(0)  # Hide cursor
    main_menu(stdscr)

if __name__ == "__main__":
    curses.wrapper(main)

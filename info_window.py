import curses

def info_window(stdscr):
    curses.init_pair(1, curses.COLOR_RED, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_GREEN, curses.COLOR_BLACK)
    RED_AND_BLACK = curses.color_pair(1)
    GREEN_AND_BLACK = curses.color_pair(2)

    header = """ ______  __    __  ________  ______  
/      |/  \  /  |/        |/      \ 
$$$$$$/ $$  \ $$ |$$$$$$$$//$$$$$$  |
  $$ |  $$$  \$$ |$$ |__   $$ |  $$ |
  $$ |  $$$$  $$ |$$    |  $$ |  $$ |
  $$ |  $$ $$ $$ |$$$$$/   $$ |  $$ |
 _$$ |_ $$ |$$$$ |$$ |     $$ \__$$ |
/ $$   |$$ | $$$ |$$ |     $$    $$/ 
$$$$$$/ $$/   $$/ $$/       $$$$$$/ """
    info = [
        "Press 'b' to go back.",
        "Use arrow keys to scroll",
        "",
        "Github: https://github.com/jdhagood/Barduino_UI",
        "",
        "GENERAL",
        "This is UI for the 'Barduino', a machine made by the EECS section of",
        "HTMAA 2024. It is truly a marvel of MIT students' ingenuity and love",
        "of alcohol.",
        "",
        "NAVIGATION",
        "Navigate the menus with the arrow keys.",
        "Press 'Enter' to select a menu item.",
        "Some menu items require text input. Select them, type your input, and",
        "press 'Enter' to save and exit.",
        "",
        "MAKING NEW SYSTEM DRINKS",
        "To make a new drink go to the Drink Config menu.",
        "Select Make New Drink and enter the name. Adjust the amounts of",
        "each liquid to desired amounts."
        "",
        "EDITING SYSTEM DRINKS",
        "If you would like to edit or delete a drink go under the Drink",
        "Config menu and select Edit Drinks. You can scroll through saved",
        "Drinks and select the one you wish to edit/delete.",
        "",
        "EDITING LIQUIDS",
        "If you change the liquids on the Barduino, you can reflect this",
        "by going to the Edit Liquids menu under the Drink Config menu.",
        "Simply select and type in the name of the new liquid. This change",
        "will effect all of the drinks saved in the system so you may have",
        "to delete drinks that are no longer possible.",
        "",
        "POURING DRINKS",
        "To actually make the Barduino pour you a drink. Go under the Pour",
        "Drinks menu. Select the drink you want to make, and the number of",
        "drinks between 1 and 6. The menus will walk you through loading the",
        "cups and notify you when it is done pouring. Sit back and enjoy the",
        "show.",
        "",
        "FURTHER QUESTIONS",
        "Email me at jdhagood@mit.edu with subject 'BARDUINO'."
    ]

    header_height = header.count("\n") + 1
    pad_height = len(info) + 2
    pad_width = max(len(line) for line in info) + 2
    pad = curses.newpad(pad_height, pad_width)

    for line in info:
        pad.addstr(line + "\n", GREEN_AND_BLACK)

    pad_pos = 0
    max_visible_lines = 20
    max_visible_columns = min(curses.COLS, pad_width)

    stdscr.clear()
    stdscr.addstr(0, 0, header, RED_AND_BLACK)
    stdscr.refresh()

    while True:
        pad.refresh(
            pad_pos, 0,
            header_height, 0,
            header_height + max_visible_lines - 1, max_visible_columns - 1
        )

        key = stdscr.getch()
        if key == curses.KEY_UP and pad_pos > 0:
            pad_pos -= 1
        elif key == curses.KEY_DOWN and pad_pos < pad_height - max_visible_lines:
            pad_pos += 1
        elif key == ord('b'):
            break

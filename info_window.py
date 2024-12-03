import curses

def info_window(stdscr):
    """
    Displays a header at the top and scrollable information below it.
    The information is in a pad and is scrolled using arrow keys.
    Pressing 'b' exits the function.
    """
    # Initialize colors
    curses.init_pair(1, curses.COLOR_RED, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_GREEN, curses.COLOR_BLACK)
    curses.init_pair(3, curses.COLOR_GREEN, curses.COLOR_WHITE)
    curses.init_pair(4, curses.COLOR_RED, curses.COLOR_WHITE)

    RED_AND_BLACK = curses.color_pair(1)
    GREEN_AND_BLACK = curses.color_pair(2)
    GREEN_AND_WHITE = curses.color_pair(3)
    RED_AND_WHITE = curses.color_pair(4)

    # Sample header and information content
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
        GREEN_AND_BLACK,
        "Press 'b' to go back. \n",
        "Use arrow keys to scroll\n\n",
        GREEN_AND_BLACK,
        "Github: https://github.com/jdhagood/Barduino_UI \n\n",
        RED_AND_BLACK,
        "General\n",
        GREEN_AND_BLACK,
        "This is UI for the 'Barduino', a machine made by the EECS section of HTMAA 2024.\n",
        "It is truly a marvel of MIT students' ingenuity and love of alcohol.\n\n",
        RED_AND_BLACK,
        "A quick how to"
    ]

    # Split information into lines for easier management
    #info_lines = info.splitlines()

    # Create a pad for the information
    header_height = header.count("\n") + 2
    pad_height = len(info) + 1
    pad_width = max(len(line) for line in info if isinstance(line, str)) + 2
    pad = curses.newpad(pad_height, pad_width)

    # Write content to the pad
    current_color = GREEN_AND_BLACK
    for line in info:
        if isinstance(line, str):
            pad.addstr(line, current_color)
        else:
            current_color = line

    # Variables to manage scrolling
    pad_pos = 0  # Current position in the pad
    max_visible_lines = 20 # Leave space for the header
    max_visible_columns = pad_width  # Use the full width of the screen

    # Clear the screen
    stdscr.clear()
    stdscr.addstr(0, 0, header, RED_AND_BLACK)
    stdscr.refresh()

    while True:
        # Refresh the pad to display visible lines
        pad.refresh(
            pad_pos, 0,  # Upper-left corner of the pad to display
            header_height, 0,  # Upper-left corner of the screen to start displaying the pad
            max_visible_lines + 1, max_visible_columns  # Lower-right corner of the screen
        )

        # Get user input
        key = stdscr.getch()

        if key == curses.KEY_UP and pad_pos > 0:  # Scroll up
            pad_pos -= 1
        elif key == curses.KEY_DOWN and pad_pos < pad_height - max_visible_lines:  # Scroll down
            pad_pos += 1
        elif key == ord('b'):  # Exit the function
            break

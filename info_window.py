import curses

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
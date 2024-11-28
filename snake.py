import curses
from time import sleep
from random import randint

WIDTH = 30
HEIGHT = 30
global apple_x 
global apple_y
def main(stdscr):
    if apple_x is None:
        apple_x = randint(1, WIDTH + 1)
    if apple_y is None:
        apple_y = randint(1, HEIGHT + 1)
    curses.init_pair(1, curses.COLOR_GREEN, curses.COLOR_BLACK) #ID, foreground, background
    curses.init_pair(2, curses.COLOR_CYAN, curses.COLOR_BLACK) #ID, foreground, background
    GREEN_AND_BLACK = curses.color_pair(1)
    BLUE_AND_BLACK = curses.color_pair(2)
    # Initialize the screen
    curses.curs_set(0)  # Hide the cursor
    stdscr.nodelay(1)   # Non-blocking input
    stdscr.timeout(100) # Refresh rate in milliseconds

    # Initial snake position and direction
    snake = [[5, 10], [5, 9], [5, 8]]  # List of [y, x] coordinates
    direction = curses.KEY_RIGHT       # Initial direction

    # Game loop
    while True:
        # Get user input
        key = stdscr.getch()
        if key != -1:
            direction = key

        # Calculate new head position
        head = snake[0]
        if direction == curses.KEY_UP:
            new_head = [head[0] - 1, head[1]]
        elif direction == curses.KEY_DOWN:
            new_head = [head[0] + 1, head[1]]
        elif direction == curses.KEY_LEFT:
            new_head = [head[0], head[1] - 1]
        elif direction == curses.KEY_RIGHT:
            new_head = [head[0], head[1] + 1]

        # Add the new head to the snake
        snake.insert(0, new_head)

        # Remove the tail to simulate movement
        snake.pop()

        # Clear the screen and draw the snake
        stdscr.clear()
        for segment in snake:
            stdscr.addch(segment[0], segment[1], '■', GREEN_AND_BLACK)
        
        #display the apple
        stdscr.addstr(apple_y, apple_x, '🍎')

        #interact with the apple
        if apple_y == snake[0][1] and apple_x == snake[0][0]:
            apple_x = 1

        #draw board
        stdscr.addstr(0, 0, '▦'*(WIDTH+2), BLUE_AND_BLACK)
        for i in range(1, HEIGHT + 1):
            stdscr.addstr(i, 0, '▦', BLUE_AND_BLACK)
            stdscr.addstr(i, WIDTH+1, '▦', BLUE_AND_BLACK)
        stdscr.addstr(HEIGHT+1, 0, '▦'*(WIDTH+2), BLUE_AND_BLACK)
        # Refresh the screen
        stdscr.refresh()

        # End the game if the snake collides with the edges
        if (new_head[0] in [0, curses.LINES] or
            new_head[1] in [0, curses.COLS]):
            break

        # Delay for the game loop
        sleep(0.1)

# Run the game
curses.wrapper(main)

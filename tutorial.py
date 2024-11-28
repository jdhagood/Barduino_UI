import curses
import time

#ASCII art generated from https://patorjk.com/software/taag/#p=testall&h=1&v=1&f=Big%20Money-sw&t=Barduino
logo2  = """
   ___                 __       _          
  / _ ) ___ _ ____ ___/ /__ __ (_)___  ___ 
 / _  |/ _ `// __// _  // // // // _ \/ _ \\
/____/ \_,_//_/   \_,_/ \_,_//_//_//_/\___/
                                           
"""

logo3 = """
 __                    
|__) _  _ _|   . _  _  
|__)(_|| (_||_||| )(_) 
""" # font: Straight

attrs = [ # comments apply to poewrshell
    curses.A_ALTCHARSET, # sorta glitched effect
    curses.A_BLINK, #light gray highlight background
    curses.A_BOLD, #bolded
    curses.A_DIM,
    curses.A_INVIS,
    curses.A_ITALIC, #italic
    curses.A_NORMAL,
    curses.A_PROTECT,
    curses.A_REVERSE, #medium gray background
    curses.A_STANDOUT, # white backgorund
    curses.A_UNDERLINE, #underline
    curses.A_HORIZONTAL,
    curses.A_LEFT,
    curses.A_LOW,
    curses.A_RIGHT,
    curses.A_TOP,
    curses.A_VERTICAL,
    curses.A_CHARTEXT
]

def main_menu(stdscr):
    curses.init_pair(1, curses.COLOR_RED, curses.COLOR_BLACK) #ID, foreground, background
    curses.init_pair(2, curses.COLOR_GREEN, curses.COLOR_BLACK)
    curses.init_pair(3, curses.COLOR_GREEN, curses.COLOR_WHITE)
    RED_AND_BLACK = curses.color_pair(1)
    BLUE_AND_BLACK = curses.color_pair(2)
    BLUE_AND_WHITE = curses.color_pair(3)
    header =  """
 ______                    _         _               
(____  \                  | |       (_)              
 ____)  ) _____   ____  __| | _   _  _  ____    ___  
|  __  ( (____ | / ___)/ _  || | | || ||  _ \  / _ \ tm
| |__)  )/ ___ || |   ( (_| || |_| || || | | || |_| |
|______/ \_____||_|    \____||____/ |_||_| |_| \___/      
    """ # font: rounded
    MENU_OPTIONS = [
        ["Pour Drinks", lambda _: 0],
        ["Make Drinks", lambda _: 0],
        ["Info", info],
        ["Exit Program", lambda _: True] 
    ]
    options_win = curses.newwin(len(MENU_OPTIONS) + 1, 20, 8, 0) # len(MENU_OPTIONS) char tall, 20 char long, 10 rows down, 0 cols over
    current_row = 0

    while True:
        stdscr.clear()
        stdscr.addstr(header, RED_AND_BLACK)
        stdscr.refresh()

        options_win.clear()
        for i, menu_item in enumerate(MENU_OPTIONS):
            if i == current_row:
                options_win.addstr(i, 0, menu_item[0], BLUE_AND_WHITE)
            else:
                options_win.addstr(i, 0, menu_item[0], BLUE_AND_BLACK)
        options_win.refresh()
        key = stdscr.getch()
        if key == curses.KEY_UP and current_row > 0:
            current_row -= 1
        elif key == curses.KEY_DOWN and current_row < len(MENU_OPTIONS) - 1:
            current_row += 1
        elif key == ord("\n"):  # Enter key
            should_exit = MENU_OPTIONS[current_row][1](stdscr)
            if should_exit:
                return True


def info(stdscr):
    stdscr.clear()
    curses.init_pair(1, curses.COLOR_RED, curses.COLOR_BLACK) #ID, foreground, background
    curses.init_pair(2, curses.COLOR_GREEN, curses.COLOR_BLACK)
    curses.init_pair(3, curses.COLOR_GREEN, curses.COLOR_WHITE)
    RED_AND_BLACK = curses.color_pair(1)
    BLUE_AND_BLACK = curses.color_pair(2)
    BLUE_AND_WHITE = curses.color_pair(3)
    header = """
$$$$$$\ $$\   $$\ $$$$$$$$\  $$$$$$\  
\_$$  _|$$$\  $$ |$$  _____|$$  __$$\ 
  $$ |  $$$$\ $$ |$$ |      $$ /  $$ |
  $$ |  $$ $$\$$ |$$$$$\    $$ |  $$ |
  $$ |  $$ \$$$$ |$$  __|   $$ |  $$ |
  $$ |  $$ |\$$$ |$$ |      $$ |  $$ |
$$$$$$\ $$ | \$$ |$$ |       $$$$$$  |
\______|\__|  \__|\__|       \______/ 
    """
    stdscr.addstr(header, RED_AND_BLACK)
    stdscr.refresh()
    key = stdscr.getch()



def main(stdscr):
    curses.curs_set(0)  # Hide cursor
    main_menu(stdscr)
    # curses.init_pair(1, curses.COLOR_RED, curses.COLOR_BLACK) #ID, foreground, background
    # curses.init_pair(2, curses.COLOR_BLUE, curses.COLOR_GREEN) #ID, foreground, background
    # RED_AND_BLACK = curses.color_pair(1)
    # BLUE_AND_GREEN = curses.color_pair(2)

    # counter_win = curses.newwin(1, 20, 10, 10) # 1 char tall, 20 char long, 10 rows down, 10 cols over
    # #you can update windows independently of the screen and other windows
    # pad =  curses.newpad(100, 100) # create a pad 100 lines by 100 cols
    # stdscr.refresh()
    # stdscr.addstr(logo2, RED_AND_BLACK)
    
    # # for _ in range(100):
    # #     for j in range(26):
    # #         char = chr(67+j)
    # #         pad.addstr(char, BLUE_AND_GREEN)
    # # for i in range(50):
    # #     stdscr.clear()
    # #     stdscr.refresh()
    # #     pad.refresh(0, 0, 5, 5+i, 10, 10+i)# (pad upper left start) (screen pad upper left) (screen pad lower right)
    # #     time.sleep(0.2)
    # # stdscr.getch()
    # # stdscr.clear()
    # # # for i, a in enumerate(attrs):   
    # # #     stdscr.addstr(i, 0,"Hello World", a | BLUE_AND_YELLOW) #row, col, text
    # # #stdscr.addstr(logo, BLUE_AND_YELLOW)
    # # for i in range(50):
    # #     counter_win.clear()
    # #     if i % 2 == 0:
    # #         counter_win.addstr(str(i), BLUE_AND_GREEN)
    # #     else:
    # #         counter_win.addstr(str(i), RED_AND_BLACK)
    # #     time.sleep(0.2)
    # #     counter_win.refresh()

    # stdscr.refresh()
    # stdscr.getch() # watit for the user to hit a key

if __name__ == "__main__":
    curses.wrapper(main)
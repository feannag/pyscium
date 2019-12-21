import curses
import curses.textpad
import sys


def init_ncurses():
    stdscr = curses.initscr()
    curses.noecho()
    curses.cbreak()
    stdscr.keypad(True)
    return stdscr


def restore_terminal(stdscr):
    curses.nocbreak()
    stdscr.keypad(False)
    curses.echo()
    curses.endwin()


def main():
    stdscr = init_ncurses()

    try:
        while True:
            ch = stdscr.getch()
            if ch == 24:
                sys.exit()
            stdscr.addch(ch)
    except KeyboardInterrupt:
        pass
    finally:
        restore_terminal(stdscr)


if __name__ == "__main__":
    main()

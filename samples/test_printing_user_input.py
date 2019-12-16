import curses
import curses.textpad


def terminate_application(stdscr):
    curses.nocbreak()
    stdscr.keypad(False)
    curses.echo()
    curses.endwin()


def main():
    stdscr = curses.initscr()
    curses.noecho()
    curses.cbreak()
    stdscr.keypad(True)

    # take user input and print it on screen
    ch = stdscr.getch()
    while ch != ord('~'):
        textbox = curses.textpad.Textbox(stdscr)
        textbox.do_command(ch)
        ch = stdscr.getch()

    # clean up
    terminate_application(stdscr)


main()

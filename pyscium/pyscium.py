import sys
import curses
from logger import pyscium_logger
from workspace_manager import WorkspaceManager

logger = pyscium_logger.get_logger(__name__, 'pyscium.log')


def init_curses():
    logger.info("init_curses()")
    stdscr = curses.initscr()
    curses.raw()
    curses.noecho()
    curses.cbreak()
    stdscr.keypad(True)
    return stdscr


def restore_terminal(stdscr):
    logger.info("restore_terminal()")
    curses.noraw()
    curses.nocbreak()
    stdscr.keypad(False)
    curses.echo()
    curses.endwin()


def main():
    logger.info("main()")
    stdscr = init_curses()
    filename = None
    if len(sys.argv) > 1:
        filename = sys.argv[1]
    wm = WorkspaceManager(stdscr, filename)
    try:
        wm.start()
    except KeyboardInterrupt:
        pass
    finally:
        logger.info("exiting pyscium")
        restore_terminal(stdscr)


if __name__ == "__main__":
    main()

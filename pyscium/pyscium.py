import curses
from logger import pyscium_logger
from workspace_manager import WorkspaceManager

logger = pyscium_logger.get_logger(__name__, 'pyscium.log')


def init_ncurses():
    logger.info("init_ncurses()")
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
    stdscr = init_ncurses()
    wm = WorkspaceManager(stdscr)
    try:
        logger.info("start()")
        wm.start()
    except KeyboardInterrupt:
        pass
    finally:
        logger.info("exiting pyscium")
        restore_terminal(stdscr)


if __name__ == "__main__":
    main()

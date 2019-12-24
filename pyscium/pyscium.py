import logging
import curses
from workspace_manager import WorkspaceManager


def get_logger():
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.DEBUG)
    formatter = logging.Formatter(
        '%(asctime)s %(name)-12s %(levelname)-8s %(message)s')
    fh = logging.FileHandler(filename='../logs/pyscium.log', mode='w')
    fh.setFormatter(formatter)
    logger.addHandler(fh)

    return logger


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


logger = get_logger()

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

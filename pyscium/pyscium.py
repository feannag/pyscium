import curses
import sys

from logger import pyscium_logger
from workspace_manager import WorkspaceManager

logger = pyscium_logger.get_logger(__name__, 'pyscium.log')


def init_curses():
    logger.info("init_curses()")
    curses.initscr()
    curses.raw()
    curses.noecho()
    curses.cbreak()


def restore_terminal():
    logger.info("restore_terminal()")
    curses.noraw()
    curses.nocbreak()
    curses.echo()
    curses.endwin()


def main():
    logger.info("main()")

    try:
        init_curses()
        filename = None

        if len(sys.argv) > 1:
            filename = sys.argv[1]
        wm = WorkspaceManager(filename)

        wm.start()

    except KeyboardInterrupt as e:
        logger.exception(e)

    except TypeError as e:
        logger.exception(e)

    except curses.error as e:
        logger.exception(e)

    finally:
        logger.info("exiting pyscium")
        restore_terminal()


if __name__ == "__main__":
    main()

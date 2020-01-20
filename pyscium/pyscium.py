import sys
import curses
from curses import wrapper
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

    except KeyboardInterrupt:
        pass

    except TypeError:
        pass

    except curses.error as e:
        logger.info(e)

    finally:
        logger.info("exiting pyscium")
        restore_terminal()


if __name__ == "__main__":
    main()

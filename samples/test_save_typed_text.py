import logging
import curses
import curses.textpad
import sys
import hashlib

logging.FileHandler(filename='samples.log', mode='w')
logging.basicConfig(filename='samples.log', level=logging.DEBUG)


def init_ncurses():
    stdscr = curses.initscr()
    curses.raw()
    curses.noecho()
    curses.cbreak()
    stdscr.keypad(True)
    return stdscr


def restore_terminal(stdscr):
    curses.noraw()
    curses.nocbreak()
    stdscr.keypad(False)
    curses.echo()
    curses.endwin()


def create_file():
    filename = sys.argv[1]
    file = open(filename, 'w', 1)
    return file


def compute_checksum(input_string):
    logging.info("computing checksum")
    checksum = hashlib.md5(input_string.encode('utf-8')).hexdigest()
    logging.info("DONE calculating checksum")
    return checksum


def is_file_modified(input_string, file_checksum):  # TODO: change name of method
    logging.info("checking if checksum are same")
    if compute_checksum(input_string) == file_checksum:
        logging.info("checksums are same")
        return False
    else:
        logging.info("input modified")
        return True


def main():
    stdscr = init_ncurses()
    file = create_file()
    file_checksum = hashlib.md5(open(file.name, 'rb').read()).hexdigest()
    input = []

    try:
        while True:
            ch = stdscr.getch()

            if ch == 24:
                logging.info("exiting pyscium")
                file.flush()
                file.close()
                sys.exit()
            elif ch == 19:
                input_string = ''.join(chr(i) for i in input)
                if is_file_modified(input_string, file_checksum):
                    logging.info("input: " + input_string)
                    logging.info("input modified, writing to file...")
                    file.seek(0);
                    file.write(input_string)
                    file.truncate()
                    logging.info("storing new checksum")
                    file_checksum = compute_checksum(input_string)
            else:
                stdscr.addch(ch)
                input.append(ch)

    except KeyboardInterrupt:
        pass
    finally:
        restore_terminal(stdscr)


if __name__ == "__main__":
    main()

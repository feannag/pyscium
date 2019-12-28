from logger import pyscium_logger
from utils import checksum_util
import curses


class Window:
    logger = pyscium_logger.get_logger(__name__, 'window.log')

    @staticmethod
    def new_win(height, width, begin_y, begin_x):
        local_window = curses.newwin(height, width, begin_y, begin_x)
        local_window.keypad(True)
        # local_window.box(0, 0)

        return local_window

    def set_current_cursor_coordinates(self):
        self.cursor_current_coordinates = curses.getsyx()

    def __init__(self, filename):
        self.main_window = Window.new_win(curses.LINES - 1, curses.COLS, 0, 0)
        self.filename = filename
        self.file = None
        self.file_checksum = None
        self.user_input = []
        self.cursor_current_coordinates = ()

    def display_file_contents(self):
        Window.logger.info('display_file()')
        data = self.file.read()
        Window.logger.info('data: ' + data)

        # also initialize user_input
        for i in data:
            self.user_input.append(ord(i))
        Window.logger.info(self.user_input)

        self.main_window.addstr(data)

    def is_file_modified(self, input_string):  # TODO: change name of method(is_buffer_modified/is_input_modified)
        Window.logger.info("checking if checksum are same")
        if checksum_util.compute_string_checksum(input_string) == self.file_checksum:
            Window.logger.info("checksums are same")
            return False
        else:
            Window.logger.info("input modified")
            return True

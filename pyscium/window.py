import curses
from pathlib import Path

from buffer import Buffer
from logger import pyscium_logger
from utils import file_util
from mini_window import MiniWindow


class Window:
    logger = pyscium_logger.get_logger(__name__, 'window.log')

    def __init__(self, filename=None):
        self.__main_window = curses.newwin(curses.LINES - 1, curses.COLS, 0, 0) # ht, wd, begin_y, begin_x
        self.__main_window.keypad(True)
        self.__mini_window = MiniWindow()
        self.__buffer = Buffer(filename)
        self.open_file_or_create_it()

    def get_window(self):
        return self.__main_window

    def add_ch(self, ch):
        self.__main_window.addch(ch)
        self.__buffer.add_ch(ch)

    def display_buffer_contents(self):
        data = self.__buffer.get_contents()

        try:
            for line in data:
                self.__main_window.addstr(line)
        except TypeError as e:
            Window.logger.info(e)

    def set_current_cursor_coordinates(self):
        self.__buffer.set_current_cursor_coordinates(curses.getsyx())

    def open_file_or_create_it(self):
        filename = self.__buffer.get_file_name()

        if filename is not None:
            if Path(filename).is_file():
                self.display_buffer_contents()
            else:
                file_util.create_file(self.__buffer.get_file_name())

    def save_file(self):
        self.set_current_cursor_coordinates()

        if self.__buffer.get_file_name() is not None:
            if self.__buffer.get_is_modified():
                self.__buffer.save_file()
                self.__mini_window.display_message_in_mini_buffer('Changes saved')
                self.restore_cursor()
            else:
                self.__mini_window.display_message_in_mini_buffer('no changes need to be saved')
                self.restore_cursor()

        else:
            filename = self.__mini_window.get_file_name()
            if filename is not None:
                file_path = Path(filename)
                if file_path.parent.exists():
                    file_util.create_file(file_path)
                    self.__buffer.set_file_name(file_path)
                    self.__buffer.save_file()
                    self.__mini_window.display_message_in_mini_buffer('Changes saved')

            self.restore_cursor()

    def close_file(self):
        if self.__buffer.get_file_name() is not None:
            file_util.close_file(self.__buffer.get_file_name())

    def restore_cursor(self):
        current_cursor_coordinates = self.__buffer.get_current_cursor_coordinates()
        self.__main_window.move(current_cursor_coordinates[0],
                                current_cursor_coordinates[1])

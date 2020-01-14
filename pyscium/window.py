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
        self.__maxy, self.__maxx = self.__main_window.getmaxyx()

        self.__mini_window = MiniWindow()
        self.__buffer = Buffer(filename)
        self.open_file_or_create_it()

    def _update_max_yx(self):
        maxy, maxx = self.__main_window.getmaxyx()
        self.__maxy = maxy - 1
        self.__maxx = maxx - 1

    def _end_of_line(self, y):
        self._update_max_yx()
        last = self.__maxx
        while True:
            if curses.ascii.ascii(self.__main_window.inch(y, last)) != curses.ascii.SP:
                last = min(self.__maxx, last+1)
                break
            elif last == 0:
                break
            last = last - 1
        return last

    def get_window(self):
        return self.__main_window

    def move_to_beginning_of_line(self):
        (y, x) = self.__main_window.getyx()
        self.__main_window.move(y, 0)

    def move_to_end_of_line(self):
        self._update_max_yx()
        (y, x) = self.__main_window.getyx()
        self.__main_window.move(y, self._end_of_line(y))

    def move_forward_one_char(self):
        (y, x) = self.__main_window.getyx()
        if x < self._end_of_line(y):
            self.__main_window.move(y, x + 1)
        elif y == self.__maxy:
            pass
        else:
            self.__main_window.move(y + 1, 0)

    def move_backward_one_char(self):
        (y, x) = self.__main_window.getyx()
        if x > 0:
            self.__main_window.move(y, x - 1)
        elif y == 0:
            pass
        else:
            self.__main_window.move(y - 1, 0)
            self.move_to_end_of_line()

    def move_to_next_line(self):
        (y, x) = self.__main_window.getyx()
        if y < self.__maxy:
            self.__main_window.move(y + 1, x)
            if x > self._end_of_line(y + 1):
                self.__main_window.move(y + 1, self._end_of_line(y + 1))

    def move_to_previous_line(self):
        (y, x) = self.__main_window.getyx()
        if y > 0:
            self.__main_window.move(y - 1, x)
            if x > self._end_of_line(y - 1):
                self.__main_window.move(y - 1, self._end_of_line(y - 1))

    def backspace(self):
        self.move_backward_one_char()
        self.__main_window.delch()

    def newline(self):
        ch = 10
        self.__main_window.addch(ch)

    def add_ch(self, ch):
        self.__main_window.insch(ch)
        self.move_forward_one_char()

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

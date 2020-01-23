import curses
from pathlib import Path

from buffer import Buffer
from logger import pyscium_logger
from utils import file_util
from mini_window import MiniWindow


class Window:
    logger = pyscium_logger.get_logger(__name__, 'window.log')

    def __init__(self, filename=None):
        self.__internal_window = curses.newwin(curses.LINES - 1, curses.COLS, 0, 0) # ht, wd, begin_y, begin_x
        self.__internal_window.keypad(True)
        self.__maxy, self.__maxx = self.__internal_window.getmaxyx()

        self.__mini_window = MiniWindow()
        self.__buffer = Buffer(filename)
        self.__current_cursor_coordinates = ()

        # represents the first line of the internal window
        self.__top = 0

        # represents the last line of the internal window
        self.__bottom = curses.LINES - 1

        self.__left = 0

        self.__right = curses.COLS

        # since current_line_number is used to index through the contents, it is initialized to 0
        self.__current_line_number = 0

        self.__current_line_character_number = 0

        self.open_file_or_create_it()

    def get_current_cursor_coordinates(self):
        return self.__current_cursor_coordinates

    def set_current_cursor_coordinates(self):
        self.__current_cursor_coordinates = curses.getsyx()

    def increment_top(self):
        self.__top += 1

    def decrement_top(self):
        if self.__top > 0:
            self.__top -= 1

    def increment_bottom(self):
        self.__bottom += 1

    def decrement_bottom(self):
        self.__bottom -= 1

    def set_left(self, left):
        self.__left = left

    def set_right(self, right):
        self.__right = right

    def increment_left(self):
        self.__left += 1

    def decrement_left(self):
        self.__left -= 1

    def increment_right(self):
        self.__right += 1

    def decrement_right(self):
        self.__right -= 1

    def get_current_line_number(self):
        return self.__current_line_number

    def increment_current_line_number(self):
        self.__current_line_number += 1

    def decrement_current_line_number(self):
        self.__current_line_number -= 1

    def get_current_line_character_number(self):
        return self.__current_line_character_number

    def set_current_line_character_number(self, character_number):
        self.__current_line_character_number = character_number

    def increment_current_line_character_number(self):
        self.__current_line_character_number += 1

    def decrement_current_line_character_number(self):
        self.__current_line_character_number -= 1

    def get_internal_window(self):
        return self.__internal_window

    def move_to_beginning_of_line(self):
        y, x = self.__internal_window.getyx()
        maxy, maxx = self.__internal_window.getmaxyx()

        self.set_left(0)
        self.set_right(maxx)
        self.set_current_line_character_number(0)

        self.display_buffer_contents()
        self.__internal_window.move(y, 0)

    def move_to_end_of_line(self):
        y, x = self.__internal_window.getyx()
        maxy, maxx = self.__internal_window.getmaxyx()
        current_line_number = self.get_current_line_number()

        current_line_length = self.__buffer.get_length_of_line(current_line_number) + 1  # +1 for \n

        if current_line_length > maxx:
            self.set_left(current_line_length - maxx)
            self.set_right(current_line_length)
            self.display_buffer_contents()
            self.__internal_window.move(y, maxx - 1)

        else:
            self.display_buffer_contents()
            self.__internal_window.move(y, current_line_length - 1)

        self.set_current_line_character_number(current_line_length - 1)  # -1 since it acts as an index

    def move_forward_one_char(self):
        y, x = self.__internal_window.getyx()
        maxy, maxx = self.__internal_window.getmaxyx()
        buffer_end_y, buffer_end_x = self.__buffer.get_buffer_end()
        current_line_number = self.get_current_line_number()

        current_line_character_number = self.get_current_line_character_number()
        x_of_last_character_of_line_on_y = self.__buffer.get_length_of_line(current_line_number)

        if x < maxx - 1 and current_line_character_number < x_of_last_character_of_line_on_y:
            self.__internal_window.move(y, x + 1)
            self.increment_current_line_character_number()

        elif x == maxx - 1 and current_line_character_number < x_of_last_character_of_line_on_y:
            self.increment_left()
            self.increment_right()
            self.increment_current_line_character_number()
            self.display_buffer_contents()

            self.__internal_window.move(y, maxx - 1)

        elif current_line_number == buffer_end_y:
            curses.beep()

        else:
            self.move_to_next_line()
            self.set_current_line_character_number(0)

    def move_backward_one_char(self):
        y, x = self.__internal_window.getyx()
        buffer_start_y, buffer_start_x = self.__buffer.get_buffer_start()
        current_line_number = self.get_current_line_number()
        current_line_character_number = self.get_current_line_character_number()

        if x > 0:
            self.__internal_window.move(y, x - 1)
            self.decrement_current_line_character_number()

        elif x == 0 and current_line_character_number > 0:
            self.decrement_left()
            self.decrement_right()
            self.decrement_current_line_character_number()
            self.display_buffer_contents()

            self.__internal_window.move(y, 0)

        elif current_line_number == buffer_start_y:
            curses.beep()

        else:
            self.move_to_previous_line()
            self.move_to_end_of_line()
            current_line_number = self.get_current_line_number()
            current_line_character_number = self.__buffer.get_length_of_line(current_line_number)
            self.set_current_line_character_number(current_line_character_number)

    def move_to_next_line(self):
        y, x = self.__internal_window.getyx()
        maxy, maxx = self.__internal_window.getmaxyx()
        current_line_number = self.get_current_line_number()
        buffer_end_y, buffer_end_x = self.__buffer.get_buffer_end()

        if current_line_number != buffer_end_y:

            next_line_y = y + 1
            main_window_height = curses.LINES - 1

            if next_line_y == main_window_height:
                self.increment_top()
                self.increment_bottom()

                self.display_buffer_contents()
                self.__internal_window.move(y, 0)

            else:
                self.set_left(0)
                self.set_right(maxx)
                self.set_current_line_character_number(0)
                self.display_buffer_contents()
                self.__internal_window.move(y + 1, 0)

            if current_line_number < buffer_end_y:
                self.increment_current_line_number()

        else:
            curses.beep()

    def move_to_previous_line(self):
        y, x = self.__internal_window.getyx()

        current_line_number = self.get_current_line_number()
        (buffer_start_y, buffer_start_x) = self.__buffer.get_buffer_start()
        if current_line_number != buffer_start_y:

            prev_line_y = y - 1

            if prev_line_y == -1:
                self.decrement_top()
                self.decrement_bottom()

                self.display_buffer_contents()
                self.__internal_window.move(0, 0)

            else:
                self.__internal_window.move(y - 1, 0)

            if current_line_number > buffer_start_y:
                self.decrement_current_line_number()

        else:
            curses.beep()

    def backspace(self):
        y, x = self.__internal_window.getyx()
        maxy, maxx = self.__internal_window.getmaxyx()
        current_line_number = self.get_current_line_number()
        current_line_character_number = self.get_current_line_character_number()
        length_of_line_to_append_to = self.__buffer.get_length_of_line(current_line_number - 1)
        prev_line_y = current_line_number - 1

        if y > 0 and x > 0:
            self.move_backward_one_char()
            self.__internal_window.delch()
            self.__buffer.delete_character(current_line_number, current_line_character_number - 1)

            self.display_buffer_contents()
            self.__internal_window.move(y, x - 1)
        elif y > 0 and x == 0:
            if self.__buffer.get_length_of_line(current_line_number - 1) > maxx:
                self.set_left(self.__buffer.get_length_of_line(current_line_number - 1) - int(maxx / 2))
                self.set_right(self.__buffer.get_length_of_line(current_line_number - 1) + int(maxx / 2))

                self.__buffer.remove_line_and_append_at_position(current_line_number, current_line_number - 1)
                self.set_current_line_character_number(length_of_line_to_append_to)
                self.decrement_current_line_number()

                self.display_buffer_contents()
                self.__internal_window.move(prev_line_y, int(maxx / 2))
            else:
                self.__buffer.remove_line_and_append_at_position(current_line_number, current_line_number - 1)
                self.set_current_line_character_number(length_of_line_to_append_to)
                self.decrement_current_line_number()

                self.display_buffer_contents()
                self.__internal_window.move(prev_line_y, length_of_line_to_append_to)
        elif y == 0 and x > 0:
            self.move_backward_one_char()
            self.__internal_window.delch()
            self.__buffer.delete_character(current_line_number, current_line_character_number - 1)

            self.display_buffer_contents()
            self.__internal_window.move(y, x - 1)
        elif current_line_character_number > 0 and x == 0:
            self.decrement_left()
            self.decrement_right()
            self.decrement_current_line_character_number()

            self.display_buffer_contents()
            self.__internal_window.move(y, 0)
        elif y == 0 and current_line_number != 0:
            self.set_left(self.__buffer.get_length_of_line(current_line_number - 1) - int(maxx / 2))
            self.set_right(self.__buffer.get_length_of_line(current_line_number - 1) + int(maxx / 2))

            self.__buffer.remove_line_and_append_at_position(current_line_number, current_line_number - 1)
            self.set_current_line_character_number(length_of_line_to_append_to)
            self.decrement_current_line_number()

            self.decrement_top()
            self.decrement_bottom()

            self.display_buffer_contents()
            self.__internal_window.move(prev_line_y, int(maxx / 2))
        elif current_line_number == 0 and x == 0:
            curses.beep()

    def newline(self):
        newline = 10
        main_window_height = curses.LINES - 1
        maxy, maxx = self.__internal_window.getmaxyx()
        y, x = self.__internal_window.getyx()
        next_line_y = y + 1
        next_line_x = 0
        current_line_number = self.get_current_line_number()
        current_line_character_number = self.get_current_line_character_number()
        self.__internal_window.insch(newline)
        self.__buffer.ins_ch(newline, current_line_number, current_line_character_number)

        self.__buffer.move_current_line_to_next_line(current_line_number, current_line_character_number + 1)
        self.set_left(0)
        self.set_right(maxx)
        self.set_current_line_character_number(0)
        self.increment_current_line_number()

        if next_line_y == main_window_height:
            self.increment_top()
            self.increment_bottom()

        self.display_buffer_contents()

        if next_line_y != main_window_height:
            self.__internal_window.move(next_line_y, next_line_x)

        else:
            self.__internal_window.move(y, 0)

    def ins_ch(self, ch):
        y, x = self.__internal_window.getyx()
        current_line_number = self.get_current_line_number()
        current_line_character_number = self.get_current_line_character_number()
        self.__internal_window.insch(ch)
        self.__buffer.ins_ch(ch, current_line_number, current_line_character_number)

        self.move_forward_one_char()

    def display_buffer_contents(self):
        self.__internal_window.erase()

        data = self.__buffer.get_contents()
        try:
            for index, line in enumerate(data[self.__top : self.__bottom]):
                string = ''.join(line[self.__left : self.__right])

                if string:
                    self.__internal_window.addstr(string)
                else:
                    self.__internal_window.addstr('\n')

        except TypeError as e:
            Window.logger.exception(e)

        except curses.error as e:
            Window.logger.exception(e)

    def open_file_or_create_it(self):
        filename = self.__buffer.get_file_name()

        if filename is not None:
            if Path(filename).is_file():
                self.display_buffer_contents()
                self.__internal_window.move(0, 0)

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
                self.__mini_window.display_message_in_mini_buffer('No changes need to be saved')
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
        current_cursor_coordinates = self.get_current_cursor_coordinates()
        self.__internal_window.move(current_cursor_coordinates[0],
                                    current_cursor_coordinates[1])

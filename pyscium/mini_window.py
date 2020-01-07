import curses
from curses.textpad import Textbox


class MiniWindow:
    def __init__(self):
        self.__mini_window = curses.newwin(1, curses.COLS, curses.LINES - 1, 0)
        self.__mini_window.keypad(True)
        self.__mini_window_tb = Textbox(self.__mini_window)

    def display_message_in_mini_buffer(self, msg):
        self.__mini_window.erase()
        self.__mini_window.addstr(msg)
        self.__mini_window.refresh()

    def get_file_name(self):
        self.display_message_in_mini_buffer('file to save in: ')

        filename = ""
        while True:
            mini_buffer_ch = self.__mini_window.getch()
            if mini_buffer_ch == 24:
                self.__mini_window.erase()
                self.__mini_window.refresh()
                return None

            elif mini_buffer_ch == 10:
                return filename

            else:
                self.__mini_window_tb.do_command(mini_buffer_ch)
                filename += chr(mini_buffer_ch)

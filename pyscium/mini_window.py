import curses
from curses.textpad import Textbox


class MiniWindow:
    @staticmethod
    def new_win(height, width, begin_y, begin_x):
        local_window = curses.newwin(height, width, begin_y, begin_x)
        local_window.keypad(True)
        # local_window.box(0, 0)

        return local_window

    def __init__(self):
        self.mini_window = MiniWindow.new_win(1, curses.COLS, curses.LINES-1, 0)
        self.mini_window_tb = Textbox(self.mini_window)
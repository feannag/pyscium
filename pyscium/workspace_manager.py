from logger import pyscium_logger
import sys
from pathlib import Path
from utils import checksum_util
from utils import file_util
from window import Window
from mini_window import MiniWindow
import os


class WorkspaceManager(object):
    logger = pyscium_logger.get_logger(__name__, 'workspace_manager.log')

    def __init__(self, filename):
        self.window = Window(filename)
        self.mini_window = MiniWindow()

    def start(self):
        WorkspaceManager.logger.info("start()")

        if self.window.filename is None:
            pass

        else:
            if Path(self.window.filename).is_file():
                self.window.file = file_util.open_file(self.window.filename)
                self.window.display_file_contents()
                self.window.file_checksum = checksum_util.compute_file_checksum(self.window.file)
            else:
                self.window.file = file_util.create_file(self.window.filename)
                self.window.file_checksum = checksum_util.compute_file_checksum(self.window.file)

        while True:
            ch = self.window.main_window.getch()

            if ch == 24:
                if self.window.file is not None:
                    self.window.file.flush()
                    self.window.file.close()
                sys.exit()
            elif ch == 19:
                self.window.set_current_cursor_coordinates()
                input_string = ''.join(chr(i) for i in self.window.user_input)
                if self.window.file is not None:
                    if self.window.is_file_modified(input_string):
                        file_util.write_contents_to_file(input_string, self.window.file)

                        self.mini_window.mini_window.erase()
                        self.mini_window.mini_window.addstr('Changes saved')
                        self.mini_window.mini_window.refresh()
                        self.window.main_window.move(self.window.cursor_current_coordinates[0],
                                                     self.window.cursor_current_coordinates[1])

                        self.window.file_checksum = checksum_util.compute_string_checksum(input_string)
                    else:
                        self.mini_window.mini_window.erase()
                        self.mini_window.mini_window.addstr('No changes need to be saved')
                        self.mini_window.mini_window.refresh()
                        self.window.main_window.move(self.window.cursor_current_coordinates[0],
                                                     self.window.cursor_current_coordinates[1])
                else:
                    self.mini_window.mini_window.erase()
                    self.mini_window.mini_window.addstr('file to save in: ')
                    self.mini_window.mini_window.refresh()

                    mini_buffer_input = ""
                    while True:
                        mini_buffer_ch = self.mini_window.mini_window.getch()
                        if mini_buffer_ch == 24:
                            self.mini_window.mini_window.erase()
                            self.mini_window.mini_window.refresh()
                            self.window.main_window.move(0, 0)
                            break
                        elif mini_buffer_ch == 10:
                            # check if Path(file_name) : save ? don't save
                            WorkspaceManager.logger.info("mini_buffer_input: " + mini_buffer_input)
                            file_path = Path(mini_buffer_input)
                            WorkspaceManager.logger.info("file_path: " + os.fspath(file_path))
                            if file_path.parent.exists():
                                self.window.file = file_util.create_file(file_path)
                                WorkspaceManager.logger.info("file_path.name: " + file_path.name)
                                file_util.write_contents_to_file(input_string, self.window.file)

                                self.mini_window.mini_window.erase()
                                self.mini_window.mini_window.addstr('Changes saved')
                                self.mini_window.mini_window.refresh()
                                self.window.main_window.move(self.window.cursor_current_coordinates[0],
                                                             self.window.cursor_current_coordinates[1])

                                self.window.file_checksum = checksum_util.compute_file_checksum(self.window.file)

                        else:
                            self.mini_window.mini_window_tb.do_command(mini_buffer_ch)
                            mini_buffer_input += chr(mini_buffer_ch)
                            WorkspaceManager.logger.info(f'mini_buffer_input: {mini_buffer_input}')
            else:
                self.window.main_window.addch(ch)
                self.window.user_input.append(ch)

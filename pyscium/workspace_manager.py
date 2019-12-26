from logger import pyscium_logger
import sys
from pathlib import Path
from utils import checksum_util
from utils import file_util
from window import Window


class WorkspaceManager(object):
    logger = pyscium_logger.get_logger(__name__, 'workspace_manager.log')

    def __init__(self, stdscr, filename):
        self.window = Window(stdscr, filename)

    def start(self):
        WorkspaceManager.logger.info("start()")

        #  check if argument(filename) is passed;
        #  if no, allow user to save contents of buffer
        if self.window.filename is None:
            # TODO: complete this
            pass

        # if yes, check if that file exists; if it exists, display contents; if no, create a new file
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
                input_string = ''.join(chr(i) for i in self.window.user_input)
                if self.window.file is not None:
                    if self.window.is_file_modified(input_string):
                        file_util.write_contents_to_file(input_string, self.window.file)
                        WorkspaceManager.logger.info("storing new checksum")
                        self.window.file_checksum = checksum_util.compute_string_checksum(input_string)
            else:
                self.window.main_window.addch(ch)
                self.window.user_input.append(ch)

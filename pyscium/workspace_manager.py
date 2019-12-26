from logger import pyscium_logger
import sys
from pathlib import Path
from utils import checksum_util
from utils import file_util


class WorkspaceManager(object):
    logger = None

    def __init__(self, stdscr, filename):
        WorkspaceManager.logger = pyscium_logger.get_logger(__name__, 'workspace_manager.log')
        self.filename = filename
        self.stdscr = stdscr
        self.file = None
        self.file_checksum = None
        self.user_input = []

    def display_file_contents(self):
        WorkspaceManager.logger.info('display_file()')
        data = self.file.read()
        WorkspaceManager.logger.info('data: ' + data)

        # also initialize user_input
        for i in data:
            self.user_input.append(ord(i))
        WorkspaceManager.logger.info(self.user_input)

        self.stdscr.addstr(data)

    def is_file_modified(self, input_string):  # TODO: change name of method(is_buffer_modified/is_input_modified)
        WorkspaceManager.logger.info("checking if checksum are same")
        if checksum_util.compute_string_checksum(input_string) == self.file_checksum:
            WorkspaceManager.logger.info("checksums are same")
            return False
        else:
            WorkspaceManager.logger.info("input modified")
            return True

    def start(self):
        WorkspaceManager.logger.info("start()")

        #  check if argument(filename) is passed;
        #  if no, allow user to save contents of buffer
        if self.filename is None:
            # TODO: complete this
            pass

        # if yes, check if that file exists; if it exists, display contents; if no, create a new file
        else:
            if Path(self.filename).is_file():
                self.file = file_util.open_file(self.filename)
                self.display_file_contents()
                self.file_checksum = checksum_util.compute_file_checksum(self.file)
            else:
                self.file = file_util.create_file(self.filename)
                self.file_checksum = checksum_util.compute_file_checksum(self.file)

        while True:
            ch = self.stdscr.getch()

            if ch == 24:
                if self.file is not None:
                    self.file.flush()
                    self.file.close()
                sys.exit()
            elif ch == 19:
                input_string = ''.join(chr(i) for i in self.user_input)
                if self.file is not None:
                    if self.is_file_modified(input_string):
                        file_util.write_contents_to_file(input_string, self.file)
                        WorkspaceManager.logger.info("storing new checksum")
                        self.file_checksum = checksum_util.compute_string_checksum(input_string)
            else:
                self.stdscr.addch(ch)
                self.user_input.append(ch)

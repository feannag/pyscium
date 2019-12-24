from logger import pyscium_logger
import sys
import hashlib
from pathlib import Path


class WorkspaceManager(object):
    logger = None

    def __init__(self, stdscr):
        WorkspaceManager.logger = pyscium_logger.get_logger(__name__, 'workspace_manager.log')
        self.stdscr = stdscr
        self.file = None
        self.file_checksum = None
        self.user_input = []

    def open_file(self, filename):
        WorkspaceManager.logger.info('open_file()')
        self.file = open(filename, 'r+')
        # file = open(filename, 'r+', 1)

    def create_file(self, filename):
        WorkspaceManager.logger.info('create_file')
        self.file = open(filename, 'x')

    def display_file_contents(self):
        WorkspaceManager.logger.info('display_file()')
        data = self.file.read()
        WorkspaceManager.logger.info('data: ' + data)

        # also initialize user_input
        for i in data:
            self.user_input.append(ord(i))
        WorkspaceManager.logger.info(self.user_input)

        self.stdscr.addstr(data)

    def write_contents_to_file(self, string):
        WorkspaceManager.logger.info("writing to file")
        # logger.info("input: " + input_string)
        self.file.seek(0)
        self.file.write(string)
        self.file.truncate()

    def compute_checksum(self, input_string):
        WorkspaceManager.logger.info("computing checksum")
        checksum = hashlib.md5(input_string.encode('utf-8')).hexdigest()
        WorkspaceManager.logger.info("DONE calculating checksum")
        return checksum

    def is_file_modified(self, input_string):  # TODO: change name of method(is_buffer_modified/is_input_modified)
        WorkspaceManager.logger.info("checking if checksum are same")
        if self.compute_checksum(input_string) == self.file_checksum:
            WorkspaceManager.logger.info("checksums are same")
            return False
        else:
            WorkspaceManager.logger.info("input modified")
            return True

    def start(self):
        #  TODO: check if argument is passed;
        #  TODO: if no, allow user to save contents of buffer
        if not len(sys.argv) > 1:
            # TODO: complete this
            pass

        # TODO: if yes, check if that file exists; if it exists, display contents; if no, create a new file
        else:
            if Path(sys.argv[1]).is_file():
                self.open_file(sys.argv[1])
                self.display_file_contents()
                self.file_checksum = hashlib.md5(open(self.file.name, 'rb').read()).hexdigest()
            else:
                self.create_file(sys.argv[1])
                self.file_checksum = hashlib.md5(open(self.file.name, 'rb').read()).hexdigest()

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
                        self.write_contents_to_file(input_string)
                        WorkspaceManager.logger.info("storing new checksum")
                        self.file_checksum = self.compute_checksum(input_string)
            else:
                self.stdscr.addch(ch)
                self.user_input.append(ch)

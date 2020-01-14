from utils import file_util
from logger import pyscium_logger


class Buffer:
    logger = pyscium_logger.get_logger(__name__, 'buffer.log')

    def __init__(self, filename=None):
        self.__buffer_name = filename
        self.__file_name = filename
        self.__contents = []
        self.__is_modified = False
        self.__current_cursor_coordinates = ()

        if filename is not None:
            self.__contents = file_util.get_file_contents(filename)

    def get_buffer_name(self):
        return self.__buffer_name

    def set_buffer_name(self, buffer_name):
        self.__buffer_name = buffer_name

    def get_file_name(self):
        return self.__file_name

    def set_file_name(self, filename):
        self.__file_name = filename

    def get_contents(self):
        return self.__contents

    def set_contents(self):
        self.__contents = file_util.get_file_contents(self.__file_name)

    def add_ch(self, ch):
        self.__contents.append(chr(ch))
        self.set_is_modified(True)

    def get_current_cursor_coordinates(self):
        return self.__current_cursor_coordinates

    def set_current_cursor_coordinates(self, coordinates):
        self.__current_cursor_coordinates = coordinates

    def get_is_modified(self):
        return self.__is_modified

    def set_is_modified(self, flag):
        self.__is_modified = flag

    def save_file(self):
        if self.__is_modified:
            file_util.write_data_to_file(self.__file_name, self.get_contents())
            self.set_is_modified(False)

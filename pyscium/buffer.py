from utils import file_util
from logger import pyscium_logger


class Buffer:
    logger = pyscium_logger.get_logger(__name__, 'buffer.log')

    def __init__(self, filename=None):
        self.__buffer_name = filename
        self.__file_name = filename
        self.__contents = []
        self.__is_modified = False
        self.__buffer_start = (0, 0)
        self.__buffer_end = (0, 0)

        if filename is not None:
            self._init_buffer_contents(filename)

    def _init_buffer_contents(self, filename):
        for line in file_util.get_file_contents(filename):
            temp_list = []
            for character in line:
                temp_list.append(character)
            self.__contents.append(temp_list)

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

    def get_is_modified(self):
        return self.__is_modified

    def set_is_modified(self, flag):
        self.__is_modified = flag

    def get_buffer_start(self):
        return self.__buffer_start

    def get_buffer_end(self):
        # this is to ensure you get updated values
        self._update_buffer_end()

        return self.__buffer_end

    def _update_buffer_end(self):
        y = len(self.__contents) - 1
        x = len(self.__contents[len(self.__contents) - 1]) - 1

        self.__buffer_end = (y, x)

    def add_ch(self, ch, current_line_number, current_line_character_number):
        try:
            if ch != 10:
                self.__contents[current_line_number].insert(current_line_character_number, chr(ch))

            elif self.__contents[current_line_number][current_line_character_number] != '\n':
                self.__contents[current_line_number].insert(current_line_character_number, chr(ch))

        except IndexError:
            self.__contents.append([])
            self.__contents[current_line_number].insert(current_line_character_number, chr(ch))

        self.set_is_modified(True)

    def save_file(self):
        if self.__is_modified:
            file_util.write_data_to_file(self.__file_name, self.get_contents())
            self.set_is_modified(False)

    def delete_character(self, y, x):
        try:
            del self.__contents[y][x]

        except IndexError:
            del self.__contents[y]

        self.set_is_modified(True)

    def get_length_of_line(self, line_number):
        try:
            number_of_lines_in_buffer = len(self.__contents)
            if line_number <= number_of_lines_in_buffer:

                number_of_characters_in_line = len(self.__contents[line_number])
                if number_of_characters_in_line > 0:

                    number_of_characters_in_line_less_newline = number_of_characters_in_line - 1
                    return number_of_characters_in_line_less_newline

                else:
                    return 0

        except IndexError as e:
            Buffer.logger.info(e)

    def remove_line_and_append_at_position(self, current_line_number, position):
        try:
            if '\n' in self.__contents[position]:
                del self.__contents[position][-1]

            self.__contents[position].extend(self.__contents[current_line_number])
            del self.__contents[current_line_number]
            self.set_is_modified(True)

        except IndexError:
            pass

    def get_length_of_line_after_append(self, current_line_number):
        return self.get_length_of_line(current_line_number) + self.get_length_of_line(current_line_number - 1)

    def move_current_line_to_next_line(self, current_line_number, current_line_character_number):
        line_under_cursor = self.__contents[current_line_number]
        contents_after_cursor = line_under_cursor[current_line_character_number:]

        # check if contents_after_cursor is empty; if yes, append a newline
        if not contents_after_cursor:
            contents_after_cursor.insert(0, '\n')

        # insert those contents in the next line
        self.__contents.insert(current_line_number + 1, contents_after_cursor)

        # remove those contents from buffer
        self.__contents[current_line_number] = line_under_cursor[:current_line_character_number]

        self.set_is_modified(True)

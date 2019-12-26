
def open_file(filename):
    # logger.info('open_file()')
    file = open(filename, 'r+')
    return file
    # file = open(filename, 'r+', 1)


def create_file(filename):
    # logger.info('create_file')
    file = open(filename, 'x')
    return file


def write_contents_to_file(string, file):
    # logger.info("writing to file")
    # logger.info("input: " + string)
    file.seek(0)
    file.write(string)
    file.truncate()
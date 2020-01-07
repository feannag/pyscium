from pathlib import Path
from logger import pyscium_logger

logger = pyscium_logger.get_logger(__name__, 'file_util.log')


def create_file(filename):
    try:
        open(filename, 'x')
    except FileExistsError as e:
        logger.info(e)


def open_file(filename):
    if Path(filename).is_file():
        file = open(filename, 'r+')
        return file
    else:
        return None


def get_file_contents(filename):
    file = open_file(filename)

    return file.readlines()


def write_data_to_file(filename, data):
    file = open_file(filename)
    if file is not None:
        file.seek(0)
        for line in data:
            file.write(line)
        file.truncate()


def close_file(filename):
    file = open_file(filename)
    if file is not None:
        file.flush()
        file.close()

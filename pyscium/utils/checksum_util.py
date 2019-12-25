import hashlib


# TODO: need to add a logger
def compute_string_checksum(input_string):
    # logger.info("computing checksum")
    checksum = hashlib.md5(input_string.encode('utf-8')).hexdigest()
    # logger.info("calculating checksum...DONE")
    return checksum


def compute_file_checksum(file):
    checksum = hashlib.md5(open(file.name, 'rb').read()).hexdigest()
    return checksum

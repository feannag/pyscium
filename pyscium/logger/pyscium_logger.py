import logging


def get_logger(name, filename):
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)
    formatter = logging.Formatter(
        '%(asctime)s %(name)-12s %(levelname)-8s %(message)s')
    fh = logging.FileHandler(filename='./logs/' + filename, mode='w')
    fh.setFormatter(formatter)
    logger.addHandler(fh)

    return logger

import logging


def get_logger(mod_name: str):
    log = logging.getLogger(mod_name)
    log.setLevel(logging.DEBUG)
    return log

import logging

def get_logger():
    logger = logging.getLogger("gmail_unsub")
    logger.setLevel(logging.DEBUG)
    return logger


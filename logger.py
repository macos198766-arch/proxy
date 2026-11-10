import logging
import sys
from config import FILE_NAME, LOG_LEVEL

def setup_logger():
    logger = logging.getLogger("proxy")

    if logger.hasHandlers():
        return logger
    logger.setLevel(getattr(logging, LOG_LEVEL))
    file_handler = logging.FileHandler(FILE_NAME, encoding="utf-8")
    console_handler = logging.StreamHandler(sys.stdout)
    formatter = logging.Formatter('%(asctime)s – %(name)s – %(levelname)s – %(message)s')
    file_handler.setFormatter(formatter)
    console_handler.setFormatter(formatter)

    logger.addHandler(file_handler)
    logger.addHandler(console_handler)
    return logger

logger = setup_logger()
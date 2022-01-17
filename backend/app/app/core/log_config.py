import logging
import sys


def init_loggers():
    """Configure loggers."""
    logger = logging.getLogger("app")
    logger.setLevel(logging.DEBUG)

    stdout_handler = logging.StreamHandler(sys.stdout)
    stdout_format = "[%(asctime)s - %(levelname)s - %(filename)s:%(lineno)s - %(funcName)20s() ] %(message)s"
    formatter = logging.Formatter(stdout_format)
    stdout_handler.setFormatter(formatter)
    logger.addHandler(stdout_handler)

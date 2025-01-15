import logging
import os
from sys import stdout

from config import DATA_DIR

LOG_DIR = DATA_DIR / "log"
EXCEPTIONS_FILE = LOG_DIR / "exception_log.log"
STREAM_LOGGER = "STREAM"
FILE_LOGGER = "FILE"

if not os.path.exists(EXCEPTIONS_FILE):
    with open(EXCEPTIONS_FILE, "w"):
        pass

stream_logger = logging.getLogger(STREAM_LOGGER)

sl_stream_handler = logging.StreamHandler(stream=stdout)
sl_formatter = logging.Formatter("%(asctime)s [%(levelname)s] %(message)s")

sl_stream_handler.setFormatter(sl_formatter)
stream_logger.addHandler(sl_stream_handler)

file_logger = logging.getLogger(FILE_LOGGER)

fl_file_handler = logging.FileHandler(
    filename=DATA_DIR / "log" / "exception_log.log", mode="a"
)
fl_formatter = logging.Formatter("%(asctime)s [%(levelname)s] %(message)s")
fl_file_handler.setFormatter(fl_formatter)
file_logger.addHandler(fl_file_handler)


file_logger.setLevel(logging.INFO)
stream_logger.setLevel(logging.INFO)

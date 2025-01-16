import logging
import os

from config import DATA_DIR

LOG_DIR = DATA_DIR / "log"
REQUESTS_LOG_FILE = LOG_DIR / "requests.log"
EXCEPTIONS_LOG_FILE = LOG_DIR / "exceptions.log"
REQUESTS_LOGGER = "REQUESTS"
EXCEPTIONS_LOGGER = "EXCEPTIONS"

for path in [REQUESTS_LOG_FILE, EXCEPTIONS_LOG_FILE]:
    if not os.path.exists(path):
        with open(path, "w"):
            pass

# requests logger
request_logger = logging.getLogger(REQUESTS_LOGGER)

request_log_fh = logging.FileHandler(filename=REQUESTS_LOG_FILE, mode="a")
request_log_fmt = logging.Formatter("%(asctime)s [%(levelname)s] %(message)s")
request_log_fh.setFormatter(request_log_fmt)
request_logger.addHandler(request_log_fh)

# exceptions logger
exceptions_logger = logging.getLogger(EXCEPTIONS_LOGGER)

exceptions_log_fh = logging.FileHandler(filename=EXCEPTIONS_LOG_FILE, mode="a")
exceptions_log_fmt = logging.Formatter("%(asctime)s [%(levelname)s] %(message)s")
exceptions_log_fh.setFormatter(exceptions_log_fmt)
exceptions_logger.addHandler(exceptions_log_fh)

request_logger.setLevel(logging.INFO)
exceptions_logger.setLevel(logging.ERROR)

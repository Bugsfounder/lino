import logging
import inspect
from datetime import datetime


class Logger:
    def __init__(self, log_file="app.log"):
        self.log_file = log_file
        logging.basicConfig(
            filename=self.log_file,
            filemode="a",
            format="%(asctime)s | %(levelname)s | %(pathname)s:%(lineno)d | %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S",
            level=logging.DEBUG,
        )

    def log(self, message, level="info"):
        frame = inspect.stack()[1]
        pathname = frame.filename
        lineno = frame.lineno
        log_msg = f"{pathname}:{lineno} | {message}"

        if level == "debug":
            logging.debug(log_msg)
        elif level == "warning":
            logging.warning(log_msg)
        elif level == "error":
            logging.error(log_msg)
        elif level == "critical":
            logging.critical(log_msg)
        else:
            logging.info(log_msg)

    def log_to_file(self, custom_msg):
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        frame = inspect.stack()[1]
        full_path = frame.filename
        line = frame.lineno

        with open(self.log_file, "a") as f:
            f.write(f"{timestamp} | {full_path}:{line} | {custom_msg}\n")

import os
import logging
from logging.handlers import RotatingFileHandler

class Logger:
    def __init__(self, name='TestLogger', prod=False, max_bytes=2*1024*1024, backup_count=3):
        """
        :param name: Logger name
        :param prod: If True, use production log path and INFO level
        :param max_bytes: Max log file size before rotation (default 2MB)
        :param backup_count: Number of rotated log files to keep
        """
        base_dir = os.path.expanduser("~/.local/share/TestLogger/logs") if prod else "logs"
        os.makedirs(base_dir, exist_ok=True)
        log_file = os.path.join(base_dir, "app.log")

        self.logger = logging.getLogger(name)
        self.logger.setLevel(logging.DEBUG if not prod else logging.INFO)
        self.logger.propagate = False  # Prevent duplicate logs if root logger is configured

        # Remove existing handlers to avoid duplicate logs in interactive/test runs
        if self.logger.hasHandlers():
            self.logger.handlers.clear()

        # Rotating file handler for log rotation
        handler = RotatingFileHandler(log_file, maxBytes=max_bytes, backupCount=backup_count)
        handler.setLevel(logging.DEBUG if not prod else logging.INFO)
        formatter = logging.Formatter('%(asctime)s | %(levelname)s | %(pathname)s:%(lineno)s | %(funcName)s() | %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S')
        handler.setFormatter(formatter)
        self.logger.addHandler(handler)

        # Also log to console in dev mode
        if not prod:
            console = logging.StreamHandler()
            console.setLevel(logging.DEBUG)
            console.setFormatter(formatter)
            self.logger.addHandler(console)

    def debug(self, msg, *args, **kwargs): self.logger.debug(msg, *args, **kwargs)
    def info(self, msg, *args, **kwargs): self.logger.info(msg, *args, **kwargs)
    def warning(self, msg, *args, **kwargs): self.logger.warning(msg, *args, **kwargs)
    def error(self, msg, *args, **kwargs): self.logger.error(msg, *args, **kwargs)
    def critical(self, msg, *args, **kwargs): self.logger.critical(msg, *args, **kwargs)

    def pLog():
        return Logger(prod=True)
    def dLog():
        return Logger(prod=True)
# --- Test code ---

def test_logs(prod):
    print(f"\nTesting {'PRODUCTION' if prod else 'DEVELOPMENT'} mode logging\n")
    log = Logger(prod=prod)
    log.debug("This is a DEBUG message")
    log.info("This is an INFO message")
    log.warning("This is a WARNING message")
    log.error("This is an ERROR message")
    log.critical("This is a CRITICAL message")

if __name__ == "__main__":
    # Test dev mode
    test_logs(prod=False)

    # Test prod mode
    test_logs(prod=True)

    print("\nCheck the logs folder (dev) or ~/.local/share/TestLogger/logs (prod) for app.log")
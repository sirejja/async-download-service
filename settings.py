import os


DEFAULT_LOG_LEVEL = "INFO"
DEFAULT_DELAY = 0.01
DEFAULT_STORAGE_PATH = f'{os.getcwd()}/test_photos/'

LOG_LEVELS = (
    "CRITICAL",
    "FATAL",
    "ERROR",
    "WARNING",
    "WARN",
    "INFO",
    "DEBUG",
    "NOTSET",
)

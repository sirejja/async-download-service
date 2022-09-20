import argparse
import settings
import os


def get_args():
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "-s", "--storage",
        help="Path to storage",
        required=False,
        type=str,
        default=os.getenv("STORAGE", settings.DEFAULT_STORAGE_PATH),
    )

    parser.add_argument(
        "-d", "--delay",
        help="Delay of receiving chunks in seconds",
        required=False,
        type=float,
        default=os.getenv("DELAY", settings.DEFAULT_DELAY),
    )

    parser.add_argument(
        "-l", "--log",
        help="Loging level",
        required=False,
        type=str,
        choices=settings.LOG_LEVELS,
        default=os.getenv("LOG_LEVEL", settings.DEFAULT_LOG_LEVEL),
    )

    return parser.parse_args()
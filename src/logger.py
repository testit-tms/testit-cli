import logging


class Logger:
    """Class representing a logger factory"""

    @staticmethod
    def register_logger(is_debug: bool):
        """Function registers loggers."""

        logging.basicConfig(
            format="%(asctime)s (%(levelname)s) [%(filename)s.%(funcName)s] %(message)s"
            if is_debug
            else "%(message)s",
            datefmt="%Y-%m-%d %H:%M:%S",
            level=logging.DEBUG if is_debug else logging.INFO,
        )

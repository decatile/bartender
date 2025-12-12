import logging.config

from rich.logging import RichHandler


def setup_logging(verbosity: int) -> None:
    level = None

    match verbosity:
        case 0:
            level = logging.WARN
        case 1:
            level = logging.INFO
        case 2:
            level = logging.DEBUG
        case _:
            raise ValueError

    global L
    L.setLevel(level)


L = logging.Logger('reqresolve')
L.addHandler(RichHandler())

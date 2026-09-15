import logging

from rich.logging import RichHandler


def setup_logging(verbosity: int) -> None:
    level = None

    match verbosity:
        case 0:
            level = logging.WARNING
        case 1:
            level = logging.INFO
        case _:
            level = logging.DEBUG

    L.setLevel(level)


L = logging.getLogger("bartender")
L.addHandler(RichHandler())

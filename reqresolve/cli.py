from argparse import ArgumentParser, Namespace
from datetime import datetime, UTC
from typing import cast, Callable


def datetime_action(value: str) -> datetime:
    for strategy in (
            lambda ts: datetime.fromtimestamp(int(ts), UTC),
            lambda ts: datetime.fromisoformat(ts),
    ):
        # noinspection PyBroadException
        try:
            return cast(Callable[[str], datetime], strategy)(value)
        except Exception:
            ...
    raise ValueError('Cannot convert into datetime: tried UTC timestamp and ISO format')


def parse() -> Namespace:
    parser = ArgumentParser()
    subparsers = parser.add_subparsers(dest='command')

    query_parser = subparsers.add_parser('query', help='Query packages without reading any file')
    query_parser.add_argument('packages',
                              nargs='+',
                              help='Package names to query')
    query_parser.add_argument('-t',
                              '--time',
                              type=datetime_action,
                              help='Time before which we query package versions (UTC | Unix)',
                              required=True)

    file_parser = subparsers.add_parser('file', help='Query packages from selected file and write results into it')
    file_parser.add_argument('-r',
                             '--root',
                             default='.',
                             help="Root of the repository (default '.')")
    file_parser.add_argument('-f',
                             '--file',
                             default='requirements.txt',
                             help="Relative path (from root) to requirements file (default 'requirements.txt')")
    file_parser.add_argument('-d',
                             '--dry-run',
                             action='store_true',
                             help='Output packages into console (it helps when writing to specific format is not supported)')

    return parser.parse_args()

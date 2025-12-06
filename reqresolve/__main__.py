import asyncio
import os
import sys
from argparse import ArgumentParser
from pathlib import Path

from .git import find_newest_change
from .interactor import for_filepath as interactor_for_filepath
from .pypi import PypiClient


async def main() -> None:
    parser = ArgumentParser()
    parser.add_argument('-r',
                        '--root',
                        default='.',
                        help="Root of the repository (default '.')")
    parser.add_argument('-f',
                        '--file',
                        default='requirements.txt',
                        help="Relative path (from root) to requirements file (default 'requirements.txt')")
    args = parser.parse_args(sys.argv[1:])
    fullpath = str(Path(args.root) / args.file)
    before_time = find_newest_change(args.root, args.file)
    interactor = interactor_for_filepath(fullpath)
    packages = interactor.load_specs()
    mappings = await PypiClient(before_time).query_packages(pkg.name for pkg in packages if pkg.unconstrained)

    if len(mappings) == 0:
        return

    os.rename(fullpath, fullpath + '.bak')
    with open(fullpath, 'w+') as f:
        for pkg in packages:
            if pkg.unconstrained:
                f.write(f'{pkg}<={mappings[pkg.name]}\n')
            else:
                f.write(f'{pkg}\n')


if __name__ == '__main__':
    asyncio.run(main())

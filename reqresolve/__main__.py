import asyncio
import os.path
from typing import cast

import rich
from rich.progress import Progress

from reqresolve import cli
from reqresolve.git import find_newest_change
from reqresolve.interactor import for_filepath as interactor_for_filepath
from reqresolve.pypi import PypiClient


async def _main() -> None:
    args = cli.parse()

    match args.command:
        case 'query':
            with Progress(transient=True) as p:
                task = p.add_task('Working...', total=len(args.packages))
                mappings = await PypiClient(
                    args.time,
                    lambda: p.update(task, advance=1)
                ).query_packages(args.packages)
            rich.get_console().rule('Results')
            for pkg in args.packages:
                print(f'{pkg}<={mappings[pkg]}')

        case 'file':
            fullpath = cast(str, os.path.join(args.root, args.file))
            before_time = find_newest_change(args.root, args.file)
            interactor = interactor_for_filepath(fullpath)
            packages = interactor.load_specs()
            unconstrained_packages = [pkg.name for pkg in packages if pkg.unconstrained]

            if len(unconstrained_packages) == 0:
                rich.print('[yellow]Nothing to do')
                return

            with Progress(transient=True) as p:
                task = p.add_task('Working...', total=len(unconstrained_packages))
                mappings = await PypiClient(
                    before_time,
                    lambda: p.update(task, advance=1)
                ).query_packages(unconstrained_packages)

            packages = [
                i.versioned(f'<={mappings[i.name]}') if i.unconstrained else i
                for i in packages
            ]
            if not args.dry_run:
                interactor.save_specs(packages)
            else:
                rich.get_console().rule('Results')
                rich.print(f'{interactor.dump_specs(packages)}')


def main() -> None:
    asyncio.run(_main())


if __name__ == '__main__':
    main()

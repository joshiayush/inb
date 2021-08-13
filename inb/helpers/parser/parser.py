"""from __future__ imports must occur at the beginning of the file. DO NOT CHANGE!"""
from __future__ import annotations

from typing import Any

import argparse

from .coloredparser import ColoredArgumentParser


class NARGS(object):
    """Class NARGS provides constant strings that specify the number of arguments for
    the add_argument() method."""
    OPTIONAL: str = "?"
    ZERO_OR_MORE: str = "*"
    ONE_OR_MORE: str = "+"


def CreateParser(
        prog: str = None,
        usage: str = None,
        description: str = None,
        epilog: str = '',
        parents: list = [],
        formatter_class: object = argparse.HelpFormatter,
        prefix_chars: str = '-',
        fromfile_prefix_chars: str = '',
        argument_default: Any = ...,
        conflict_handler: str = "error",
        add_help: bool = True,
        allow_abbrev: bool = True) -> argparse.ArgumentParser:
    """Function to create a new ArgumentParser object for our cli.

    :Args:
        - prog: The name of the program (default: sys.argv[0])
        - usage: The string describing the program usage (default: generated from arguments added to parser)
        - description: Text to display before the argument help (default: none)
        - epilog: Text to display after the argument help (default: none)
        - parents: A list of ArgumentParser objects whose arguments should also be included
        - formatter_class: A class for customizing the help output
        - prefix_chars: The set of characters that prefix optional arguments (default: ‘-‘)
        - fromfile_prefix_chars: The set of characters that prefix files from which additional arguments should 
            be read (default: None)
        - argument_default: The global default value for arguments (default: None)
        - conflict_handler: The strategy for resolving conflicting optionals (usually unnecessary)
        - add_help: Add a -h/--help option to the parser (default: True)
        - allow_abbrev: Allows long options to be abbreviated if the abbreviation is unambiguous. (default: True)z

    :Returns:
        - {arparse.ArgumentParser}
    """
    return ColoredArgumentParser(
        prog=prog,
        usage=usage,
        description=description,
        epilog=epilog,
        parents=parents,
        formatter_class=formatter_class,
        prefix_chars=prefix_chars,
        fromfile_prefix_chars=fromfile_prefix_chars,
        argument_default=argument_default,
        conflict_handler=conflict_handler,
        add_help=add_help,
        allow_abbrev=allow_abbrev)

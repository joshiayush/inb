# MIT License
#
# Copyright (c) 2019 Creative Commons
#
# Permission is hereby granted, free of charge, to any person obtaining a
# copy of this software and associated documentation files (the "Software"),
# to deal in the Software without restriction, including without limitation
# the rights to use, copy, modify, merge, publish, distribute, sublicense,
# and/or sell copies of the Software, and to permit persons to whom the
# Software is furnished to do so, subject to the following conditions
#
# The above copyright notice and this permission notice shall be included
# in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS
# OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.

"""from __future__ imports must occur at the beginning of the file. DO NOT CHANGE!"""
from __future__ import annotations

import sys
import argparse

try:
    from gettext import gettext as _
except ImportError:
    def _(message):
        return message


class NARGS(object):
    """Class NARGS provides constant strings that specify the number of arguments for
    the add_argument() method."""
    OPTIONAL: str = "?"
    ZERO_OR_MORE: str = "*"
    ONE_OR_MORE: str = "+"


class OPT_ARGS_ACTION(object):
    """Class OPT_ARGS_ACTION provides the actions accepted by the add_argument() method
    while adding an optional argument."""
    COUNT: str = "count"
    STORE_TRUE: str = "store_true"


class _ArgumentParser(argparse.ArgumentParser):
    """We don't want any compatibility issue so we don't overwrite the constructor!
    The parent constructor method takes the following arguments:

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
        - allow_abbrev: Allows long options to be abbreviated if the abbreviation is unambiguous. (default: True)
    """
    __COLOR_DICT = {"RED": "1;31",
                    "GREEN": "1;32",
                    "YELLOW": "1;33",
                    "BLUE": "1;36"}

    def print_usage(self: _ArgumentParser,
                    file: str = None) -> None:
        file = sys.stdout if file is None else file

        self._print_message(self.format_usage()[0].upper() + self.format_usage()[1:],
                            file,
                            self.__COLOR_DICT["YELLOW"])

    def print_help(self: _ArgumentParser,
                   file: str = None) -> None:
        file = sys.stdout if file is None else file

        self._print_message(self.format_help()[0].upper() + self.format_help()[1:],
                            file,
                            self.__COLOR_DICT["BLUE"])

    def _print_message(self: _ArgumentParser,
                       message: str,
                       file: str = None,
                       color: str = None) -> None:
        if not message:
            return

        file = sys.stderr if file is None else file

        if color is None:
            file.write(message)
            return

        file.write(
            '\x1b[' + color + 'm' + message.strip() + '\x1b[0m\n')

    def exit(self: _ArgumentParser,
             status: int = 0,
             message: str = None) -> None:
        if message:
            self._print_message(message,
                                sys.stderr,
                                self.__COLOR_DICT["RED"])

        sys.exit(status)

    def error(self: _ArgumentParser,
              message: str,
              usage: bool = True) -> None:
        if usage:
            self.print_usage(sys.stderr)

        self.exit(2,
                  _("%(prog)s: Error: %(message)s\n") % {"prog": self.prog, "message": message})

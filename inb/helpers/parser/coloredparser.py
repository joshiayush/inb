from __future__ import annotations

import sys
import argparse

from gettext import gettext


class ColoredArgumentParser(argparse.ArgumentParser):
    """We don't want any compatibility issue so we don't overwrite the constructor!"""
    color_dict = {
        "RED": "1;31", "GREEN": "1;32", "YELLOW": "1;33", "BLUE": "1;36"}

    def print_usage(self: ColoredArgumentParser, file: str = None) -> None:
        file = sys.stdout if file is None else file

        self._print_message(
            self.format_usage()[0].upper() + self.format_usage()[1:], file, self.color_dict["YELLOW"])

    def print_help(self: ColoredArgumentParser, file: str = None) -> None:
        file = sys.stdout if file is None else file

        self._print_message(
            self.format_help()[0].upper() + self.format_help()[1:], file, self.color_dict["BLUE"])

    def _print_message(self: ColoredArgumentParser, message: str, file: str = None, color: str = None) -> None:
        if not message:
            return

        file = sys.stderr if file is None else file

        if color is None:
            file.write(message)
            return

        file.write(
            '\x1b[' + color + 'm' + message.strip() + '\x1b[0m\n')

    def exit(self: ColoredArgumentParser, status: int = 0, message: str = None) -> None:
        if message:
            self._print_message(message, sys.stderr, self.color_dict["RED"])

        sys.exit(status)

    def error(self: ColoredArgumentParser, message: str) -> None:
        self.print_usage(sys.stderr)

        self.exit(2, gettext(
            "%(prog)s: Error: %(message)s\n") % {"prog": self.prog, "message": message})

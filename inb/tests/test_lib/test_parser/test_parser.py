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

# from __future__ imports must occur at the beginning of the file. DO NOT CHANGE!
from __future__ import annotations

import sys
import unittest

from unittest.mock import Mock
from unittest.mock import patch

from lib import ArgumentParser

try:
    from gettext import gettext as _
except ImportError:
    def _(message: str):
        return message


class TestOverridedVersionOfArgumentParserClass(unittest.TestCase):
    def setUp(self: TestOverridedVersionOfArgumentParserClass) -> None:
        self.argparse = ArgumentParser(
            prog="tests", description="text to display before argument help goes here")
        self.color_dict = {"RED": "\x1b[1;31m",
                           "GREEN": "\x1b[1;32m",
                           "YELLOW": "\x1b[1;33m",
                           "BLUE": "\x1b[1;36m",
                           "RESET": "\x1b[0m"}

    def test_color_dict_values(self: TestOverridedVersionOfArgumentParserClass) -> None:
        self.assertEqual(
            self.argparse._ArgumentParser__COLOR_DICT, self.color_dict)

    @patch("lib.ArgumentParser._print_message")
    @patch("argparse.ArgumentParser.format_usage")
    def test_overrided_print_usage_method_internal_calls(self: TestOverridedVersionOfArgumentParserClass,
                                                         mock_format_usage: Mock,
                                                         mock_print_message: Mock) -> None:
        self.argparse.print_usage()
        mock_format_usage.assert_called()
        message = self.argparse.format_usage()
        mock_print_message.assert_called_with(
            message[0].upper() + message[1:], sys.stdout, self.color_dict["YELLOW"])

    @patch("lib.ArgumentParser._print_message")
    @patch("argparse.ArgumentParser.format_help")
    def test_overrided_print_help_method_internal_calls(self: TestOverridedVersionOfArgumentParserClass,
                                                        mock_format_help: Mock,
                                                        mock_print_message: Mock) -> None:
        self.argparse.print_help()
        mock_format_help.assert_called()
        message = self.argparse.format_help()
        mock_print_message.assert_called_with(
            message[0].upper() + message[1:], sys.stdout, self.color_dict["BLUE"])

    @patch("sys.stdin.write")
    @patch("sys.stderr.write")
    @patch("sys.stdout.write")
    def test_overrided_print_message_method_internal_calls(self: TestOverridedVersionOfArgumentParserClass,
                                                           mock_stdout_write: Mock,
                                                           mock_stderr_write: Mock,
                                                           mock_stdin_write: Mock) -> None:
        message = "testing private method print_message"

        self.argparse._print_message(message=message)
        mock_stdout_write.assert_called_with(message + '\n')

        self.argparse._print_message(message=message, file=sys.stdout)
        mock_stdout_write.assert_called_with(message + '\n')

        self.argparse._print_message(message=message, file=sys.stderr)
        mock_stderr_write.asser_called_with(message + '\n')

        self.argparse._print_message(message=message, file=sys.stdin)
        mock_stdin_write.assert_called_with(message + '\n')

    @patch("lib.ArgumentParser._print_message")
    @patch("sys.exit")
    def test_overrided_exit_method_internal_calls(self: TestOverridedVersionOfArgumentParserClass,
                                                  mock_exit: Mock,
                                                  mock_print_message: Mock) -> None:
        self.argparse.exit()
        mock_print_message.assert_not_called()
        mock_exit.assert_called_with(0)

        self.argparse.exit(1)
        mock_print_message.assert_not_called()
        mock_exit.assert_called_with(1)

        self.argparse.exit(0, "exiting...")
        mock_print_message.assert_called_with(
            "exiting...", sys.stderr, self.color_dict["RED"])
        mock_exit.assert_called_with(0)

    @patch("lib.ArgumentParser.exit")
    @patch("lib.ArgumentParser.print_usage")
    def test_overrided_error_method_internal_calls(self: TestOverridedVersionOfArgumentParserClass,
                                                   mock_print_usage: Mock,
                                                   mock_exit: Mock) -> None:
        err_msg = "error..."

        self.argparse.error(err_msg)
        mock_print_usage.assert_called_with(sys.stderr)
        mock_exit.assert_called_with(2, _("%(prog)s: Error: %(message)s\n") %
                                     {"prog": self.argparse.prog, "message": err_msg})

        self.argparse.error(err_msg, usage=False)
        mock_print_usage.assert_not_called()
        mock_exit.assert_called_with(2, _("%(prog)s: Error: %(message)s\n") %
                                     {"prog": self.argparse.prog, "message": err_msg})

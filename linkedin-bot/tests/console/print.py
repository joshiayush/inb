from __future__ import annotations

import colorama
import unittest

from unittest import mock
from unittest.mock import Mock
from unittest.mock import patch

from console.print import printk
from console.print import printRed
from console.print import printBlue
from console.print import printWhite
from console.print import printGreen
from console.print import printYellow


class TestPrintFunctions(unittest.TestCase):

    @patch("builtins.print")
    def test_printk(self: TestPrintFunctions, mock: Mock):
        printk("Testing printk() function ...")
        mock.assert_called_with("Testing printk() function ...")

        printk(
            "Testing printk() function with [start] parameter ...", start=' ')
        mock.assert_called_with(
            "Testing printk() function with [start] parameter ...", start=' ')

        printk("Testing printk() function with [pad] parameter ...", pad='1')
        mock.assert_called_with(
            "Testing printk() function with [pad] parameter ...")

    @patch("builtins.print")
    @patch("console.print.printk")
    def test_printRed(self: TestPrintFunctions, mock_printk: Mock, mock_print: Mock):
        printRed("Testing printRed() function ...")
        mock_printk.assert_called_with(
            f"""{colorama.Fore.RED}Testing printRed() function ...{colorama.Fore.RESET}""")

        printRed(
            "Testing printRed() function with [style] parameter ...", style='b')
        mock_printk.assert_called_with(
            f"""{colorama.Fore.RED}Testing printRed() function with [style] parameter ...{colorama.Fore.RESET}""")
        mock_print.assert_has_calls([mock.call(
            f"""{colorama.Style.BRIGHT}""", end=''),
            mock.call(f"""{colorama.Style.RESET_ALL}""", end='')])

    @patch("builtins.print")
    @patch("console.print.printk")
    def test_printGreen(self: TestPrintFunctions, mock_printk: Mock, mock_print: Mock):
        printGreen("Testing printGreen() function ...")
        mock_printk.assert_called_with(
            f"""{colorama.Fore.GREEN}Testing printGreen() function ...{colorama.Fore.RESET}""")

        printGreen(
            "Testing printGreen() function with [style] parameter ...", style='b')
        mock_printk.assert_called_with(
            f"""{colorama.Fore.GREEN}Testing printGreen() function with [style] parameter ...{colorama.Fore.RESET}""")
        mock_print.assert_has_calls([mock.call(
            f"""{colorama.Style.BRIGHT}""", end=''),
            mock.call(f"""{colorama.Style.RESET_ALL}""", end='')])

    @patch("builtins.print")
    @patch("console.print.printk")
    def test_printBlue(self, mock_printk: Mock, mock_print: Mock):
        printBlue("Testing printBlue() function ...")
        mock_printk.assert_called_with(
            f"""{colorama.Fore.BLUE}Testing printBlue() function ...{colorama.Fore.RESET}""")

        printBlue(
            "Testing printBlue() function with [style] parameter ...", style='b')
        mock_printk.assert_called_with(
            f"""{colorama.Fore.BLUE}Testing printBlue() function with [style] parameter ...{colorama.Fore.RESET}""")
        mock_print.assert_has_calls([mock.call(
            f"""{colorama.Style.BRIGHT}""", end=''),
            mock.call(f"""{colorama.Style.RESET_ALL}""", end='')])

    @patch("builtins.print")
    @patch("console.print.printk")
    def test_printYellow(self, mock_printk: Mock, mock_print: Mock):
        printYellow("Testing printYellow() function ...")
        mock_printk.assert_called_with(
            f"""{colorama.Fore.YELLOW}Testing printYellow() function ...{colorama.Fore.RESET}""")

        printYellow(
            "Testing printYellow() function with [style] parameter ...", style='b')
        mock_printk.assert_called_with(
            f"""{colorama.Fore.YELLOW}Testing printYellow() function with [style] parameter ...{colorama.Fore.RESET}""")
        mock_print.assert_has_calls([mock.call(
            f"""{colorama.Style.BRIGHT}""", end=''),
            mock.call(f"""{colorama.Style.RESET_ALL}""", end='')])

    @patch("builtins.print")
    @patch("console.print.printk")
    def test_printWhite(self, mock_printk, mock_print):
        printWhite("Testing printWhite() function ...")
        mock_printk.assert_called_with(
            f"""{colorama.Fore.WHITE}Testing printWhite() function ...{colorama.Fore.RESET}""")

        printWhite(
            "Testing printWhite() function with [style] parameter ...", style='b')
        mock_printk.assert_called_with(
            f"""{colorama.Fore.WHITE}Testing printWhite() function with [style] parameter ...{colorama.Fore.RESET}""")
        mock_print.assert_has_calls([mock.call(
            f"""{colorama.Style.BRIGHT}""", end=''),
            mock.call(f"""{colorama.Style.RESET_ALL}""", end='')])

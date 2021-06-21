from __future__ import annotations

import sys
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
    def test_printk(self: TestPrintFunctions, mock_print: Mock) -> None:
        printk("Testing printk() function ...")
        mock_print.assert_called_with("Testing printk() function ...")

        printk("Testing printk() function with a new string ...")
        mock_print.assert_called_with(
            "Testing printk() function with a new string ...")

    @patch("builtins.print")
    def test_printk_parameter(self: TestPrintFunctions, mock_print: Mock) -> None:
        printk(
            "Testing printk() function with [start] parameter ...", start=' ')
        mock_print.assert_has_calls([
            mock.call(end=' '), mock.call("Testing printk() function with [start] parameter ...")])

        printk("Testing printk() function with [pad] parameter ...", pad='1')
        mock_print.assert_has_calls([
            mock.call(' ', end=''), mock.call("Testing printk() function with [pad] parameter ...")])

        printk(
            "Testing printk() function with [pad] and [start] parameter ...", pad='1', start=' ')
        mock_print.assert_has_calls([
            mock.call(end=' '), mock.call(' ', end=''),
            mock.call("Testing printk() function with [pad] and [start] parameter ...")])

    @patch("builtins.print")
    @patch("console.print.printk")
    def test_printRed(self: TestPrintFunctions, mock_printk: Mock, mock_print: Mock) -> None:
        printRed("Testing printRed() function ...")
        self.assertFalse(mock_print.called)
        mock_printk.assert_called_with(
            f"""{colorama.Fore.RED}Testing printRed() function ...{colorama.Fore.RESET}""")

        printRed("Testing printRed() function with a new string ...")
        self.assertFalse(mock_print.called)
        mock_printk.assert_called_with(
            f"""{colorama.Fore.RED}Testing printRed() function with a new string ...{colorama.Fore.RESET}""")

    @patch("builtins.print")
    @patch("console.print.printk")
    def test_printRed_parameter(self: TestPrintFunctions, mock_printk: Mock, mock_print: Mock) -> None:
        printRed(
            "Testing printRed() function with [style] parameter ...", style='b')
        mock_printk.assert_called_with(
            f"""{colorama.Fore.RED}Testing printRed() function with [style] parameter ...{colorama.Fore.RESET}""")
        mock_print.assert_has_calls([
            mock.call(f"""{colorama.Style.BRIGHT}""", end=''), mock.call(f"""{colorama.Style.RESET_ALL}""", end='')])

        printRed(
            "Testing printRed() function with [style] and [pad] parameter ...", style='b', pad='1')
        mock_printk.assert_called_with(
            f"""{colorama.Fore.RED}Testing printRed() function with [style] and [pad] parameter ...{colorama.Fore.RESET}""", pad='1')
        mock_print.assert_has_calls([
            mock.call(f"""{colorama.Style.BRIGHT}""", end=''), mock.call(f"""{colorama.Style.RESET_ALL}""", end='')])

        printRed(
            "Testing printRed() function with [style], [pad] and [start] parameter ...", style='b', pad='1', start='\n')
        mock_printk.assert_called_with(
            f"""{colorama.Fore.RED}Testing printRed() function with [style], [pad] and [start] parameter ...{colorama.Fore.RESET}""", start='\n', pad='1')
        mock_print.assert_has_calls([
            mock.call(f"""{colorama.Style.BRIGHT}""", end=''), mock.call(f"""{colorama.Style.RESET_ALL}""", end='')])

    @patch("builtins.print")
    @patch("console.print.printk")
    def test_printGreen(self: TestPrintFunctions, mock_printk: Mock, mock_print: Mock):
        printGreen("Testing printGreen() function ...")
        self.assertFalse(mock_print.called)
        mock_printk.assert_called_with(
            f"""{colorama.Fore.GREEN}Testing printGreen() function ...{colorama.Fore.RESET}""")

        printGreen("Testing printGreen() function with a new string ...")
        self.assertFalse(mock_print.called)
        mock_printk.assert_called_with(
            f"""{colorama.Fore.GREEN}Testing printGreen() function with a new string ...{colorama.Fore.RESET}""")

    @patch("builtins.print")
    @patch("console.print.printk")
    def test_printGreen_parameter(self: TestPrintFunctions, mock_printk: Mock, mock_print: Mock) -> None:
        printGreen(
            "Testing printGreen() function with [style] parameter ...", style='b')
        mock_printk.assert_called_with(
            f"""{colorama.Fore.GREEN}Testing printGreen() function with [style] parameter ...{colorama.Fore.RESET}""")
        mock_print.assert_has_calls([
            mock.call(f"""{colorama.Style.BRIGHT}""", end=''), mock.call(f"""{colorama.Style.RESET_ALL}""", end='')])

        printGreen(
            "Testing printGreen() function with [style] and [pad] parameter ...", style='b', pad='1')
        mock_printk.assert_called_with(
            f"""{colorama.Fore.GREEN}Testing printGreen() function with [style] and [pad] parameter ...{colorama.Fore.RESET}""", pad='1')
        mock_print.assert_has_calls([
            mock.call(f"""{colorama.Style.BRIGHT}""", end=''), mock.call(f"""{colorama.Style.RESET_ALL}""", end='')])

        printGreen(
            "Testing printGreen() function with [style], [pad] and [start] parameter ...", style='b', pad='1', start='\n')
        mock_printk.assert_called_with(
            f"""{colorama.Fore.GREEN}Testing printGreen() function with [style], [pad] and [start] parameter ...{colorama.Fore.RESET}""", start='\n', pad='1')
        mock_print.assert_has_calls([
            mock.call(f"""{colorama.Style.BRIGHT}""", end=''), mock.call(f"""{colorama.Style.RESET_ALL}""", end='')])

    @patch("builtins.print")
    @patch("console.print.printk")
    def test_printBlue(self, mock_printk: Mock, mock_print: Mock):
        printBlue("Testing printBlue() function ...")
        self.assertFalse(mock_print.called)
        mock_printk.assert_called_with(
            f"""{colorama.Fore.BLUE}Testing printBlue() function ...{colorama.Fore.RESET}""")

        printBlue("Testing printBlue() function with a new string ...")
        self.assertFalse(mock_print.called)
        mock_printk.assert_called_with(
            f"""{colorama.Fore.BLUE}Testing printBlue() function with a new string ...{colorama.Fore.RESET}""")

    @patch("builtins.print")
    @patch("console.print.printk")
    def test_printBlue_parameter(self: TestPrintFunctions, mock_printk: Mock, mock_print: Mock) -> None:
        printBlue(
            "Testing printBlue() function with [style] parameter ...", style='b')
        mock_printk.assert_called_with(
            f"""{colorama.Fore.BLUE}Testing printBlue() function with [style] parameter ...{colorama.Fore.RESET}""")
        mock_print.assert_has_calls([
            mock.call(f"""{colorama.Style.BRIGHT}""", end=''), mock.call(f"""{colorama.Style.RESET_ALL}""", end='')])

        printBlue(
            "Testing printBlue() function with [style] and [pad] parameter ...", style='b', pad='1')
        mock_printk.assert_called_with(
            f"""{colorama.Fore.BLUE}Testing printBlue() function with [style] and [pad] parameter ...{colorama.Fore.RESET}""", pad='1')
        mock_print.assert_has_calls([
            mock.call(f"""{colorama.Style.BRIGHT}""", end=''), mock.call(f"""{colorama.Style.RESET_ALL}""", end='')])

        printBlue(
            "Testing printBlue() function with [style], [pad] and [start] parameter ...", style='b', pad='1', start='\n')
        mock_printk.assert_called_with(
            f"""{colorama.Fore.BLUE}Testing printBlue() function with [style], [pad] and [start] parameter ...{colorama.Fore.RESET}""", start='\n', pad='1')
        mock_print.assert_has_calls([
            mock.call(f"""{colorama.Style.BRIGHT}""", end=''), mock.call(f"""{colorama.Style.RESET_ALL}""", end='')])

    @patch("builtins.print")
    @patch("console.print.printk")
    def test_printYellow(self, mock_printk: Mock, mock_print: Mock):
        printYellow("Testing printYellow() function ...")
        self.assertFalse(mock_print.called)
        mock_printk.assert_called_with(
            f"""{colorama.Fore.YELLOW}Testing printYellow() function ...{colorama.Fore.RESET}""")

        printYellow("Testing printYellow() function with a new string ...")
        self.assertFalse(mock_print.called)
        mock_printk.assert_called_with(
            f"""{colorama.Fore.YELLOW}Testing printYellow() function with a new string ...{colorama.Fore.RESET}""")

    @patch("builtins.print")
    @patch("console.print.printk")
    def test_printYellow_parameter(self: TestPrintFunctions, mock_printk: Mock, mock_print: Mock) -> None:
        printYellow(
            "Testing printYellow() function with [style] parameter ...", style='b')
        mock_printk.assert_called_with(
            f"""{colorama.Fore.YELLOW}Testing printYellow() function with [style] parameter ...{colorama.Fore.RESET}""")
        mock_print.assert_has_calls([
            mock.call(f"""{colorama.Style.BRIGHT}""", end=''), mock.call(f"""{colorama.Style.RESET_ALL}""", end='')])

        printYellow(
            "Testing printYellow() function with [style] and [pad] parameter ...", style='b', pad='1')
        mock_printk.assert_called_with(
            f"""{colorama.Fore.YELLOW}Testing printYellow() function with [style] and [pad] parameter ...{colorama.Fore.RESET}""", pad='1')
        mock_print.assert_has_calls([
            mock.call(f"""{colorama.Style.BRIGHT}""", end=''), mock.call(f"""{colorama.Style.RESET_ALL}""", end='')])

        printYellow(
            "Testing printYellow() function with [style], [pad] and [start] parameter ...", style='b', pad='1', start='\n')
        mock_printk.assert_called_with(
            f"""{colorama.Fore.YELLOW}Testing printYellow() function with [style], [pad] and [start] parameter ...{colorama.Fore.RESET}""", start='\n', pad='1')
        mock_print.assert_has_calls([
            mock.call(f"""{colorama.Style.BRIGHT}""", end=''), mock.call(f"""{colorama.Style.RESET_ALL}""", end='')])

    @patch("builtins.print")
    @patch("console.print.printk")
    def test_printWhite(self, mock_printk, mock_print):
        printWhite("Testing printWhite() function ...")
        self.assertFalse(mock_print.called)
        mock_printk.assert_called_with(
            f"""{colorama.Fore.WHITE}Testing printWhite() function ...{colorama.Fore.RESET}""")

        printWhite("Testing printWhite() function with a new string ...")
        self.assertFalse(mock_print.called)
        mock_printk.assert_called_with(
            f"""{colorama.Fore.WHITE}Testing printWhite() function with a new string ...{colorama.Fore.RESET}""")

    @patch("builtins.print")
    @patch("console.print.printk")
    def test_printWhite_parameter(self: TestPrintFunctions, mock_printk: Mock, mock_print: Mock) -> None:
        printWhite(
            "Testing printWhite() function with [style] parameter ...", style='b')
        mock_printk.assert_called_with(
            f"""{colorama.Fore.WHITE}Testing printWhite() function with [style] parameter ...{colorama.Fore.RESET}""")
        mock_print.assert_has_calls([
            mock.call(f"""{colorama.Style.BRIGHT}""", end=''), mock.call(f"""{colorama.Style.RESET_ALL}""", end='')])

        printWhite(
            "Testing printWhite() function with [style] and [pad] parameter ...", style='b', pad='1')
        mock_printk.assert_called_with(
            f"""{colorama.Fore.WHITE}Testing printWhite() function with [style] and [pad] parameter ...{colorama.Fore.RESET}""", pad='1')
        mock_print.assert_has_calls([
            mock.call(f"""{colorama.Style.BRIGHT}""", end=''), mock.call(f"""{colorama.Style.RESET_ALL}""", end='')])

        printWhite(
            "Testing printWhite() function with [style], [pad] and [start] parameter ...", style='b', pad='1', start='\n')
        mock_printk.assert_called_with(
            f"""{colorama.Fore.WHITE}Testing printWhite() function with [style], [pad] and [start] parameter ...{colorama.Fore.RESET}""", start='\n', pad='1')
        mock_print.assert_has_calls([
            mock.call(f"""{colorama.Style.BRIGHT}""", end=''), mock.call(f"""{colorama.Style.RESET_ALL}""", end='')])

from __future__ import annotations

import colorama
import unittest

from unittest import mock
from unittest.mock import Mock
from unittest.mock import patch

from console.scan import scank
from console.scan import scanRed
from console.scan import scanBlue
from console.scan import scanGreen
from console.scan import scanWhite
from console.scan import scanYellow


class TestScanFunctions(unittest.TestCase):

    @patch("builtins.input", side_effect=["linkedin", "config", "help", "clear", "theme", "exit", "developer"])
    def test_scank(self: TestScanFunctions, mock_input: Mock) -> None:
        self.assertTrue(scank("LinkedIn/>") == "linkedin")
        mock_input.assert_called_with("LinkedIn/>")

        self.assertTrue(scank("LinkedIn/>") == "config")
        mock_input.assert_called_with("LinkedIn/>")

        self.assertTrue(scank("LinkedIn/>") == "help")
        mock_input.assert_called_with("LinkedIn/>")

        self.assertTrue(scank("LinkedIn/>") == "clear")
        mock_input.assert_called_with("LinkedIn/>")

        self.assertTrue(scank("LinkedIn/>") == "theme")
        mock_input.assert_called_with("LinkedIn/>")

        self.assertTrue(scank("LinkedIn/>") == "exit")
        mock_input.assert_called_with("LinkedIn/>")

        self.assertTrue(scank("LinkedIn/>") == "developer")
        mock_input.assert_called_with("LinkedIn/>")

    @patch("builtins.print")
    @patch("builtins.input", return_value="linkedin")
    def test_scank_parameter(self: TestScanFunctions, mock_input: Mock, mock_print: Mock) -> None:
        scank("LinkedIn/>", start=' ')
        mock_print.assert_called_with(end=' ')

        scank("LinkedIn/>", pad='1')
        mock_input.assert_called_with(" LinkedIn/>")

        scank("LinkedIn/>", end=' ')
        mock_input.assert_called_with("LinkedIn/> ")

        scank("LinkedIn/>", start='\n', pad='1', end='\n')
        mock_print.assert_called_with(end='\n')
        mock_input.assert_called_with(" LinkedIn/>\n")

    @patch("builtins.print")
    @patch("console.scan.scank", side_effect=["linkedin", "config", "help", "clear", "theme", "exit", "developer"])
    def test_scanWhite(self: TestScanFunctions, mock_scank: Mock, mock_print: Mock) -> None:
        self.assertTrue(scanWhite("LinkedIn/>") == "linkedin")
        mock_scank.assert_called_with("LinkedIn/>")
        mock_print.assert_has_calls([
            mock.call(f"""{colorama.Fore.WHITE}""", end=''), mock.call(f"""{colorama.Fore.RESET}""", end='')])

        self.assertTrue(scanWhite("LinkedIn/>") == "config")
        mock_scank.assert_called_with("LinkedIn/>")
        mock_print.assert_has_calls([
            mock.call(f"""{colorama.Fore.WHITE}""", end=''), mock.call(f"""{colorama.Fore.RESET}""", end='')])

        self.assertTrue(scanWhite("LinkedIn/>") == "help")
        mock_scank.assert_called_with("LinkedIn/>")
        mock_print.assert_has_calls([
            mock.call(f"""{colorama.Fore.WHITE}""", end=''), mock.call(f"""{colorama.Fore.RESET}""", end='')])

        self.assertTrue(scanWhite("LinkedIn/>") == "clear")
        mock_scank.assert_called_with("LinkedIn/>")
        mock_print.assert_has_calls([
            mock.call(f"""{colorama.Fore.WHITE}""", end=''), mock.call(f"""{colorama.Fore.RESET}""", end='')])

        self.assertTrue(scanWhite("LinkedIn/>") == "theme")
        mock_scank.assert_called_with("LinkedIn/>")
        mock_print.assert_has_calls([
            mock.call(f"""{colorama.Fore.WHITE}""", end=''), mock.call(f"""{colorama.Fore.RESET}""", end='')])

        self.assertTrue(scanWhite("LinkedIn/>") == "exit")
        mock_scank.assert_called_with("LinkedIn/>")
        mock_print.assert_has_calls([
            mock.call(f"""{colorama.Fore.WHITE}""", end=''), mock.call(f"""{colorama.Fore.RESET}""", end='')])

        self.assertTrue(scanWhite("LinkedIn/>") == "developer")
        mock_scank.assert_called_with("LinkedIn/>")
        mock_print.assert_has_calls([
            mock.call(f"""{colorama.Fore.WHITE}""", end=''), mock.call(f"""{colorama.Fore.RESET}""", end='')])

    @patch("builtins.print")
    @patch("console.scan.scank", return_value="linkedin")
    def test_scanWhite_parameter(self: TestScanFunctions, mock_scank: Mock, mock_print: Mock) -> None:
        scanWhite("LinkedIn/>", style='')
        self.assertFalse(mock_scank.called)
        self.assertFalse(mock_print.called)

        scanWhite("LinkedIn/>", style='b')
        mock_scank.assert_called_with("LinkedIn/>")
        mock_print.assert_has_calls([
            mock.call(f"""{colorama.Style.BRIGHT}""", end=''),
            mock.call(f"""{colorama.Fore.WHITE}""", end=''),
            mock.call(f"""{colorama.Fore.RESET}""", end=''),
            mock.call(f"""{colorama.Style.RESET_ALL}""", end='')
        ])

        scanWhite("LinkedIn/>", style='b', start='\n')
        mock_scank.assert_called_with("LinkedIn/>", start='\n')
        mock_print.assert_has_calls([
            mock.call(f"""{colorama.Style.BRIGHT}""", end=''),
            mock.call(f"""{colorama.Fore.WHITE}""", end=''),
            mock.call(f"""{colorama.Fore.RESET}""", end=''),
            mock.call(f"""{colorama.Style.RESET_ALL}""", end='')
        ])

        scanWhite("LinkedIn/>", style='b', start='\n', pad='1')
        mock_scank.assert_called_with("LinkedIn/>", start='\n', pad='1')
        mock_print.assert_has_calls([
            mock.call(f"""{colorama.Style.BRIGHT}""", end=''),
            mock.call(f"""{colorama.Fore.WHITE}""", end=''),
            mock.call(f"""{colorama.Fore.RESET}""", end=''),
            mock.call(f"""{colorama.Style.RESET_ALL}""", end='')
        ])

        scanWhite(
            "LinkedIn/>", style='b', start='\n', pad='1', end='\n')
        mock_scank.assert_called_with(
            "LinkedIn/>", start='\n', pad='1', end='\n')
        mock_print.assert_has_calls([
            mock.call(f"""{colorama.Style.BRIGHT}""", end=''),
            mock.call(f"""{colorama.Fore.WHITE}""", end=''),
            mock.call(f"""{colorama.Fore.RESET}""", end=''),
            mock.call(f"""{colorama.Style.RESET_ALL}""", end='')
        ])

    @patch("builtins.print")
    @patch("console.scan.scank", side_effect=["linkedin", "config", "help", "clear", "theme", "exit", "developer"])
    def test_scanRed(self: TestScanFunctions, mock_scank: Mock, mock_print: Mock) -> None:
        self.assertTrue(scanRed("LinkedIn/>") == "linkedin")
        mock_scank.assert_called_with("LinkedIn/>")
        mock_print.assert_has_calls([
            mock.call(f"""{colorama.Fore.RED}""", end=''), mock.call(f"""{colorama.Fore.RESET}""", end='')])

        self.assertTrue(scanRed("LinkedIn/>") == "config")
        mock_scank.assert_called_with("LinkedIn/>")
        mock_print.assert_has_calls([
            mock.call(f"""{colorama.Fore.RED}""", end=''), mock.call(f"""{colorama.Fore.RESET}""", end='')])

        self.assertTrue(scanRed("LinkedIn/>") == "help")
        mock_scank.assert_called_with("LinkedIn/>")
        mock_print.assert_has_calls([
            mock.call(f"""{colorama.Fore.RED}""", end=''), mock.call(f"""{colorama.Fore.RESET}""", end='')])

        self.assertTrue(scanRed("LinkedIn/>") == "clear")
        mock_scank.assert_called_with("LinkedIn/>")
        mock_print.assert_has_calls([
            mock.call(f"""{colorama.Fore.RED}""", end=''), mock.call(f"""{colorama.Fore.RESET}""", end='')])

        self.assertTrue(scanRed("LinkedIn/>") == "theme")
        mock_scank.assert_called_with("LinkedIn/>")
        mock_print.assert_has_calls([
            mock.call(f"""{colorama.Fore.RED}""", end=''), mock.call(f"""{colorama.Fore.RESET}""", end='')])

        self.assertTrue(scanRed("LinkedIn/>") == "exit")
        mock_scank.assert_called_with("LinkedIn/>")
        mock_print.assert_has_calls([
            mock.call(f"""{colorama.Fore.RED}""", end=''), mock.call(f"""{colorama.Fore.RESET}""", end='')])

        self.assertTrue(scanRed("LinkedIn/>") == "developer")
        mock_scank.assert_called_with("LinkedIn/>")
        mock_print.assert_has_calls([
            mock.call(f"""{colorama.Fore.RED}""", end=''), mock.call(f"""{colorama.Fore.RESET}""", end='')])

    @patch("builtins.print")
    @patch("console.scan.scank", return_value="linkedin")
    def test_scanRed_parameter(self: TestScanFunctions, mock_scank: Mock, mock_print: Mock) -> None:
        scanRed("LinkedIn/>", style='')
        self.assertFalse(mock_scank.called)
        self.assertFalse(mock_print.called)

        scanRed("LinkedIn/>", style='b')
        mock_scank.assert_called_with("LinkedIn/>")
        mock_print.assert_has_calls([
            mock.call(f"""{colorama.Style.BRIGHT}""", end=''),
            mock.call(f"""{colorama.Fore.RED}""", end=''),
            mock.call(f"""{colorama.Fore.RESET}""", end=''),
            mock.call(f"""{colorama.Style.RESET_ALL}""", end='')
        ])

        scanRed("LinkedIn/>", style='b', start='\n')
        mock_scank.assert_called_with("LinkedIn/>", start='\n')
        mock_print.assert_has_calls([
            mock.call(f"""{colorama.Style.BRIGHT}""", end=''),
            mock.call(f"""{colorama.Fore.RED}""", end=''),
            mock.call(f"""{colorama.Fore.RESET}""", end=''),
            mock.call(f"""{colorama.Style.RESET_ALL}""", end='')
        ])

        scanRed("LinkedIn/>", style='b', start='\n', pad='1')
        mock_scank.assert_called_with("LinkedIn/>", start='\n', pad='1')
        mock_print.assert_has_calls([
            mock.call(f"""{colorama.Style.BRIGHT}""", end=''),
            mock.call(f"""{colorama.Fore.RED}""", end=''),
            mock.call(f"""{colorama.Fore.RESET}""", end=''),
            mock.call(f"""{colorama.Style.RESET_ALL}""", end='')
        ])

        scanRed(
            "LinkedIn/>", style='b', start='\n', pad='1', end='\n')
        mock_scank.assert_called_with(
            "LinkedIn/>", start='\n', pad='1', end='\n')
        mock_print.assert_has_calls([
            mock.call(f"""{colorama.Style.BRIGHT}""", end=''),
            mock.call(f"""{colorama.Fore.RED}""", end=''),
            mock.call(f"""{colorama.Fore.RESET}""", end=''),
            mock.call(f"""{colorama.Style.RESET_ALL}""", end='')
        ])

    @patch("builtins.print")
    @patch("console.scan.scank", side_effect=["linkedin", "config", "help", "clear", "theme", "exit", "developer"])
    def test_scanGreen(self: TestScanFunctions, mock_scank: Mock, mock_print: Mock) -> None:
        self.assertTrue(scanGreen("LinkedIn/>") == "linkedin")
        mock_scank.assert_called_with("LinkedIn/>")
        mock_print.assert_has_calls([
            mock.call(f"""{colorama.Fore.GREEN}""", end=''), mock.call(f"""{colorama.Fore.RESET}""", end='')])

        self.assertTrue(scanGreen("LinkedIn/>") == "config")
        mock_scank.assert_called_with("LinkedIn/>")
        mock_print.assert_has_calls([
            mock.call(f"""{colorama.Fore.GREEN}""", end=''), mock.call(f"""{colorama.Fore.RESET}""", end='')])

        self.assertTrue(scanGreen("LinkedIn/>") == "help")
        mock_scank.assert_called_with("LinkedIn/>")
        mock_print.assert_has_calls([
            mock.call(f"""{colorama.Fore.GREEN}""", end=''), mock.call(f"""{colorama.Fore.RESET}""", end='')])

        self.assertTrue(scanGreen("LinkedIn/>") == "clear")
        mock_scank.assert_called_with("LinkedIn/>")
        mock_print.assert_has_calls([
            mock.call(f"""{colorama.Fore.GREEN}""", end=''), mock.call(f"""{colorama.Fore.RESET}""", end='')])

        self.assertTrue(scanGreen("LinkedIn/>") == "theme")
        mock_scank.assert_called_with("LinkedIn/>")
        mock_print.assert_has_calls([
            mock.call(f"""{colorama.Fore.GREEN}""", end=''), mock.call(f"""{colorama.Fore.RESET}""", end='')])

        self.assertTrue(scanGreen("LinkedIn/>") == "exit")
        mock_scank.assert_called_with("LinkedIn/>")
        mock_print.assert_has_calls([
            mock.call(f"""{colorama.Fore.GREEN}""", end=''), mock.call(f"""{colorama.Fore.RESET}""", end='')])

        self.assertTrue(scanGreen("LinkedIn/>") == "developer")
        mock_scank.assert_called_with("LinkedIn/>")
        mock_print.assert_has_calls([
            mock.call(f"""{colorama.Fore.GREEN}""", end=''), mock.call(f"""{colorama.Fore.RESET}""", end='')])

    @patch("builtins.print")
    @patch("console.scan.scank", return_value="linkedin")
    def test_scanGreen_parameter(self: TestScanFunctions, mock_scank: Mock, mock_print: Mock) -> None:
        scanGreen("LinkedIn/>", style='')
        self.assertFalse(mock_scank.called)
        self.assertFalse(mock_print.called)

        scanGreen("LinkedIn/>", style='b')
        mock_scank.assert_called_with("LinkedIn/>")
        mock_print.assert_has_calls([
            mock.call(f"""{colorama.Style.BRIGHT}""", end=''),
            mock.call(f"""{colorama.Fore.GREEN}""", end=''),
            mock.call(f"""{colorama.Fore.RESET}""", end=''),
            mock.call(f"""{colorama.Style.RESET_ALL}""", end='')
        ])

        scanGreen("LinkedIn/>", style='b', start='\n')
        mock_scank.assert_called_with("LinkedIn/>", start='\n')
        mock_print.assert_has_calls([
            mock.call(f"""{colorama.Style.BRIGHT}""", end=''),
            mock.call(f"""{colorama.Fore.GREEN}""", end=''),
            mock.call(f"""{colorama.Fore.RESET}""", end=''),
            mock.call(f"""{colorama.Style.RESET_ALL}""", end='')
        ])

        scanGreen("LinkedIn/>", style='b', start='\n', pad='1')
        mock_scank.assert_called_with("LinkedIn/>", start='\n', pad='1')
        mock_print.assert_has_calls([
            mock.call(f"""{colorama.Style.BRIGHT}""", end=''),
            mock.call(f"""{colorama.Fore.GREEN}""", end=''),
            mock.call(f"""{colorama.Fore.RESET}""", end=''),
            mock.call(f"""{colorama.Style.RESET_ALL}""", end='')
        ])

        scanGreen(
            "LinkedIn/>", style='b', start='\n', pad='1', end='\n')
        mock_scank.assert_called_with(
            "LinkedIn/>", start='\n', pad='1', end='\n')
        mock_print.assert_has_calls([
            mock.call(f"""{colorama.Style.BRIGHT}""", end=''),
            mock.call(f"""{colorama.Fore.GREEN}""", end=''),
            mock.call(f"""{colorama.Fore.RESET}""", end=''),
            mock.call(f"""{colorama.Style.RESET_ALL}""", end='')
        ])

    @patch("builtins.print")
    @patch("console.scan.scank", side_effect=["linkedin", "config", "help", "clear", "theme", "exit", "developer"])
    def test_scanBlue(self: TestScanFunctions, mock_scank: Mock, mock_print: Mock) -> None:
        self.assertTrue(scanBlue("LinkedIn/>") == "linkedin")
        mock_scank.assert_called_with("LinkedIn/>")
        mock_print.assert_has_calls([
            mock.call(f"""{colorama.Fore.BLUE}""", end=''), mock.call(f"""{colorama.Fore.RESET}""", end='')])

        self.assertTrue(scanBlue("LinkedIn/>") == "config")
        mock_scank.assert_called_with("LinkedIn/>")
        mock_print.assert_has_calls([
            mock.call(f"""{colorama.Fore.BLUE}""", end=''), mock.call(f"""{colorama.Fore.RESET}""", end='')])

        self.assertTrue(scanBlue("LinkedIn/>") == "help")
        mock_scank.assert_called_with("LinkedIn/>")
        mock_print.assert_has_calls([
            mock.call(f"""{colorama.Fore.BLUE}""", end=''), mock.call(f"""{colorama.Fore.RESET}""", end='')])

        self.assertTrue(scanBlue("LinkedIn/>") == "clear")
        mock_scank.assert_called_with("LinkedIn/>")
        mock_print.assert_has_calls([
            mock.call(f"""{colorama.Fore.BLUE}""", end=''), mock.call(f"""{colorama.Fore.RESET}""", end='')])

        self.assertTrue(scanBlue("LinkedIn/>") == "theme")
        mock_scank.assert_called_with("LinkedIn/>")
        mock_print.assert_has_calls([
            mock.call(f"""{colorama.Fore.BLUE}""", end=''), mock.call(f"""{colorama.Fore.RESET}""", end='')])

        self.assertTrue(scanBlue("LinkedIn/>") == "exit")
        mock_scank.assert_called_with("LinkedIn/>")
        mock_print.assert_has_calls([
            mock.call(f"""{colorama.Fore.BLUE}""", end=''), mock.call(f"""{colorama.Fore.RESET}""", end='')])

        self.assertTrue(scanBlue("LinkedIn/>") == "developer")
        mock_scank.assert_called_with("LinkedIn/>")
        mock_print.assert_has_calls([
            mock.call(f"""{colorama.Fore.BLUE}""", end=''), mock.call(f"""{colorama.Fore.RESET}""", end='')])

    @patch("builtins.print")
    @patch("console.scan.scank", return_value="linkedin")
    def test_scanBlue_parameter(self: TestScanFunctions, mock_scank: Mock, mock_print: Mock) -> None:
        scanBlue("LinkedIn/>", style='')
        self.assertFalse(mock_scank.called)
        self.assertFalse(mock_print.called)

        scanBlue("LinkedIn/>", style='b')
        mock_scank.assert_called_with("LinkedIn/>")
        mock_print.assert_has_calls([
            mock.call(f"""{colorama.Style.BRIGHT}""", end=''),
            mock.call(f"""{colorama.Fore.BLUE}""", end=''),
            mock.call(f"""{colorama.Fore.RESET}""", end=''),
            mock.call(f"""{colorama.Style.RESET_ALL}""", end='')
        ])

        scanBlue("LinkedIn/>", style='b', start='\n')
        mock_scank.assert_called_with("LinkedIn/>", start='\n')
        mock_print.assert_has_calls([
            mock.call(f"""{colorama.Style.BRIGHT}""", end=''),
            mock.call(f"""{colorama.Fore.BLUE}""", end=''),
            mock.call(f"""{colorama.Fore.RESET}""", end=''),
            mock.call(f"""{colorama.Style.RESET_ALL}""", end='')
        ])

        scanBlue("LinkedIn/>", style='b', start='\n', pad='1')
        mock_scank.assert_called_with("LinkedIn/>", start='\n', pad='1')
        mock_print.assert_has_calls([
            mock.call(f"""{colorama.Style.BRIGHT}""", end=''),
            mock.call(f"""{colorama.Fore.BLUE}""", end=''),
            mock.call(f"""{colorama.Fore.RESET}""", end=''),
            mock.call(f"""{colorama.Style.RESET_ALL}""", end='')
        ])

        scanBlue(
            "LinkedIn/>", style='b', start='\n', pad='1', end='\n')
        mock_scank.assert_called_with(
            "LinkedIn/>", start='\n', pad='1', end='\n')
        mock_print.assert_has_calls([
            mock.call(f"""{colorama.Style.BRIGHT}""", end=''),
            mock.call(f"""{colorama.Fore.BLUE}""", end=''),
            mock.call(f"""{colorama.Fore.RESET}""", end=''),
            mock.call(f"""{colorama.Style.RESET_ALL}""", end='')
        ])

    @patch("builtins.print")
    @patch("console.scan.scank", side_effect=["linkedin", "config", "help", "clear", "theme", "exit", "developer"])
    def test_scanYellow(self: TestScanFunctions, mock_scank: Mock, mock_print: Mock) -> None:
        self.assertTrue(scanYellow("LinkedIn/>") == "linkedin")
        mock_scank.assert_called_with("LinkedIn/>")
        mock_print.assert_has_calls([
            mock.call(f"""{colorama.Fore.YELLOW}""", end=''), mock.call(f"""{colorama.Fore.RESET}""", end='')])

        self.assertTrue(scanYellow("LinkedIn/>") == "config")
        mock_scank.assert_called_with("LinkedIn/>")
        mock_print.assert_has_calls([
            mock.call(f"""{colorama.Fore.YELLOW}""", end=''), mock.call(f"""{colorama.Fore.RESET}""", end='')])

        self.assertTrue(scanYellow("LinkedIn/>") == "help")
        mock_scank.assert_called_with("LinkedIn/>")
        mock_print.assert_has_calls([
            mock.call(f"""{colorama.Fore.YELLOW}""", end=''), mock.call(f"""{colorama.Fore.RESET}""", end='')])

        self.assertTrue(scanYellow("LinkedIn/>") == "clear")
        mock_scank.assert_called_with("LinkedIn/>")
        mock_print.assert_has_calls([
            mock.call(f"""{colorama.Fore.YELLOW}""", end=''), mock.call(f"""{colorama.Fore.RESET}""", end='')])

        self.assertTrue(scanYellow("LinkedIn/>") == "theme")
        mock_scank.assert_called_with("LinkedIn/>")
        mock_print.assert_has_calls([
            mock.call(f"""{colorama.Fore.YELLOW}""", end=''), mock.call(f"""{colorama.Fore.RESET}""", end='')])

        self.assertTrue(scanYellow("LinkedIn/>") == "exit")
        mock_scank.assert_called_with("LinkedIn/>")
        mock_print.assert_has_calls([
            mock.call(f"""{colorama.Fore.YELLOW}""", end=''), mock.call(f"""{colorama.Fore.RESET}""", end='')])

        self.assertTrue(scanYellow("LinkedIn/>") == "developer")
        mock_scank.assert_called_with("LinkedIn/>")
        mock_print.assert_has_calls([
            mock.call(f"""{colorama.Fore.YELLOW}""", end=''), mock.call(f"""{colorama.Fore.RESET}""", end='')])

    @patch("builtins.print")
    @patch("console.scan.scank", return_value="linkedin")
    def test_scanYellow_parameter(self: TestScanFunctions, mock_scank: Mock, mock_print: Mock) -> None:
        scanYellow("LinkedIn/>", style='')
        self.assertFalse(mock_scank.called)
        self.assertFalse(mock_print.called)

        scanYellow("LinkedIn/>", style='b')
        mock_scank.assert_called_with("LinkedIn/>")
        mock_print.assert_has_calls([
            mock.call(f"""{colorama.Style.BRIGHT}""", end=''),
            mock.call(f"""{colorama.Fore.YELLOW}""", end=''),
            mock.call(f"""{colorama.Fore.RESET}""", end=''),
            mock.call(f"""{colorama.Style.RESET_ALL}""", end='')
        ])

        scanYellow("LinkedIn/>", style='b', start='\n')
        mock_scank.assert_called_with("LinkedIn/>", start='\n')
        mock_print.assert_has_calls([
            mock.call(f"""{colorama.Style.BRIGHT}""", end=''),
            mock.call(f"""{colorama.Fore.YELLOW}""", end=''),
            mock.call(f"""{colorama.Fore.RESET}""", end=''),
            mock.call(f"""{colorama.Style.RESET_ALL}""", end='')
        ])

        scanYellow("LinkedIn/>", style='b', start='\n', pad='1')
        mock_scank.assert_called_with("LinkedIn/>", start='\n', pad='1')
        mock_print.assert_has_calls([
            mock.call(f"""{colorama.Style.BRIGHT}""", end=''),
            mock.call(f"""{colorama.Fore.YELLOW}""", end=''),
            mock.call(f"""{colorama.Fore.RESET}""", end=''),
            mock.call(f"""{colorama.Style.RESET_ALL}""", end='')
        ])

        scanYellow(
            "LinkedIn/>", style='b', start='\n', pad='1', end='\n')
        mock_scank.assert_called_with(
            "LinkedIn/>", start='\n', pad='1', end='\n')
        mock_print.assert_has_calls([
            mock.call(f"""{colorama.Style.BRIGHT}""", end=''),
            mock.call(f"""{colorama.Fore.YELLOW}""", end=''),
            mock.call(f"""{colorama.Fore.RESET}""", end=''),
            mock.call(f"""{colorama.Style.RESET_ALL}""", end='')
        ])

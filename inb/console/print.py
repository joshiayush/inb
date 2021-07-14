from typing import Any
from typing import Optional

from rich.style import Style
from rich.console import Console

from console import RED_HEX
from console import CYAN_HEX
from console import BLUE_HEX
from console import GREEN_HEX
from console import ORANGE_HEX


def inbprint(
    obj: Any,
    color: Optional[str] = None,
    link: Optional[str] = None,
    bold: Optional[bool] = False,
    blink: Optional[bool] = False,
    blink2: Optional[bool] = False,
    conceal: Optional[bool] = False,
    italic: Optional[bool] = False,
    reverse: Optional[bool] = False,
    strike: Optional[bool] = False,
    underline: Optional[bool] = False,
    underline2: Optional[bool] = False,
    frame: Optional[bool] = False,
    encircle: Optional[bool] = False,
    overline: Optional[bool] = False,
    end: Optional[str] = '\n'
) -> None:
    """Function inbprint() prints the given object out to the console using the rich
    library methods to print formatted text on the screen.

    :Args:
        - obj: {Any} object to print on the terminal
        - color: {Optional[str]} color of the text
        - link: {Optional[str]} if the object shows a link
        - bold: {Optional[str]} print bold text
        - blink: {Optional[str]} print blinking text
        - blink2: {Optional[str]} print fast blinking text
        - conceal: {Optional[str]} print concealed text
        - italic: {Optional[str]} print italic text
        - reverse: {Optional[str]} print reverse text
        - strike: {Optional[str]} add strike through the text
        - underline: {Optional[str]} add underline on the text 
        - underline2: {Optional[str]} add double underline on the text
        - frame: {Optional[str]} for framed text
        - encircle: {Optional[str]} for encircled text
        - overline: {Optional[str]} for overlined text

    :Returns:
        - {None}
    """
    def style() -> Style:
        """Function style() creates a Style object for the rich's print method.

        :Returns:
            - {Style}
        """
        _kwargs = {
            "link": link,
            "bold": bold,
            "blink": blink,
            "blink2": blink2,
            "conceal": conceal,
            "italic": italic,
            "reverse": reverse,
            "strike": strike,
            "underline": underline,
            "underline2": underline2,
            "frame": frame,
            "encircle": encircle,
            "overline": overline
        }
        if not color:
            return Style(**_kwargs)

        if color.lower() == 'r' or color.lower() == "red":
            return Style(color=RED_HEX, **_kwargs)

        if color.lower() == 'g' or color.lower() == "green":
            return Style(color=GREEN_HEX, **_kwargs)

        if color.lower() == 'b' or color.lower() == "blue":
            return Style(color=BLUE_HEX, **_kwargs)

        if color.lower() == 'c' or color.lower() == "cyan":
            return Style(color=CYAN_HEX, **_kwargs)

        if color.lower() == 'o' or color.lower() == "orange":
            return Style(color=ORANGE_HEX, **_kwargs)

    Console().print(obj, style=style(), end=end)

from typing import TextIO
from typing import Optional

from rich.console import Console

from . import DEFAULT
from . import RED_HEX
from . import CYAN_HEX
from . import BLUE_HEX
from . import GREEN_HEX
from . import ORANGE_HEX


def inbinput(
    prompt: str = "",
    color: Optional[str] = None,
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
    markup: Optional[bool] = True,
    emoji: Optional[bool] = True,
    password: Optional[bool] = False,
    stream: Optional[TextIO] = None
) -> str:
    """Function inbinput() displays a prompt and waits for input from the user. 
    The prompt may contain color / style.

    :Args:
        - prompt: {Union[str, Text]} Text to render in the prompt.
        - markup: {Optional[bool]} Enable console markup (requires a str prompt). Defaults to True.
        - emoji: {Optional[bool]} Enable emoji (requires a str prompt). Defaults to True.
        - password: {Optional[bool]} Hide typed text. Defaults to False.
        - stream: {Optional[bool]}} Optional file to read input from (rather than stdin). Defaults to None.

    :Returns:
        - {str} Text read from stdin.
    """
    styles: list = []

    if bold:
        styles.append("bold")
    if blink:
        styles.append("blink")
    if blink2:
        styles.append("blink2")
    if conceal:
        styles.append("conceal")
    if italic:
        styles.append("italic")
    if reverse:
        styles.append("reverse")
    if strike:
        styles.append("strike")
    if underline:
        styles.append("underline")
    if underline2:
        styles.append("underline2")
    if frame:
        styles.append("frame")
    if encircle:
        styles.append("encircle")
    if overline:
        styles.append("overline")

    if color:
        if color.lower() == 'g' or color.lower() == "green":
            styles.append(GREEN_HEX)
        elif color.lower() == 'r' or color.lower() == "red":
            styles.append(RED_HEX)
        elif color.lower() == 'b' or color.lower() == "blue":
            styles.append(BLUE_HEX)
        elif color.lower() == 'c' or color.lower() == "cyan":
            styles.append(CYAN_HEX)
        elif color.lower() == 'o' or color.lower() == "orange":
            styles.append(ORANGE_HEX)
        else:
            styles.append(DEFAULT)

    prompt = f"""[{' '.join(styles)}]{prompt}[/]"""

    return Console().input(
        prompt=prompt,
        markup=markup,
        emoji=emoji,
        password=password,
        stream=stream
    )

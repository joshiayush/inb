from typing import Any
from typing import TextIO
from typing import Optional

from rich.console import Console


def inbinput(
        prompt: str = "",
        markup: bool = True,
        emoji: bool = True,
        password: bool = False,
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
    return Console().input(
        prompt=prompt,
        markup=markup,
        emoji=emoji,
        password=password,
        stream=stream
    )

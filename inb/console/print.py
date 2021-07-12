from typing import Any

from rich.console import Console


def inbprint(object: Any,
             bold: bool = False,
             blink: bool = False,
             blink2: bool = False,
             concealed: bool = False,
             italic: bool = False,
             reverse: bool = False,
             strike: bool = False,
             underline: bool = False,
             underline2: bool = False,
             frame: bool = False,
             encircle: bool = False,
             overline: bool = False) -> None:
    styles: list = []

    def add(styles: list, style: str): return styles.append(
        style) if eval(style) else None

    add(styles=styles, style="bold")
    add(styles=styles, style="blink")
    add(styles=styles, style="blink2")
    add(styles=styles, style="concealed")
    add(styles=styles, style="italic")
    add(styles=styles, style="revers")
    add(styles=styles, style="strike")
    add(styles=styles, style="underline")
    add(styles=styles, style="underline2")
    add(styles=styles, style="frame")
    add(styles=styles, style="encircle")
    add(styles=styles, style="overline")

    Console().print(object, style=" ".join(styles))


def inbprintred(object: Any,
                bold: bool = False,
                blink: bool = False,
                blink2: bool = False,
                concealed: bool = False,
                italic: bool = False,
                reverse: bool = False,
                strike: bool = False,
                underline: bool = False,
                underline2: bool = False,
                frame: bool = False,
                encircle: bool = False,
                overline: bool = False) -> None:
    styles: list = []

    def add(styles: list, style: str): return styles.append(
        style) if eval(style) else None

    add(styles=styles, style="bold")
    add(styles=styles, style="blink")
    add(styles=styles, style="blink2")
    add(styles=styles, style="concealed")
    add(styles=styles, style="italic")
    add(styles=styles, style="revers")
    add(styles=styles, style="strike")
    add(styles=styles, style="underline")
    add(styles=styles, style="underline2")
    add(styles=styles, style="frame")
    add(styles=styles, style="encircle")
    add(styles=styles, style="overline")

    if len(styles) == 0:
        Console().print(object, style="red")
    else:
        Console().print(object, style=f"""{" ".join(styles)} on red""")


def inbprintgreen(object: Any,
                  bold: bool = False,
                  blink: bool = False,
                  blink2: bool = False,
                  concealed: bool = False,
                  italic: bool = False,
                  reverse: bool = False,
                  strike: bool = False,
                  underline: bool = False,
                  underline2: bool = False,
                  frame: bool = False,
                  encircle: bool = False,
                  overline: bool = False) -> None:
    styles: list = []

    def add(styles: list, style: str): return styles.append(
        style) if eval(style) else None

    add(styles=styles, style="bold")
    add(styles=styles, style="blink")
    add(styles=styles, style="blink2")
    add(styles=styles, style="concealed")
    add(styles=styles, style="italic")
    add(styles=styles, style="revers")
    add(styles=styles, style="strike")
    add(styles=styles, style="underline")
    add(styles=styles, style="underline2")
    add(styles=styles, style="frame")
    add(styles=styles, style="encircle")
    add(styles=styles, style="overline")

    if len(styles) == 0:
        Console().print(object, style="green")
    else:
        Console().print(object, style=f"""{" ".join(styles)} on green""")


def inbprintblue(object: Any,
                 bold: bool = False,
                 blink: bool = False,
                 blink2: bool = False,
                 concealed: bool = False,
                 italic: bool = False,
                 reverse: bool = False,
                 strike: bool = False,
                 underline: bool = False,
                 underline2: bool = False,
                 frame: bool = False,
                 encircle: bool = False,
                 overline: bool = False) -> None:
    styles: list = []

    def add(styles: list, style: str): return styles.append(
        style) if eval(style) else None

    add(styles=styles, style="bold")
    add(styles=styles, style="blink")
    add(styles=styles, style="blink2")
    add(styles=styles, style="concealed")
    add(styles=styles, style="italic")
    add(styles=styles, style="revers")
    add(styles=styles, style="strike")
    add(styles=styles, style="underline")
    add(styles=styles, style="underline2")
    add(styles=styles, style="frame")
    add(styles=styles, style="encircle")
    add(styles=styles, style="overline")

    if len(styles) == 0:
        Console().print(object, style="blue")
    else:
        Console().print(object, style=f"""{" ".join(styles)} on blue""")

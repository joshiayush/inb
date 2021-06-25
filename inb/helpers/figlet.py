import pyfiglet


def CreateFigletString(text: str, font: str = "standard", **kwargs) -> pyfiglet.FigletString:
    """Function CreateFigletString() takes ASCII text and returns it in ASCII art fonts. 
    figlet_format method convert ASCII text into ASCII art fonts.

    :Args:
        - text: ASCII text to convert to ASCII art fonts
        - font: font type { "standard", "slant", "3-d", "3x5", "5lineoblique", "alphabet", 
            "banner3-D", "doh", "isometric1", "letters", "alligator", "dotmatrix", "bubble", 
            "bulbhead", "digital" } for more fonts see http://www.figlet.org/fontdb.cgi
        - kwargs: keyword arguments

    :Returns:
        - ASCII art font
    """
    return pyfiglet.figlet_format(text=text, font=font, **kwargs)

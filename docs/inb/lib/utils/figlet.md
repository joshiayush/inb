# Figlet Service

This service provides a mechanism to create figlet string out of normal text.

This document has the following section:

- [System Call Interface](#system-call-interface)

## System Call Interface

- **Method CreateFigletString():**

  > ```python
  > def CreateFigletString(text: str, font: str = "standard", **kwargs) -> pyfiglet.FigletString:
  > ```
  >
  > This function takes in a string and returns the figlet form of it.
  > <br><br>
  > This function takes in one obligatory argument `text`, one optional argument `font` and variadic number of keyword arguments.
  > The argument `font` defines the style of the figlet string you will get. For more information on pyfiglet visit
  > [gfg][_gfgpyfiglet].

<!-- Definitions -->

[_gfgpyfiglet]: https://www.geeksforgeeks.org/python-ascii-art-using-pyfiglet-module/

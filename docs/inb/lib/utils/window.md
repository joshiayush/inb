# Windows Service

This service provides a mechanism to set or get the cursor position on the console. This service is required to alter the cursor
position while logging information on the console. This service provides a way to format the text output.

This document has the following sections:

- [Overview](#overview)
- [System Call Interface](#system-call-interface)

## Overview

**Terminal Class:**

> ```python
> class Terminal(object):
> ```
>
> This class provides an interface for `Windows` service. This class inherits from `object` class which is the default class of
> every class in python.

## System Call Interface

- **Method setcursorposition():**

  > This method is publicly available for every object of `Terminal` class.
  >
  > ```python
  > def setcursorposition(
  >     self: Terminal,
  >     x: int,
  >     y: int,
  >     file: TextIO = sys.stdout
  > ) -> None:
  > ```
  >
  > This method takes in three arguments, two are obligatory and one is optional.
  >
  > The arguments `x` and `y` determines the position of the cursor on the console or the file specified in the file argument. If
  > the `file` argument is not given or either is `None` it is defaulted to `sys.stdout` file.

- **Method getcursorposition():**

  > This method is publicly available for every object of `Terminal` class.
  >
  > ```python
  > def getcursorposition(self: Terminal) -> tuple:
  > ```
  >
  > This method returns a tuple containing the current `x` and `y` position of the cursor on the console respectively.

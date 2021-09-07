# Parser Service

This service provides a way to modify the built-in `argparse.ArgumentParser` service by overriding the methods it provides.

This document has the following sections:

- [NARGS](#nargs)
- [OPT_ARGS_ACTION](#optargsaction)
- [\_ArgumentParser](#argumentparser)

## NARGS

> This service is used with the method `add_argument()` to determine the number of arguments required. This service provides some
> constants listed below:
>
> ```python
> OPTIONAL = "?"        # 0 or one argument required
> ZERO_OR_MORE = "*"    # 0 or more arguments required
> ONE_OR_MORE = "+"     # 1 or more arguments required
> ```

## OPT_ARGS_ACTION

> This service provides the actions accepted by the `add_argument()` method while adding an optional argument.
>
> ```python
> COUNT = "count"                 # count the number of optional arguments given
> STORE_TRUE = "store_true"       # store true in case the optional argument is given
> ```

## \_ArgumentParser

This service provides the overrided implementation of the `argparse.ArgumentParser` class. With this implementation we can colorify
the text output on the console.

This document has the following sections for this service:

- [Overview](#overview)
- [System Call Interface](#system-call-interface)
- [System Internal Call Interface](#system-internal-call-interface)

## Overview

**\_ArgumentParser Class:**

> ```python
> class _ArgumentParser(argparse.ArgumentParser):
> ```
>
> This class has a base class `argparse.ArgumentParser` so that to inherit all of the functionality that `argparse.ArgumentParser`
> provides and therefore, later we have the flexibility to override the methods if we want.
> <br><br>
> The `_ArgumentParser` also have a private static variable called `__COLOR_DICT` that holds the ANSI Escape color codes to colorify
> the text output.

**\_ArgumentParser Constructor:**

> ```python
> def __init__(
>   self: ArgumentParser,
>   prog: str = None,
>   usage: str = None,
>   description: str = None,
>   epilog: str = None,
>   parents: List[ArgumentParser] = [],
>   formatter_class: type = HelpFormatter,
>   prefix_chars: str = '-',
>   fromfile_prefix_chars: str = None,
>   argument_default: str = None,
>   conflict_handler: str = 'error',
>   add_help: bool = True,
>   allow_abbrev: bool = True
> ) -> None:
> ```
>
> We don't override the base class constructor to avoid compatibility issues.
> <br><br>
> You should give the program name `prog`, `usage` and `description` for the the parser object you create. For more information
> you should look at [argparse][_argparse].

**\_ArgumentParser Destructor:**

> We don't have a destructor method for `arparse.ArgumentParser` class neither we create a custom destructor for `_ArgumentParser`
> class.

## System Call Interface

- **Method print_usage():**

  > ```python
  > def print_usage(self: _ArgumentParser, file: TextIO = None) -> None:
  > ```
  >
  > This method is publicly available for all of the instances of `_ArgumetParser`.
  > <br><br>
  > This method internally calls the public method `format_usage()` of `ArgumentParser` class to get a formatted string of usage.
  > Once this method has successfully received the formatted usage this method calls an internal overrided method of
  > `ArgumentParser` class `_print_message()` to dump the message on the ouput file.
  > <br><br>
  > This method takes in an argument `file` that specifies which file to dump the output on. If the argument `file` is `None` it
  > is defaulted to `sys.stdout`.

- **Method print_help():**

  > ```python
  > def print_help(self: _ArgumentParser, file: TextIO = None) -> None:
  > ```
  >
  > This method is publicly available to all of the instances of `_ArgumentParser`.
  > <br><br>
  > This method internally calls the public method `format_help()` of `ArgumentParser` class to get a formatted string of help.
  > Once this method has successfully received the formatted help this method calls an internal overrided method of
  > `ArgumentParser` class `_print_message()` to dump the message on the ouput file.
  > <br><br>
  > This method takes in an argument `file` that specifies which file to dump the output on. If the argument `file` is `None` it
  > is defaulted to `sys.stdout`.

- **Method exit():**

  > ```python
  > def exit(
  >     self: _ArgumentParser,
  >     status: int = 0,
  >     message: str = None
  > ) -> None:
  > ```
  >
  > This method is publicly available for all of the instances of `_ArgumentParser`.
  > <br><br>
  > This method takes in two arguments `status` and `message` both are optional. The `status` argument is used to exit the program
  > using the `sys.exit()` method with the current exit status. The `message` argument if given is displayed on the screen before
  > calling the `sys.exit()` method.

- **Method error():**

  > ```python
  > def error(
  >     self: _ArgumentParser,
  >     message: str,
  >     usage: bool = True
  > ) -> None:
  > ```
  >
  > This method is publicly available for all of the instances of `_ArgumentParser`.
  > <br><br>
  > This method takes in two arguments `message` and `usage`. Argument `message` is obligatory, it is the message to dump on the
  > screen informing the user about the error that occured. Argument `usage` is optional, it is a boolean value which if set to
  > `True` also shows the usage of the program.

## System Internal Call Interface

- **Method \_print_message():**

  > ```python
  > def _print_message(
  >     self: _ArgumentParser,
  >     message: str,
  >     file: TextIO = None,
  >     color: str = None
  > ) -> None:
  > ```
  >
  > This method is a private method of `_ArgumentParser` class.
  > <br><br>
  > This method takes in three arguments `message`, `file` and `color`. Argument `message` is the object that we need to dump on
  > the given file. Argument `file` is the file on which we need to dump the given message, if this argument is `None` then it is
  > defaulted to `sys.stdout`. Argument `color` is the color that we need to apply on the `message` given, if this argument is
  > `None` the given message remains same.

<!-- Definitions -->

[_argparse]: https://docs.python.org/3/library/argparse.html

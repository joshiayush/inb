# linkedin-bot cli

### Update

**Command Line Interface** will be implemented using [`argparse`][_argparse] library.

Now we have to refactor the entire `main.py` file.

## argparse.ArgumentParser

```python
class argparse.ArgumentParser(
        prog=None,
        usage=None,
        description=None,
        epilog=None,
        parents=[],
        formatter_class=argparse.HelpFormatter,
        prefix_chars='-',
        fromfile_prefix_chars=None,
        argument_default=None,
        conflict_handler='error',
        add_help=True,
        allow_abbrev=True,
        exit_on_error=True)
```

Create a new [`ArgumentParser`][_argparse_argument_parser] object. All parameters should be passed as keyword arguments.

- [prog][_argparse_prog] - The name of the program (default: `sys.argv[0]`)
- [usage][_argparse_usage] - The string describing the program usage (default: generated from arguments added to parser)
- [description][_argparse_description] - Text to display before the argument help (default: none)
- [epilog][_argparse_epilog] - Text to display after the argument help (default: none)
- [parents][_argparse_parents] - A list of [ArgumentParser][_argparse_argument_parser] objects whose arguments should also be included
- [formatter_class][_argparse_formatter_class] - A class for customizing the help output
- [prefix_chars][_argparse_prefix_chars] - The set of characters that prefix optional arguments (default: `‘-‘`)
- [fromfile_prefix_chars][_argparse_fromfile_prefix_chars] - The set of characters that prefix files from which additional arguments should be read (default: `None`)
- [argument_default][_argparse_argument_default] - The global default value for arguments (default: `None`)
- [conflict_handler][_argparse_conflict_handler] - The strategy for resolving conflicting optionals (usually unnecessary)
- [add_help][_argparse_add_help] - Add a `-h/--help` option to the parser (default: `True`)
- [allow_abbrev][_argparse_allow_abbrev] - Allows long options to be abbreviated if the abbreviation is unambiguous. (default: `True`)

### CreateParser

```python
def CreateParser(
        prog: str,
        usage: str,
        description: str,
        epilog: str = '',
        parents: list = [],
        formatter_class: object = argparse.HelpFormatter,
        prefix_chars: str = '-',
        fromfile_prefix_chars: str = '',
        argument_default: Any = ...,
        conflict_handler: str = "error",
        add_help: bool = True,
        allow_abbrev: bool = True) -> argparse.ArgumentParser:
    """Function to create a new ArgumentParser object for our cli.

    :Args:
        - prog: The name of the program (default: sys.argv[0])
        - usage: The string describing the program usage (default: generated from arguments added to parser)
        - description: Text to display before the argument help (default: none)
        - epilog: Text to display after the argument help (default: none)
        - parents: A list of ArgumentParser objects whose arguments should also be included
        - formatter_class: A class for customizing the help output
        - prefix_chars: The set of characters that prefix optional arguments (default: ‘-‘)
        - fromfile_prefix_chars: The set of characters that prefix files from which additional arguments should
            be read (default: None)
        - argument_default: The global default value for arguments (default: None)
        - conflict_handler: The strategy for resolving conflicting optionals (usually unnecessary)
        - add_help: Add a -h/--help option to the parser (default: True)
        - allow_abbrev: Allows long options to be abbreviated if the abbreviation is unambiguous. (default: True)z

    :Returns:
        - {arparse.ArgumentParser}
    """
    return argparse.ArgumentParser(
        prog=prog,
        usage=usage,
        description=description,
        epilog=epilog,
        parents=parents,
        formatter_class=formatter_class,
        prefix_chars=prefix_chars,
        fromfile_prefix_chars=fromfile_prefix_chars,
        argument_default=argument_default,
        conflict_handler=conflict_handler,
        add_help=add_help,
        allow_abbrev=allow_abbrev)
```

Function `CreateParser()` will help to create a `ArgumentParser` object for us. This way we are also obeying the `SOLID` design
principle which we will be following throughout this project.

<!-- Definitions -->

[_argparse]: https://docs.python.org/3/library/argparse.html
[_argparse_argument_parser]: https://docs.python.org/3/library/argparse.html#argparse.ArgumentParser
[_argparse_prog]: https://docs.python.org/3/library/argparse.html#prog
[_argparse_usage]: https://docs.python.org/3/library/argparse.html#usage
[_argparse_description]: https://docs.python.org/3/library/argparse.html#description
[_argparse_epilog]: https://docs.python.org/3/library/argparse.html#epilog
[_argparse_parents]: https://docs.python.org/3/library/argparse.html#parents
[_argparse_formatter_class]: https://docs.python.org/3/library/argparse.html#formatter-class
[_argparse_prefix_chars]: https://docs.python.org/3/library/argparse.html#prefix-chars
[_argparse_fromfile_prefix_chars]: https://docs.python.org/3/library/argparse.html#fromfile-prefix-chars
[_argparse_argument_default]: https://docs.python.org/3/library/argparse.html#argument-default
[_argparse_conflict_handler]: https://docs.python.org/3/library/argparse.html#conflict-handler
[_argparse_add_help]: https://docs.python.org/3/library/argparse.html#add-help
[_argparse_allow_abbrev]: https://docs.python.org/3/library/argparse.html#allow-abbrev

# linkedin-bot cli

This documentation describes how I have utilize `argparse` to create a cli for **linkedin-bot**.

## `argparse.ArgumentParser`

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

### `CreateParser()`

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

## Commands

Now to add commands we will use the method `add_argument()` of the `ArgumentParser` object.

### The `add_argument()` method

```python
ArgumentParser.add_argument(
    name or flags...
    [, action]
    [, nargs]
    [, const]
    [, default]
    [, type]
    [, choices]
    [, required]
    [, help]
    [, metavar]
    [, dest])
```

Define how a single command-line argument should be parsed.

- [name or flag][_argparse_add_argument_name_or_flag] - Either a name or a list of option strings, e.g. `foo` or `-f`, `--foo`.
- [action][_argparse_add_argument_action] - The basic type of action to be taken when this argument is encountered at the command line.
- [nargs][_argparse_add_argument_nargs] - The number of command-line arguments that should be consumed.
- [const][_argparse_add_argument_const] - A constant value required by some [action][_argparse_add_argument_action] and [nargs][_argparse_add_argument_nargs] selections.
- [default][_argparse_argument_default] - The value produced if the argument is absent from the command line and if it is absent from the namespace object.
- [type][_argparse_add_argument_type] - The type to which the command-line argument should be converted.
- [choices][_argparse_add_argument_choices] - A container of the allowable values for the argument.
- [required][_argparse_add_argument_required] - Whether or not the command-line option may be omitted (optionals only).
- [help][_argparse_add_argument_help] - A brief description of what the argument does.
- [metavar][_argparse_add_argument_metavar] - A name for the argument in usage messages.
- [dest][_argparse_add_argument_dest] - The name of the attribute to be added to the object returned by [parse_args()][_argparse_parse_args].

## Sub-commands

### The `add_subparsers()` method

```python
ArgumentParser.add_subparsers(
    [title]
    [, description]
    [, prog]
    [, parser_class]
    [, action]
    [, option_string]
    [, dest]
    [, required]
    [, help]
    [, metavar])
```

[ArgumentParser][_argparse_argument_parser] supports the creation of such sub-commands with the [add_subparsers()][_argparse_add_subparsers] method. The [add_subparsers()][_argparse_add_subparsers] method is normally called with no arguments and returns a special action object. This object has a single method, `add_parser()`, which takes a command name and any [ArgumentParser][_argparse_argument_parser] constructor arguments, and returns an [ArgumentParser][_argparse_argument_parser] object that can be modified as usual.

- title - title for the sub-parser group in help output; by default “subcommands” if description is provided, otherwise uses title for positional arguments.
- description - description for the sub-parser group in help output, by default `None`.
- prog - usage information that will be displayed with sub-command help, by default the name of the program and any positional arguments before the subparser argument.
- parser_class - class which will be used to create sub-parser instances, by default the class of the current parser (e.g. `ArgumentParser`).
- [action][_argparse_add_subparsers_action] - the basic type of action to be taken when this argument is encountered at the command line.
- [dest][_argparse_add_subparsers_dest] - name of the attribute under which sub-command name will be stored; by default `None` and no value is stored.
- [required][_argparse_add_subparsers_required] - Whether or not a subcommand must be provided, by default `False` (added in 3.7).
- [help][_argparse_add_subparsers_help] - help for sub-parser group in help output, by default `None`.
- [metavar][_argparse_add_subparsers_metavar] - string presenting available sub-commands in help; by default it is `None` and presents sub-commands in form {cmd1, cmd2, ...}.

Creating the `send` command.

```python
parser = CreateParser(
    description=f"""LinkedIn Bash, version {__version__}(1)-release (lbot-{__version__})\n"""
    """These commands are defined internally. Type '--help' to see this list.\n"""
    """Type (command) --help to know more about that command.\n\n"""
    """A ([]) around a command means that the command is optional.\n""")

subparsers = parser.add_subparsers(help="help text")

send = subparsers.add_parser("send", help="help text")
send.add_argument(
    "-c", "--cookies", action="store_true", help="help text")
send.add_argument(
    "-ngpu", "--headless", action="store_true", help="help text")
send.set_defaults(headless=False, cookies=False)
```

To check how sub-commands work go to the documentation [argparse.add_subparsers][_argparse_add_subparsers]

<!-- Definitions -->

<!-- argparse -->

[_argparse]: https://docs.python.org/3/library/argparse.html

<!-- argument_parser -->

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

<!-- argument_parser_add_argument -->

[_argparse_add_argument_name_or_flag]: https://docs.python.org/3/library/argparse.html#name-or-flags
[_argparse_add_argument_action]: https://docs.python.org/3/library/argparse.html#action
[_argparse_add_argument_nargs]: https://docs.python.org/3/library/argparse.html#nargs
[_argparse_add_argument_const]: https://docs.python.org/3/library/argparse.html#const
[_argparse_add_argument_default]: https://docs.python.org/3/library/argparse.html#default
[_argparse_add_argument_type]: https://docs.python.org/3/library/argparse.html#type
[_argparse_add_argument_choices]: https://docs.python.org/3/library/argparse.html#choices
[_argparse_add_argument_required]: https://docs.python.org/3/library/argparse.html#required
[_argparse_add_argument_help]: https://docs.python.org/3/library/argparse.html#help
[_argparse_add_argument_metavar]: https://docs.python.org/3/library/argparse.html#metavar
[_argparse_add_argument_dest]: https://docs.python.org/3/library/argparse.html#dest

<!-- parse_args -->

[_argparse_parse_args]: https://docs.python.org/3/library/argparse.html#argparse.ArgumentParser.parse_args

<!-- argument_parser_add_subparser -->

[_argparse_add_subparsers]: https://docs.python.org/3/library/argparse.html#argparse.ArgumentParser.add_subparsers
[_argparse_add_subparsers_action]: https://docs.python.org/3/library/argparse.html#action
[_argparse_add_subparsers_dest]: https://docs.python.org/3/library/argparse.html#dest
[_argparse_add_subparsers_required]: https://docs.python.org/3/library/argparse.html#required
[_argparse_add_subparsers_help]: https://docs.python.org/3/library/argparse.html#help
[_argparse_add_subparsers_metavar]: https://docs.python.org/3/library/argparse.html#metavar

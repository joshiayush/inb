from linkedin import __version__


def get_lbot_description() -> str:
    """Function get_lbot_description() returns the description for linkedin-bot.

    :Args:
        - {None}

    :Returns:
        - {str}
    """
    return (
        f"""LinkedIn Bash, version {__version__}(1)-release (lbot-{__version__})\n"""
        """These commands are defined internally. Type '--help' to see this list\n"""
        """Type (command) --help to know more about that command""")


def get_send_description() -> str:
    """Function get_send_description() returns the description for 'send' command.

    :Args:
        - {None}

    :Returns:
        - {str}
    """
    return ("""Command 'send' sends invitation to people on linkedin.""")


def get_send_help() -> str:
    """Function get_send_help() returns the help text for 'send' command.

    :Args:
        - {None}

    :Returns:
        - {str}
    """
    return ("""Command 'send' sends invitation to people on linkedin.""")


def get_invitation_limit_description() -> str:
    """Function get_invitation_limit_description() returns the description for 'limit' flag.

    :Args:
        - {None}

    :Returns:
        - {str}
    """
    return (
        """Flag 'limit' is used to set the daily invitation limit\n"""
        """Limit must not exceed by 80 otherwise you'll be blocked for a entire\n"""
        """week""")


def get_invitation_limit_help() -> str:
    """Function get_invitation_limit_help() returns the help text for 'limit' flag.

    :Args:
        - {None}

    :Returns:
        - {str}
    """
    return ("""Flag 'limit' sets the daily invitation limit""")


def get_config_description() -> str:
    """Function get_config_description() returns the description for 'config' command.

    :Args:
        - {None}

    :Returns:
        - {str}
    """
    return (
        """Command 'config' is used to add user's credentials to the database\n"""
        """Adding user's credentials to the database for ever or until user deletes\n"""
        """them makes it feasible for user to send invitations without entering the\n"""
        """fields again and again""")


def get_config_help() -> str:
    """Function get_config_help() returns the help text for 'config' command.

    :Args:
        - {None}

    :Returns:
        - {str}
    """
    return ("""Command 'config' is used to store user's credentials""")


def get_show_description() -> str:
    """Function get_show_description() returns the description for 'show' command.

    :Args:
        - {None}

    :Returns:
        - {str}
    """
    return (
        """Command 'show' prints the information stored in the database\n"""
        """For example -> email, password ...""")


def get_show_help() -> str:
    """Function get_show_help() returns the help text for 'show' command.

    :Args:
        - {None}

    :Returns:
        - {str}
    """
    return ("""Command 'show' prints the information that is in the database""")


def get_delete_description() -> str:
    """Function get_delete_description() returns the description for 'delete' command.

    :Args:
        - {None}

    :Returns:
        - {str}
    """
    return (
        """Command 'delete' deletes the information stored in the database\n"""
        """'delete' deletes information like 'key', 'cookies' ...""")


def get_delete_help() -> str:
    """Function get_delete_help() returns the help text for 'delete' command.

    :Args:
        - {None}

    :Returns:
        - {str}
    """
    return ("""Command 'delete' deletes the information stored in the database""")


def get_developer_description() -> None:
    """Function get_developer_description() returns the description 'developer' command.

    :Args:
        - {None}

    :Returns:
        - {str}
    """
    return ("""Command 'developer' prints the information about the author""")


def get_developer_help() -> None:
    """Function get_developer_help() returns the help text for 'developer' command.

    :Args:
        - {None}

    :Returns:
        - {str}
    """
    return ("""Command 'developer' prints the information about the author""")

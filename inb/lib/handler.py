import argparse

from .command import handle_send_command
from .command import handle_show_command
from .command import handle_config_command
from .command import handle_delete_command
from .command import handle_developer_command


def CommandHandler(namespace: argparse.Namespace) -> None:
    if namespace.which == "send":
        try:
            handle_send_command(namespace=namespace)
        except Exception as e:
            raise e
        return

    if namespace.which == "show":
        try:
            handle_show_command(namespace=namespace)
        except Exception as e:
            raise e
        return

    if namespace.which == "config":
        try:
            handle_config_command(namespace=namespace)
        except Exception as e:
            raise e
        return

    if namespace.which == "delete":
        try:
            handle_delete_command(namespace=namespace)
        except Exception as e:
            raise e
        return

    if namespace.which == "developer":
        try:
            handle_developer_command(namespace=namespace)
        except Exception as e:
            raise e
        return

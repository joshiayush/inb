import argparse
from sqlite3.dbapi2 import Error

from database import database_path
from database.sql.sql import Database

from .invitation import SendInvitation


def handle_send_command(namespace: argparse.Namespace) -> None:
    if not namespace.cookies:
        if not namespace.EMAIL:
            raise argparse.ArgumentTypeError(
                "Value of type EMAIL can not be None!")

        if not namespace.PASSWORD:
            raise argparse.ArgumentTypeError(
                "Value of type PASSWORD can not be None!")

        SendInvitation({"user_email": namespace.EMAIL, "user_password": namespace.PASSWORD},
                       _limit=namespace.limit, headless=namespace.headless)

        return

    try:
        _db = Database(database=Database)
    except Error as e:
        raise e

    """Pass"""

def handle_show_command(namespace: argparse.Namespace) -> None:
    """Show the information stored in the database."""

    """Put all the information in front of the user."""
    pass


def handle_config_command(namespace: argparse.Namespace) -> None:
    """Throw the email and password in the database."""

    """Ask user to enter its email and password."""
    pass


def handle_delete_command(namespace: argparse.Namespace) -> None:
    """Delete the given value from the database."""

    """Check what the user wants to delete."""

    """Delete information from the database."""

    """Dump database if user wants so."""
    pass


def handle_developer_command(namespace: argparse.Namespace) -> None:
    """Show developer details."""

    """Check what flag is passed and then throw the information"""

    """Print every information if no flag is used."""
    pass

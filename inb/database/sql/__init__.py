"""from __future__ imports must occur at the beginning of the file. DO NOT CHANGE!"""
from __future__ import annotations

import sqlite3

from urllib.request import pathname2url

from errors.error import DatabaseDoesNotExistException

__all__ = ["SQL"]


class SQL(object):
    """Class SQL defines a prototype for the database api that we are going to use
    in this project for performing CRUD operations.
    """

    def __init__(self: SQL, database: str, mode: str) -> None:
        """Constructor method opens a sqlite3 connection.

        :Args:
            - self: {SQL}
            - database: {str} database path
            - mode: {str} connection mode

        :Raises:
            - {DatabaseDoesNotExistException} if there is an OperationalError.
        """
        try:
            self._connection = sqlite3.connect(
                database="file:%s?mode=%s" % (pathname2url(database), mode), uri=True)
        except sqlite3.OperationalError as e:
            raise DatabaseDoesNotExistException(
                "Database %s does not exist to perform (%s) operations" % (database, mode))

    def connection(self: SQL) -> sqlite3.Connection:
        """Method connection() returns the connection object formed during the initialisation
        of SQL object.

        :Args:
            - self: {SQL}

        :Returns:
            - {sqlite3.Connection}
        """
        return self._connection

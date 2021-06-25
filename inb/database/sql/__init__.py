"""from __future__ imports must occur at the beginning of the file. DO NOT CHANGE!"""
from __future__ import annotations

import sqlite3

from urllib.request import pathname2url


class SQL(object):

    def __init__(self: SQL, database: str = '', mode: str = '') -> None:
        try:
            self._connection = sqlite3.connect(
                database="file:%s?mode=%s" % (pathname2url(database), mode), uri=True)
        except sqlite3.OperationalError as e:
            raise e

    def commit(self: SQL) -> None:
        self._connection.commit()

    def close(self: SQL) -> None:
        self._connection.close()

    def connection(self: SQL) -> sqlite3.Connection:
        return self._connection

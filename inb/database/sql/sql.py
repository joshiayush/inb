"""from __future__ imports must occur at the beginning of the file. DO NOT CHANGE!"""
from __future__ import annotations

from typing import Any

from . import SQL


class Database(SQL):

    def __init__(self: Database, database: str, mode: str) -> None:
        super(SQL, self).__init__(database=database, mode=mode)

    def create(self: Database, table: str, **kwargs):
        self.connection().cursor().execute(
            f"""CREATE TABLE {table} 
            ({", ".join(["%s %s" % (key, value) for (key, value) in zip(
            kwargs.keys(), kwargs.values())])});""")

    def insert(self: Database, table: str, **kwargs):
        self.connection().cursor().execute(
            f"""INSERT INTO {table} ({", ".join([f"{col}" for col in kwargs.keys()])}) 
            VALUES ({", ".join(["'%s'" % (val) for val in kwargs.values()])});""")

    def read(self: Database, table: str, rows: str, *args) -> Any:
        if rows == "*":
            return self.connection().execute(
                f"""SELECT {", ".join(args)} FROM sqlite_master WHERE type='table' AND NAME='{table}';""").fetchall()

        if rows == ".":
            return self.connection().execute(
                f"""SELECT {", ".join(args)} FROM sqlite_master WHERE type='table' AND NAME='{table}';""").fetchone()

    def update(self: Database, table: str, where: str, **kwargs):
        if not where:
            self.connection().cursor().execute(
                f"""UPDATE {table}
                SET {", ".join(["%s = '%s'" % (col, val) for (col, val) in zip(
                    kwargs.keys(), kwargs.values())])};""")
        else:
            self.connection().cursor().execute(
                f"""UPDATE {table}
                SET {", ".join(["%s = '%s'" % (col, val) for (col, val) in zip(
                    kwargs.keys(), kwargs.values())])}
                WHERE {where};""")

    def delete(self: Database, table: str, where: str = None):
        if not where:
            self.connection().cursor().execute(
                f"""DELETE FROM {table};""")
        else:
            self.connection().cursor().execute(
                f"""DELETE FROM {table} WHERE {where};""")

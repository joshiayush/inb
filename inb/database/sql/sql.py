"""from __future__ imports must occur at the beginning of the file. DO NOT CHANGE!"""
from __future__ import annotations

from typing import Any

from rich.table import Table
from rich.console import Console

from . import SQL

from errors import DatabaseDoesNotExistException

__all__ = ["NAME_INDEX",
           "EMAIL_INDEX",
           "PASSWORD_INDEX",
           "ENCRYPTION_KEY_INDEX",
           "NAME_COLUMN",
           "EMAIL_COLUMN",
           "PASSWORD_COLUMN",
           "ENCRYPTION_KEY_COLUMN",
           "USERS_TABLE",
           "Database"]

NAME_INDEX: int = 0
EMAIL_INDEX: int = 1
PASSWORD_INDEX: int = 2
ENCRYPTION_KEY_INDEX: int = 3

NAME_COLUMN: str = "Name"
EMAIL_COLUMN: str = "Email"
PASSWORD_COLUMN: str = "Password"
ENCRYPTION_KEY_COLUMN: str = "Key"

USERS_TABLE = "Users"


class Database(SQL):
  """Class Database"""

  def __init__(self: Database, database: str, mode: str) -> None:
    try:
      super(SQL, self).__init__(database=database, mode=mode)
    except DatabaseDoesNotExistException as e:
      raise e

  def create(self: Database, table: str, **kwargs):
    self.connection().cursor().execute(
        f"""CREATE TABLE {table} 
            ({", ".join(["%s %s" % (key, value) for (key, value) in zip(
            kwargs.keys(), kwargs.values())])});""")

  def insert(self: Database, table: str, **kwargs):
    self.connection().cursor().execute(
        f"""INSERT INTO {table} ({", ".join([f"{col}" for col in kwargs.keys()])}) 
            VALUES ({", ".join(["'%s'" % (val) for val in kwargs.values()])});""")

  def read(
          self: Database, *args: list, table: str, rows: str,
          where: str = None) -> Any:
    if where == None or where.strip() == '':
      if rows == "*":
        return self.connection().execute(
            f"""SELECT {", ".join(args)} FROM sqlite_master WHERE type='table' AND NAME='{table}';""").fetchall()

      if rows == ".":
        return self.connection().execute(
            f"""SELECT {", ".join(args)} FROM sqlite_master WHERE type='table' AND NAME='{table}';""").fetchone()
    else:
      if rows == "*":
        return self.connection().execute(
            f"""SELECT {", ".join(args)} FROM sqlite_master WHERE type='table' AND NAME='{table}' AND {where};"""
        ).fetchall()

      if rows == ".":
        return self.connection().execute(
            f"""SELECT {", ".join(args)} FROM sqlite_master WHERE type='table' AND NAME='{table}' AND {where};"""
        ).fetchone()

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

  def print(self: Database, table: str, rows: list) -> None:
    _table = Table(title="%s Databse" % (table))

    _table.add_column("Name", justify="center", no_wrap=True)
    _table.add_column("Email", justify="center", no_wrap=True)
    _table.add_column("Password", justify="center", no_wrap=True)
    _table.add_column("Key", justify="center", no_wrap=True)

    for _row in rows:
      _table.add_row(*_row)

    Console().print(table)

from __future__ import annotations

__name__ = "creds"
__package__ = "creds"

from cryptography.fernet import Fernet

from database import database_path
from database.sql.sql import Database

from errors.error import DatabaseDoesNotExistException


class Creds(object):

  def get_key(self: Creds):
    try:
      _database = Database(database=database_path, mode="rw")

      fernet_key = _database.read("Key", table="Users", rows=".")
    except DatabaseDoesNotExistException:
      fernet_key = Fernet.generate_key()

      _database = Database(database=database_path, mode="rwc")

      _database.create(
          "Users", Name="varchar(255)", Email="varchar(255)",
          Password="varchar(255)", Key="varchar(255)")
      _database.insert(
          "Users", Name="", Email="", Password="",
          Key=str(Fernet.generate_key()))

    _database.commit()
    _database.close()

    return fernet_key

  def get_database_path(self: Creds):
    return database_path

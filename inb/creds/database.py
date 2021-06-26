from __future__ import annotations

from database.sql.sql import Database

from creds.cipher import Cipher

from errors.error import UserCacheNotFoundException
from errors.error import DatabaseDoesNotExistException


class CipherDatabase(Cipher):

    def __init__(self: CipherDatabase) -> None:
        super(Cipher, self).__init__()

    def post_user_info(self: CipherDatabase, email: str, password: str, name: str = None) -> None:
        """Method post_creds() stores the user secret fields as cache in a database 
        'database.db' inside of the 'db' folder that is inside of the project's root directory 
        so to use these fields later.

        :Args:
            - email: email to store in the database.
            - password: password to store in the database.
            - name: name to store in the database.

        :Returns:
            - {None}
        """
        _database = Database(database=self.get_database_path(), mode="rwc")

        _database.create(
            "Users", Name="varchar(255)", Email="varchar(255)", Password="varchar(255)", Key="varchar(255)")
        _database.insert(
            "Users", Name=name if not name == None else "", Email=self.encrypt(email), Password=self.encrypt(password),
            Key=self.get_key())

        _database.commit()
        _database.close()

    def get_user_info(self: CipherDatabase) -> dict:
        """Method get_user_info() reads the credentials stored as cache in database 
        'database.db' inside of the 'db' folder that is inside of the project's root directory 
        if exists.

        :Args:
            - self: {} object from which 'data' property is to be accessed.

        :Raises:
            - {UserCacheNotFoundException} if user's credentials are not found.

        :Returns:
            - {None}
        """
        try:
            _database = Database(database=self.get_database_path(), mode="rw")
        except DatabaseDoesNotExistException:
            raise UserCacheNotFoundException(
                "Database doesn't have any cache stored")

        row = _database.read("Email", "Password", table="Users", rows=".")

        return {"user_email": self.decrypt(row[0]), "user_password": self.decrypt(row[1])}

    def delete_user_info(self: CipherDatabase) -> None:
        """Method delete_user_info() deletes the stored cache (User credentials) if exists.

        :Args:
            - self: {CipherDatabase}

        :Returns:
            - {None}
        """
        try:
            _database = Database(database=self.get_database_path(), mode="rw")
        except DatabaseDoesNotExistException:
            raise DatabaseDoesNotExistException(
                "Database doesn't exist!\n Can't perform delete operation!")

        _database.delete("Users")

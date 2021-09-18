# MIT License
#
# Copyright (c) 2019 Creative Commons
#
# Permission is hereby granted, free of charge, to any person obtaining a
# copy of this software and associated documentation files (the "Software"),
# to deal in the Software without restriction, including without limitation
# the rights to use, copy, modify, merge, publish, distribute, sublicense,
# and/or sell copies of the Software, and to permit persons to whom the
# Software is furnished to do so, subject to the following conditions
#
# The above copyright notice and this permission notice shall be included
# in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS
# OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.

# from __future__ imports must occur at the beginning of the file. DO NOT CHANGE!
from __future__ import annotations

from database.sql.sql import Database

from creds.cipher import Cipher

from errors import DatabaseDoesNotExistException


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
            - {DatabaseDoesNotExistException} if user's credentials are not found.

        :Returns:
            - {None}
        """
        try:
            _database = Database(database=self.get_database_path(), mode="rw")
        except DatabaseDoesNotExistException as exc:
            raise DatabaseDoesNotExistException(
                "Database doesn't have any cache stored") from exc

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
        except DatabaseDoesNotExistException as exc:
            raise DatabaseDoesNotExistException(
                "Database doesn't exist!\n Can't perform delete operation!") from exc

        _database.delete("Users")

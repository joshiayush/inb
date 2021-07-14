"""from __future__ imports must occur at the beginning of the file. DO NOT CHANGE!"""
from __future__ import annotations

import argparse

from typing import Any
from typing import List

from console.input import inbinput

from database import SQL_DATABASE_PATH
from database.sql.sql import Database
from database.sql.sql import USERS_TABLE
from database.sql.sql import NAME_COLUMN
from database.sql.sql import EMAIL_COLUMN
from database.sql.sql import PASSWORD_COLUMN
from database.sql.sql import EMAIL_INDEX
from database.sql.sql import PASSWORD_INDEX

from errors.error import CredentialsNotFoundException
from errors.error import ConnectionLimitExceededException


class CommandHelper(object):
    def __init__(self: CommandHelper, namespace: argparse.Namespace) -> None:
        if namespace.which == "send":
            self.__send(namespace)
        elif namespace.which == "show":
            self.__show(namespace)
        elif namespace.which == "config":
            self.__config(namespace)
        elif namespace.which == "delete":
            self.__delete(namespace)
        elif namespace.which == "developer":
            self.__developer(namespace)

    def __send(self: CommandHelper, namespace: argparse.Namespace) -> None:
        self.email: str = namespace.email
        self.password: str = namespace.password
        self.cookies: bool = namespace.cookies

        if ((self.email == None or self.email.strip() == '') or (self.password == None or self.password.strip() == '')) \
                and not self.cookies:
            raise CredentialsNotFoundException(
                "User did not provide credentials!")

        def get_cookies() -> Any:
            return Database(database=SQL_DATABASE_PATH).read(
                NAME_COLUMN,
                EMAIL_COLUMN,
                PASSWORD_COLUMN,
                table=USERS_TABLE,
                rows="*")

        def get_user_choice(rows: List) -> int:
            Database(database=SQL_DATABASE_PATH).print(USERS_TABLE, rows=rows)
            return inbinput("Enter your email: ", bold=True)

        if self.cookies:
            Cookies = get_cookies()

            if len(Cookies) > 1:
                self.email = get_user_choice(Cookies)
                self.password = Database(database=SQL_DATABASE_PATH).read(
                    EMAIL_COLUMN, PASSWORD_COLUMN, USERS_TABLE, rows=".", where="Email = '%s'" % (self.email))[PASSWORD_INDEX]
            else:
                self.email = Cookies[EMAIL_INDEX]
                self.password = Cookies[PASSWORD_INDEX]

        self.limit = namespace.limit

        if self.limit > 80:
            raise ConnectionLimitExceededException(
                "Daily connection limit can't exceed by 80!")

        self.headless = namespace.headless
        self.incognito = namespace.incognito
        self.start_maximized = namespace.start_maximized

    def __show(self: CommandHelper) -> None:
        pass

    def __delete(self: CommandHelper) -> None:
        pass

    def __config(self: CommandHelper) -> None:
        pass

    def __developer(self: CommandHelper) -> None:
        pass

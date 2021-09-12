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

import argparse

from typing import Any

from console.input import inbinput

from database import SQL_DATABASE_PATH
from database.sql.sql import Database
from database.sql.sql import USERS_TABLE
from database.sql.sql import NAME_COLUMN
from database.sql.sql import EMAIL_COLUMN
from database.sql.sql import PASSWORD_COLUMN
from database.sql.sql import EMAIL_INDEX
from database.sql.sql import PASSWORD_INDEX

from lib import Validator

from errors import CredentialsNotGivenException


class CommandValueParser(object):
    def __init__(self: CommandValueParser, namespace: argparse.Namespace) -> None:
        if namespace.which == "send":
            self.__send(namespace)
        elif namespace.which == "connect":
            self.__connect(namespace)
        elif namespace.which == "search":
            self.__search(namespace)
        elif namespace.which == "show":
            self.__show(namespace)
        elif namespace.which == "config":
            self.__config(namespace)
        elif namespace.which == "delete":
            self.__delete(namespace)
        elif namespace.which == "developer":
            self.__developer(namespace)

    def __send(self: CommandValueParser, namespace: argparse.Namespace) -> None:
        is_creds_given: bool = True
        if namespace.email:
            if Validator(namespace.email).is_email():
                self.email = namespace.email
            else:
                raise CredentialsNotGivenException("Email %(email)s is not a valid email" % {
                    "email": namespace.email})
        else:
            self.email = None
            is_creds_given = False
        if namespace.password and not namespace.password.strip() == '':
            self.password = namespace.password
        else:
            self.password = None
            is_creds_given = False
        self.cookies: bool = namespace.cookies

        if not is_creds_given and not self.cookies:
            raise CredentialsNotGivenException(
                "User did not provide credentials!")

        def get_cookies() -> Any:
            return Database(database=SQL_DATABASE_PATH).read(NAME_COLUMN,
                                                             EMAIL_COLUMN,
                                                             PASSWORD_COLUMN,
                                                             table=USERS_TABLE,
                                                             rows="*")

        def get_user_choice(rows: list) -> int:
            Database(database=SQL_DATABASE_PATH).print(USERS_TABLE, rows=rows)
            return inbinput("Enter your email: ", bold=True)

        if self.cookies:
            Cookies = get_cookies()

            if len(Cookies) > 1:
                self.email = get_user_choice(Cookies)
                self.password = Database(database=SQL_DATABASE_PATH).read(EMAIL_COLUMN,
                                                                          PASSWORD_COLUMN,
                                                                          USERS_TABLE,
                                                                          rows=".",
                                                                          where="Email = '%s'" % (self.email))[PASSWORD_INDEX]
            else:
                self.email = Cookies[EMAIL_INDEX]
                self.password = Cookies[PASSWORD_INDEX]

        self.limit = namespace.limit if type(
            namespace.limit) is int else int(namespace.limit) if type(namespace.limit) is str else 20
        self.headless = namespace.headless
        self.incognito = namespace.incognito
        self.start_maximized = namespace.start_maximized

    def __search(self: CommandValueParser, namespace: argparse.Namespace) -> None:
        is_creds_given: bool = True
        if namespace.email:
            if Validator(namespace.email).is_email():
                self.email = namespace.email
            else:
                raise CredentialsNotGivenException("Email %(email)s is not a valid email" % {
                    "email": namespace.email})
        else:
            self.email = None
            is_creds_given = False
        if namespace.password and not namespace.password.strip() == '':
            self.password = namespace.password
        else:
            self.password = None
            is_creds_given = False
        self.cookies: bool = namespace.cookies

        if not is_creds_given and not self.cookies:
            raise CredentialsNotGivenException(
                "User did not provide credentials!")

        def get_cookies() -> Any:
            return Database(database=SQL_DATABASE_PATH).read(NAME_COLUMN,
                                                             EMAIL_COLUMN,
                                                             PASSWORD_COLUMN,
                                                             table=USERS_TABLE,
                                                             rows="*")

        def get_user_choice(rows: list) -> int:
            Database(database=SQL_DATABASE_PATH).print(USERS_TABLE, rows=rows)
            return inbinput("Enter your email: ", bold=True)

        if self.cookies:
            Cookies = get_cookies()

            if len(Cookies) > 1:
                self.email = get_user_choice(Cookies)
                self.password = Database(database=SQL_DATABASE_PATH).read(EMAIL_COLUMN,
                                                                          PASSWORD_COLUMN,
                                                                          USERS_TABLE,
                                                                          rows=".",
                                                                          where="Email = '%s'" % (self.email))[PASSWORD_INDEX]
            else:
                self.email = Cookies[EMAIL_INDEX]
                self.password = Cookies[PASSWORD_INDEX]

        if namespace.keyword and not namespace.keyword.strip() == '':
            self.keyword = namespace.keyword
        else:
            self.keyword = None
        if namespace.location and ":" in namespace.location:
            self.location = namespace.location.split(":")
            for i in range(len(self.location)):
                if self.location[i].strip() == '':
                    self.location = self.location[:i:] + self.location[i+1::]
        else:
            if namespace.location and not namespace.location.strip() == '':
                self.location = namespace.location
            else:
                self.location = None
        if namespace.title and not namespace.title.strip() == '':
            self.title = namespace.title
        else:
            self.title = None
        if namespace.first_name and not namespace.first_name.strip() == '':
            self.first_name = namespace.first_name
        else:
            self.first_name = None
        if namespace.last_name and not namespace.last_name.strip() == '':
            self.last_name = namespace.last_name
        else:
            self.last_name = None
        if namespace.school and not namespace.school.strip() == '':
            self.school = namespace.school
        else:
            self.school = None
        if namespace.industry and ":" in namespace.industry:
            self.industry = namespace.industry.split(":")
            for i in range(len(self.industry)):
                if self.industry[i].strip() == '':
                    self.industry = self.industry[:i:] + self.industry[i+1::]
        else:
            if namespace.industry and not namespace.industry.strip() == '':
                self.industry = namespace.industry.strip()
            else:
                self.industry = None
        if namespace.current_company and not namespace.current_company.strip() == '':
            self.current_company = namespace.current_company
        else:
            self.current_company = None
        if namespace.profile_language and ":" in namespace.profile_language:
            self.profile_language = namespace.profile_language.split(":")
            for i in range(len(self.profile_language)):
                if self.profile_language[i].strip() == '':
                    self.profile_language = self.profile_language[:i:] + \
                        self.profile_language[i+1::]
        else:
            if namespace.profile_language and not namespace.profile_language.strip() == '':
                self.profile_language = namespace.profile_language
            else:
                self.profile_language = None
        self.limit = namespace.limit if type(
            namespace.limit) is int else int(namespace.limit) if type(namespace.limit) is str else 20
        self.headless = namespace.headless
        self.incognito = namespace.incognito
        self.start_maximized = namespace.start_maximized

    def __connect(self: CommandValueParser, namespace: argparse.Namespace) -> None:
        is_creds_given: bool = True
        if namespace.email:
            if Validator(namespace.email).is_email():
                self.email = namespace.email
            else:
                raise CredentialsNotGivenException("Email %(email)s is not a valid email" % {
                    "email": namespace.email})
        else:
            self.email = None
            is_creds_given = False
        if namespace.password and not namespace.password.strip() == '':
            self.password = namespace.password
        else:
            self.password = None
            is_creds_given = False
        self.cookies: bool = namespace.cookies

        if not is_creds_given and not self.cookies:
            raise CredentialsNotGivenException(
                "User did not provide credentials!")

        def get_cookies() -> Any:
            return Database(
                database=SQL_DATABASE_PATH).read(NAME_COLUMN,
                                                 EMAIL_COLUMN,
                                                 PASSWORD_COLUMN,
                                                 table=USERS_TABLE,
                                                 rows="*")

        def get_user_choice(rows: list) -> int:
            Database(database=SQL_DATABASE_PATH).print(USERS_TABLE, rows=rows)
            return inbinput("Enter your email: ", bold=True)

        if self.cookies:
            Cookies = get_cookies()

            if len(Cookies) > 1:
                self.email = get_user_choice(Cookies)
                self.password = Database(
                    database=SQL_DATABASE_PATH).read(EMAIL_COLUMN,
                                                     PASSWORD_COLUMN,
                                                     USERS_TABLE,
                                                     rows=".",
                                                     where="Email = '%s'" % (self.email))[PASSWORD_INDEX]
            else:
                self.email = Cookies[EMAIL_INDEX]
                self.password = Cookies[PASSWORD_INDEX]

        self.profileid = namespace.profileid
        self.headless = namespace.headless
        self.incognito = namespace.incognito
        self.start_maximized = namespace.start_maximized

    def __show(self: CommandValueParser, namespace: argparse.Namespace) -> None:
        pass

    def __delete(self: CommandValueParser, namespace: argparse.Namespace) -> None:
        pass

    def __config(self: CommandValueParser, namespace: argparse.Namespace) -> None:
        pass

    def __developer(self: CommandValueParser, namespace: argparse.Namespace) -> None:
        pass

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
import functools

from typing import Any

from database import SQL_DATABASE_PATH
from database.sql.sql import Database
from database.sql.sql import USERS_TABLE
from database.sql.sql import NAME_COLUMN
from database.sql.sql import EMAIL_COLUMN
from database.sql.sql import PASSWORD_COLUMN
from database.sql.sql import EMAIL_INDEX
from database.sql.sql import PASSWORD_INDEX

from lib import is_int
from lib import is_str
from lib import is_empty
from lib import is_present
from lib import Validator

from errors import CredentialsNotGivenException


class CommandValueParser(object):
    def __init__(self: CommandValueParser, namespace: argparse.Namespace) -> None:
        if namespace.which == "send":
            self._send(namespace)
        elif namespace.which == "connect":
            self._connect(namespace)
        elif namespace.which == "search":
            self._search(namespace)
        elif namespace.which == "show":
            self._show(namespace)
        elif namespace.which == "config":
            self._config(namespace)
        elif namespace.which == "delete":
            self._delete(namespace)
        elif namespace.which == "developer":
            self._developer(namespace)

    def _parse_creds(function_: function) -> function:
        @functools.wraps(function_)
        def wrapper(self: CommandValueParser, *args, **kwargs) -> None:
            nonlocal function_
            namespace = args[0]
            is_creds_given: bool = True

            # parse the email given, we want to set the email to NoneType object
            # if the email is empty, moreover we only go inside of the clause once
            # we have confirmed that the email is not a NoneType object
            self.email = None
            if namespace.email:
                if Validator(namespace.email).is_email():
                    self.email = namespace.email
                else:
                    raise CredentialsNotGivenException("Email %(email)s is not valid!" % {
                                                       "email": namespace.email})
            else:
                is_creds_given = False

            # parse the password given, we want to set the password to NoneType object
            # if the password is empty, moreover we only go inside of the clause once
            # we have confirmed that the password is not a NoneType object
            self.password = None
            if namespace.password:
                if not is_empty(namespace.password):
                    self.password = namespace.password
                else:
                    self.password = None
            else:
                is_creds_given = False

            self.cookies: bool = namespace.cookies
            if not is_creds_given and not self.cookies:
                raise CredentialsNotGivenException(
                    "User did not provide credentials!")

            def get_cookies() -> Any:
                return Database(
                    database=SQL_DATABASE_PATH).read(
                        NAME_COLUMN,
                        EMAIL_COLUMN,
                        PASSWORD_COLUMN,
                        table=USERS_TABLE,
                        rows="*")

            def get_user_choice(rows: list) -> int:
                Database(database=SQL_DATABASE_PATH).print(
                    USERS_TABLE,
                    rows=rows)
                return input("Enter your email: ", bold=True)

            if self.cookies:
                Cookies = get_cookies()
                if len(Cookies) > 1:
                    self.email = get_user_choice(Cookies)
                    self.password = Database(
                        database=SQL_DATABASE_PATH).read(
                            EMAIL_COLUMN,
                            PASSWORD_COLUMN,
                            USERS_TABLE,
                            rows=".",
                            where="Email = '%s'" % (self.email))[PASSWORD_INDEX]
                else:
                    self.email = Cookies[EMAIL_INDEX]
                    self.password = Cookies[PASSWORD_INDEX]
            function_(self, *args, **kwargs)
        return wrapper

    def _parse_inb_opt_params(function_: function) -> function:
        @functools.wraps(function_)
        def wrapper(self: CommandValueParser, *args, **kwargs) -> None:
            nonlocal function_
            function_(self, *args, **kwargs)
            namespace = args[0]
            self.debug = namespace.debug
            self.headless = namespace.headless
            self.incognito = namespace.incognito
            self.start_maximized = namespace.start_maximized
        return wrapper

    @_parse_creds
    @_parse_inb_opt_params
    def _send(self: CommandValueParser, namespace: argparse.Namespace) -> None:
        # parse the limit given, we want to set the limit to 20 if the limit is
        # a string and cannot be converted into an integer with base 10
        self.limit = 20
        if is_int(namespace.limit):
            self.limit = namespace.limit
        else:
            if is_str(namespace.limit):
                try:
                    self.limit = int(namespace.limit)
                # ValueError will be raised if the namespace.limit is not a valid number string
                except ValueError:
                    self.limit = 20
            else:
                self.limit = 20

    @_parse_creds
    @_parse_inb_opt_params
    def _search(self: CommandValueParser, namespace: argparse.Namespace) -> None:
        # parse the keyword given, we want to set the keyword to NoneType object
        # if the keyword is empty, moreover we only go inside of the clause once
        # we have confirmed that the keyword is not a NoneType object
        self.keyword = None
        if namespace.keyword:
            if not is_empty(namespace.keyword):
                self.keyword = namespace.keyword
            else:
                self.keyword = None

        # parse the location given, we want to set the location to NoneType object
        # if the location is empty, moreover we only go inside of the clause once
        # we have confirmed that the location is not a NoneType object
        self.location = None
        if namespace.location:
            # if ':' is present in the location string it means that the user gave us
            # more than one location separated by ':' and we want to convert the location
            # object to a list object filled with the locations
            if is_present(':', namespace.location):
                self.location = namespace.location.split(':')
                self.location = filter(
                    lambda location: not is_empty(location), self.location)
            else:
                if is_empty(namespace.location):
                    self.location = namespace.location
                else:
                    self.location = None

        # parse the title given, we want to set the title to NoneType object
        # if the title is empty, moreover we only go inside of the clause once
        # we have confirmed that the title is not a NoneType object
        self.title = None
        if namespace.title:
            if is_empty(namespace.title):
                self.title = namespace.title
            else:
                self.title = None

        # parse the first_name given, we want to set the first_name to NoneType object
        # if the first_name is empty, moreover we only go inside of the clause once
        # we have confirmed that the first_name is not a NoneType object
        self.first_name = None
        if namespace.first_name:
            if not is_empty(namespace.first_name):
                self.first_name = namespace.first_name
            else:
                self.first_name = None

        # parse the last_name given, we want to set the last_name to NoneType object
        # if the last_name is empty, moreover we only go inside of the clause once
        # we have confirmed that the last_name is not a NoneType object
        self.last_name = None
        if namespace.last_name:
            if not is_empty(namespace.last_name):
                self.last_name = namespace.last_name
            else:
                self.last_name = None

        # parse the school given, we want to set the school to NoneType object
        # if the school is empty, moreover we only go inside of the clause once
        # we have confirmed that the school is not a NoneType object
        self.school = None
        if namespace.school:
            if not is_empty(namespace.school):
                self.school = namespace.school
            else:
                self.school = None

        # parse the industry given, we want to set the industry to NoneType object
        # if the industry is empty, moreover we only go inside of the clause once
        # we have confirmed that the industry is not a NoneType object
        self.industry = None
        if namespace.industry:
            # if ':' is present in the industry string it means that the user gave us
            # more than one industry separated by ':' and we want to convert the industry
            # object to a list object filled with the industries
            if is_present(':', namespace.industry):
                self.industry = namespace.industry.split(':')
                self.industry = filter(
                    lambda industry: not is_empty(industry), self.industry)
            else:
                if not is_empty(namespace.industry):
                    self.industry = namespace.industry.strip()
                else:
                    self.industry = None

        # parse the current_company given, we want to set the current_company to NoneType object
        # if the current_company is empty, moreover we only go inside of the clause once
        # we have confirmed that the current_company is not a NoneType object
        self.current_company = None
        if namespace.current_company:
            if not is_empty(namespace.current_company):
                self.current_company = namespace.current_company
            else:
                self.current_company = None

        # parse the profile_language given, we want to set the profile_language to NoneType object
        # if the profile_language is empty, moreover we only go inside of the clause once
        # we have confirmed that the profile_language is not a NoneType object
        self.profile_language = None
        if namespace.profile_language:
            # if ':' is present in the profile language string it means that the user gave us
            # more than one profile language separated by ':' and we want to convert the profile language
            # object to a list object filled with the profile languages
            if is_present(':', namespace.profile_language):
                self.profile_language = namespace.profile_language.split(':')
                self.profile_language = filter(
                    lambda language: not is_empty(language), self.profile_language)
            else:
                if not is_empty(namespace.profile_language):
                    self.profile_language = namespace.profile_language
                else:
                    self.profile_language = None

        # parse the limit given, we want to set the limit to 20 if the limit is
        # a string and cannot be converted into an integer with base 10
        self.limit = 20
        if is_int(namespace.limit):
            self.limit = namespace.limit
        else:
            if is_str(namespace.limit):
                try:
                    self.limit = int(namespace.limit)
                # ValueError will be raised if the namespace.limit is not a valid number string
                except ValueError:
                    self.limit = 20
            else:
                self.limit = 20

    @_parse_creds
    @_parse_inb_opt_params
    def _connect(self: CommandValueParser, namespace: argparse.Namespace) -> None:
        self.profileid = None
        if namespace.profileid:
            if not is_empty(namespace.profileid):
                self.profileid = namespace.profileid
            else:
                self.profileid = None

    def _show(self: CommandValueParser, namespace: argparse.Namespace) -> None:
        pass

    def _delete(self: CommandValueParser, namespace: argparse.Namespace) -> None:
        pass

    def _config(self: CommandValueParser, namespace: argparse.Namespace) -> None:
        pass

    def _developer(self: CommandValueParser, namespace: argparse.Namespace) -> None:
        pass

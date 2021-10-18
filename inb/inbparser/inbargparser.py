"""
This module provides service to validate values given by the user over the cli
to call the APIs according to the action selected.

Supported Actions
~~~~~~~~~~~~~~~~~

  - send                Sends invitation to people on linkedin.
  - connect             Connects you with the given profile.
  - search              Searches people on LinekdIn and then invites them.
  - config              Used to store user's credentials
  - show                Prints the information that is in the database
  - delete              Deletes the information stored in the database
  - developer           Prints the information about the author

  :author: Ayush Joshi, ayush854032@gmail.com
  :copyright: Copyright (c) 2019 Creative Commons
  :license: MIT License, see license for details
"""

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

from typing import (
  Any,
  Dict,
  List,
)

from database import SQL_DATABASE_PATH
from database.sql.sql import (
  Database,
  USERS_TABLE,
  NAME_COLUMN,
  EMAIL_COLUMN,
  PASSWORD_COLUMN,
  EMAIL_INDEX,
  PASSWORD_INDEX,
)

from lib import Validator

from errors import CredentialsNotGivenException


class InbArgParser:
  def __init__(
          self: InbArgParser, namespace: argparse.Namespace) -> None:
    """Constructor method validates the `argparse` `namespace` given by the
    caller.

    Args:
      self: (InbArgParser) Self.
      namespace: (argparse.Namespace) Namespace to validate.

    Example:
    >>> from argparse import Namespace
    >>> from inbparser.inbargparser import InbArgParser
    >>>
    >>> namespace = Namespace(which='send', email=None, password=None)
    >>> parser = InbArgParser(namespace) # This will raise CredentialsNotGivenException
    """
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
    """Decorator `_parse_creds()` adds a `wrapper` around the function given. This
    decorator is then used to validate the user email and password fields.

    This decorator also seeks into the database to find information stored if in case
    user wants to use information from there.

    Args:
      function_: (function) Function to decorate.

    Returns:
      function: Decorated function.

    Example:
    >>> class InbArgParser:
    ...   @_parse_creds
    ...   def _send(self: InbArgParser, namespace: argparse.Namespace) -> Any:
    ...     # Your code goes here
    """
    @functools.wraps(function_)
    def wrapper(
            self: InbArgParser, *args: List[Any],
            **kwargs: Dict[Any, Any]) -> None:
      nonlocal function_
      namespace = args[0]
      is_creds_given = True

      # parse the email given, we want to set the email to NoneType object
      # if the email is empty, moreover we only go inside of the clause once
      # we have confirmed that the email is not a NoneType object
      self.email = None
      if namespace.email:
        if Validator(namespace.email).is_email():
          self.email = namespace.email
        else:
          raise CredentialsNotGivenException(
              "Email %(email)s is not a valid email address!" %
              {"email": namespace.email})
      else:
        is_creds_given = False

      # parse the password given, we want to set the password to NoneType object
      # if the password is empty, moreover we only go inside of the clause once
      # we have confirmed that the password is not a NoneType object
      self.password = None
      if namespace.password:
        self.password = namespace.password
      else:
        is_creds_given = False

      self.cookies = namespace.cookies
      if not is_creds_given and not self.cookies:
        raise CredentialsNotGivenException(
            "User did not provide credentials!")

      def get_cookies() -> Any:
        return Database(database=SQL_DATABASE_PATH).read(
            NAME_COLUMN,
            EMAIL_COLUMN,
            PASSWORD_COLUMN,
            table=USERS_TABLE,
            rows="*"
        )

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
    """Decorator `_parse_inb_opt_params()` adds a `wrapper` around the function
    given. This `wrapper` is then used to parse the optional parameters given by
    the user over the cli.

    Args:
      function_: (function) Function to decorate.

    Returns:
      function: Decorated function.

    Example:
    >>> class InbArgParser:
    ...   @_parse_inb_opt_params
    ...   def _send(self: InbArgParser, namespace: argparse.Namespace) -> Any:
    ...     # Your code goes here
    """
    @functools.wraps(function_)
    def wrapper(self: InbArgParser, *args, **kwargs) -> None:
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
  def _send(self: InbArgParser, namespace: argparse.Namespace) -> None:
    """Method `send()` parses the limit given through the namespace.

    Args:
      self: (InbArgParser) Self.
      namespace: (argparse.Namespace) Namespace.
    """
    # parse the limit given, we want to set the limit to 20 if the limit is
    # a string and cannot be converted into an integer with base 10
    if namespace.limit:
      self.limit = namespace.limit
    else:
      self.limit = 20

  @_parse_creds
  @_parse_inb_opt_params
  def _search(
          self: InbArgParser, namespace: argparse.Namespace) -> None:
    """Method `search()` parses the `search` command arguments except for user
    credentials and optional paramters.

    Args:
      self: (InbArgParser) Self.
      namespace: (argparse.Namespace) Namespace.
    """
    # parse the keyword given, we want to set the keyword to NoneType object
    # if the keyword is empty, moreover we only go inside of the clause once
    # we have confirmed that the keyword is not a NoneType object
    if namespace.keyword:
      self.keyword = namespace.keyword
    else:
      self.keyword = None

    # parse the location given, we want to set the location to NoneType object
    # if the location is empty, moreover we only go inside of the clause once
    # we have confirmed that the location is not a NoneType object
    if namespace.location:
      # if ':' is present in the location string it means that the user gave us
      # more than one location separated by ':' and we want to convert the location
      # object to a list object filled with the locations
      if ':' in namespace.location:
        self.location = namespace.location.split(':')
        self.location = filter(
            lambda location: location, self.location)
      else:
        self.location = namespace.location
    else:
      self.location = None

    # parse the title given, we want to set the title to NoneType object
    # if the title is empty, moreover we only go inside of the clause once
    # we have confirmed that the title is not a NoneType object
    if namespace.title:
      self.title = namespace.title
    else:
      self.title = None

    # parse the first_name given, we want to set the first_name to NoneType object
    # if the first_name is empty, moreover we only go inside of the clause once
    # we have confirmed that the first_name is not a NoneType object
    if namespace.first_name:
      self.first_name = namespace.first_name
    else:
      self.first_name = None

    # parse the last_name given, we want to set the last_name to NoneType object
    # if the last_name is empty, moreover we only go inside of the clause once
    # we have confirmed that the last_name is not a NoneType object
    if namespace.last_name:
      self.last_name = namespace.last_name
    else:
      self.last_name = None

    # parse the school given, we want to set the school to NoneType object
    # if the school is empty, moreover we only go inside of the clause once
    # we have confirmed that the school is not a NoneType object
    if namespace.school:
      self.school = namespace.school
    else:
      self.school = None

    # parse the industry given, we want to set the industry to NoneType object
    # if the industry is empty, moreover we only go inside of the clause once
    # we have confirmed that the industry is not a NoneType object
    if namespace.industry:
      # if ':' is present in the industry string it means that the user gave us
      # more than one industry separated by ':' and we want to convert the industry
      # object to a list object filled with the industries
      if ':' in namespace.industry:
        self.industry = namespace.industry.split(':')
        self.industry = filter(
            lambda industry: industry, self.industry)
      else:
        self.industry = namespace.industry.strip()
    else:
      self.industry = None

    # parse the current_company given, we want to set the current_company to NoneType object
    # if the current_company is empty, moreover we only go inside of the clause once
    # we have confirmed that the current_company is not a NoneType object
    if namespace.current_company:
      self.current_company = namespace.current_company
    else:
      self.current_company = None

    # parse the profile_language given, we want to set the profile_language to NoneType object
    # if the profile_language is empty, moreover we only go inside of the clause once
    # we have confirmed that the profile_language is not a NoneType object
    if namespace.profile_language:
      # if ':' is present in the profile language string it means that the user gave us
      # more than one profile language separated by ':' and we want to convert the profile language
      # object to a list object filled with the profile languages
      if ':' in namespace.profile_language:
        self.profile_language = namespace.profile_language.split(':')
        self.profile_language = filter(
            lambda language: language, self.profile_language)
      else:
        self.profile_language = namespace.profile_language
    else:
      self.profile_language = None

    # parse the limit given, we want to set the limit to 20 if the limit is
    # a string and cannot be converted into an integer with base 10
    if namespace.limit:
      self.limit = namespace.limit
    else:
      self.limit = 20

  @_parse_creds
  @_parse_inb_opt_params
  def _connect(
          self: InbArgParser, namespace: argparse.Namespace) -> None:
    """Method `connect()` parses the profileid given through the namespace.

    Args:
      self: (InbArgParser) Self.
      namespace: (argparse.Namespace) Namespace.
    """
    if namespace.profileid:
      self.profileid = namespace.profileid
    else:
      self.profileid = None

  def _show(self: InbArgParser, namespace: argparse.Namespace) -> None:
    pass

  def _delete(
          self: InbArgParser, namespace: argparse.Namespace) -> None:
    pass

  def _config(
          self: InbArgParser, namespace: argparse.Namespace) -> None:
    pass

  def _developer(self: InbArgParser,
                 namespace: argparse.Namespace) -> None:
    pass

"""
This module provides corresponding method calls to the actions selected by
the user.

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

import logging
import argparse
import functools

from typing import (
  Any,
  List,
  Dict,
)

from selenium.common.exceptions import (
  TimeoutException,
)

from errors import (
  InternetNotConnectedException,
)

from linkedin import Driver
from linkedin.login import LinkedIn
from linkedin.connect import (
  LinkedInConnect,
  LinkedInConnectViaId,
  LinkedInSearchConnect,
)

from lib import (
  DRIVER_PATH,
  __project_name__,
  ping,
)

from .inbargparser import InbArgParser


class Command(InbArgParser):
  """Class `Command` acts as a medium between the `cli` and `LinkedIn` APIs.

  This class takes the arguments given by the user over the `cli`, validates them
  and serves them to the `LinkedIn` APIs.
  """

  def __init__(self: Command, namespace: argparse.Namespace) -> None:
    """Constructor method validates the arguments given over the `cli` and once
    the arguments are validated it also sets a `logger` for the current instance.

    Args:
      self: (Command) Self.
      namespace: (argparse.Namespace) `argparse` namespace object.

    Example:
    >>> from argparse import Namespace
    >>> from inbparser import Command
    >>>
    >>> namespace = Namespace(which='send', email='ayush854032@gmail.com',
    ...               password='xxx-xxx-xxx', headless=True, limit=20, debug=False,
    ...               cookies=False, start_maximized=True, incognito=True)
    >>> command = Command(namespace)
    """
    super(Command, self).__init__(namespace=namespace)

    # Initialise the logging configurations
    logging.basicConfig(format="%(levelname)s:%(message)s")
    self.logger = logging.getLogger(__project_name__)
    self.logger.setLevel(logging.INFO)

  def _check_net_stat(function_: function) -> function:
    """Decorater `_check_net_stat()` adds a `wrapper` around a function. This `wrapper`
    is then used to check the current network status of your system.

    Args:
      function_: (function) Function to decorate.

    Returns:
      function: Decorated method.

    Raises:
      InternetNotConnectedException: In case weak network is found.

    Example:
    >>> class Command(InbArgParser):
    ...   '''Class `Command` acts as a medium between the `cli` and `LinkedIn` APIs.
    ...
    ...   This class takes the arguments given by the user over the `cli`, validates them
    ...   and serves them to the `LinkedIn` APIs.
    ...   '''
    ...   @_check_net_stat
    ...   def _login(function_: function) -> function:
    ...     # Your login API call goes here
    ...     ...
    """
    @functools.wraps(function_)
    def wrapper(
            self: Command, *args: List[Any],
            **kwargs: Dict[Any, Any]) -> None:
      nonlocal function_
      self.logger.info("Checking network status")
      if not ping("linkedin.com"):
        raise InternetNotConnectedException("Weak network found")
      self.logger.info("Internet is connected")
      function_(self, *args, **kwargs)
    return wrapper

  def _login(function_: function) -> function:
    """Decorator `_login()` adds a `wrapper` around a function. This `wrapper` is then
    used to call the `LinkedIn` login APIs to log you into your account.

    Args:
      function_: (function) Function to decorate.

    Returns:
      function: Decorated function.

    Example:
    >>> class Command(InbArgParser):
    ...   '''Class `Command` acts as a medium between the `cli` and `LinkedIn` APIs.
    ...   
    ...   This class takes the arguments given by the user over the `cli`, validates them
    ...   and serves them to the `LinkedIn` APIs.
    ...   '''
    ...   @_login
    ...   def _send(function_: function) -> function:
    ...     # Your send API call goes here
    ...     ...
    """
    @functools.wraps(function_)
    def wrapper(
            self: Command, *args: List[Any],
            **kwargs: Dict[Any, Any]) -> None:
      nonlocal function_

      # Initialise driver options object
      chrome_driver_options: List[str] = []
      chrome_driver_options.append(Driver.INCOGNITO)
      chrome_driver_options.append(Driver.IGNORE_CERTIFICATE_ERRORS)
      if self.headless == True:
        chrome_driver_options.append(Driver.HEADLESS)
        chrome_driver_options.append(
            Driver.DEFAULT_HEADLESS_WINDOW_SIZE)
        chrome_driver_options.append(Driver.START_MAXIMIZED)

      # Instantiate LinkedIn login API
      self.linkedin = LinkedIn(
          user_email=self.email, user_password=self.password,
          driver_path=DRIVER_PATH,
          opt_chromedriver_options=chrome_driver_options)

      self.logger.info("Connecting")
      self.logger.info("Sending GET request to login page")
      self.logger.info(
          "Logging in LinkedIn account (user-id=%(user_id)s)" %
          {"user_id": self.email})

      try:
        self.linkedin.login()  # call login method
      except TimeoutException as error:
        self.logger.critical(error)
        return
      else:
        self.logger.info("Successfully connected")

      function_(self, *args, **kwargs)
    return wrapper

  @_check_net_stat
  @_login
  def send(self: Command) -> None:
    """Method `send()` initialises an instance of `LinkedInConnect` API.

    This instance is then used to send connection request to suggested people over
    LinkedIn.

    Args:
      self: (Command) Self.

    Example:
    >>> from argparse import Namespace
    >>> from inbparser import Command
    >>>
    >>> namespace = Namespace(which='send', email='ayush854032@gmail.com',
    ...               password='xxx-xxx-xxx', headless=True, limit=20, debug=False,
    ...               cookies=False, start_maximized=True, incognito=True)
    >>> command = Command(namespace)
    >>> command.send()
    """
    self.logger.info("Instantiating connection object")
    linkedinconnect = LinkedInConnect(
      driver=self.linkedin.driver, limit=self.limit)

    self.logger.info("Sending GET request to mynetwork page")
    try:
      linkedinconnect.run()
    except TimeoutException as error:
      self.logger.critical(error)
      return

  @_check_net_stat
  @_login
  def connect(self: Command) -> None:
    """Method `connect()` initialises an instance of `LinkedInConnectViaId` API.

    This instance is then used to send connection request to the person with the
    specified profile id.

    Args:
      self: (Command) Self.

    Example:
    >>> from argparse import Namespace
    >>> from inbparser import Command
    >>>
    >>> namespace = Namespace(which='connect', email='ayush854032@gmail.com', 
    ...               password='xxx-xxx-xxx', profileid='xxx-xxx-xxx', headless=True, 
    ...               debug=False, cookies=False, start_maximized=True, incognito=True)
    >>> command = Command(namespace)
    >>> command.connect()
    """
    self.logger.info("Instantiating connection object")
    linkedinconnectid = LinkedInConnectViaId(
        driver=self.linkedin.driver, person_id=self.personid)

    self.logger.info("Sending GET request to person's profile page")
    try:
      linkedinconnectid.run()
    except TimeoutException as exc:
      self.logger.critical(exc)
      return

  @_check_net_stat
  @_login
  def search(self: Command) -> None:
    """Method `search()` initialises an instance of `LinkedInSearchConnect` API.

    This instance is then used to send connection request to people whose profile
    aligns to the specified criteria.

    Args:
      self: (Command) Self.

    Example:
    >>> from argparse import Namespace
    >>> from inbparser import Command
    >>>
    >>> namespace = Namespace(which='search', email='ayush854032@gmail.com'
    ...               password='xxx-xxx-xxx', keyword='Medical',
    ...               location='India', title='', first_name='Mohika', last_name='Negi',
    ...               school=None, industry='Health Economy:Medical:Health Care Industry',
    ...               current_company=None, profile_language='English', limit=1, headless=True, 
    ...               debug=False, cookies=False, start_maximized=True, incognito=True)
    >>> command = Command(namespace)
    >>> command.search()
    """
    self.logger.info("Instantiating connection object")
    linkedin_search_connect = LinkedInSearchConnect(
        self.linkedin.driver, keyword=self.keyword,
        location=self.location, title=self.title,
        first_name=self.first_name, last_name=self.last_name,
        school=self.school, industry=self.industry,
        current_company=self.current_company,
        profile_language=self.profile_language, limit=self.limit)

    self.logger.info("Sending GET request to search results page")
    linkedin_search_connect.run()

  def show(self: Command) -> None:
    """Method `show()` prints user(s) information stored in database.

    This feature is not programed yet. Contributions are welcome.

    Args:
      self: (Command) Self.

    Example:
    >>> from argparse import Namespace
    >>> from inbparser import Command
    >>> 
    >>> namespace = Namespace(which='show', keyword='email', ...)
    >>> command = Command(namespace)
    >>> command.show()
    >>> # -> It should print email(s) stored in database
    """
    self.logger.info("facility not present")

  def config(self: Command) -> None:
    """Method `config()` stores user's information in database.

    This feature is not programed yet. Contributions are welcome.

    Args:
      self: (Command) Self.

    Example:
    >>> from argparse import Namespace
    >>> from inbparser import Command
    >>> 
    >>> namespace = Namespace(which='config', EMAIL='ayush@gmail.com', PASSWORD='xxx-xxx-xxx')
    >>> command = Command(namespace)
    >>> command.config()
    >>> # -> It should update database with new values
    """
    self.logger.info("facility not present")

  def delete(self: Command) -> None:
    """Method `delete()` deletes user's information from database.

    This feature is not programed yet. Contributions are welcome.

    Args:
      self: (Command) Self.

    Example:
    >>> from argparse import Namespace
    >>> from inbparser import Command
    >>> 
    >>> namespace = Namespace(which='delete', keyword='email') # Not designed yet
    >>> command = Command(namespace)
    >>> command.delete()
    >>> # -> It should remove values from database
    """
    self.logger.info("facility not present")

  def developer(self: Command) -> None:
    """Method `developer()` prints developer's information that is stored in the
    database.

    This feature is not programed yet. Contributions are welcome.

    Args:
      self: (Command) Self.

    Example:
    >>> from argparse import Namespace
    >>> from inbparser import Command
    >>> 
    >>> namespace = Namespace(which='developer', name=True, linkedin=True, github=True)
    >>> command = Command(namespace)
    >>> command.developer()
    >>> # -> It should print developer(s) information
    """
    self.logger.info("facility not present")

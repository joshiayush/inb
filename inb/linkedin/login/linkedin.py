"""
This module provides service to communicate with LinkedIn's login form.

  :copyright: Copyright (c) 2019 Creative Commons.
  :license: MIT License, see license for details.
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

import functools

from typing import (
    Any, Dict, List
)

from .. import Driver

from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.keys import Keys

from lib import __project_name__
from errors import CredentialsNotGivenException


class LinkedIn(Driver):
  LOGIN_PAGE_URL = "https://www.linkedin.com/login"

  def __init__(self: LinkedIn, user_email: str,
               user_password: str, driver_path: str,
               opt_chromedriver_options: list = []) -> None:
    """LinkedIn class constructor to initialise LinkedIn object.

    This instance will help to log into LinkedIn account.

    Args:
      self: (LinkedIn) Self
      user_email: (str) User email.
      user_password: (str) User password.
      driver_path: (str) Chrome driver path.
      opt_chromedriver_options: (list) Chromedriver options if any (optional).

    Returns: 
      `None`

    Raises:
      CredentialsNotGivenException: If either of `user_email` or `user_password` field is
        empty.

    Example:
    >>> from lib import chromedriver_abs_path
    >>> from linkedin import Driver
    >>> from linkedin.login import LinkedIn
    >>>
    >>> chromedriver_options = [Driver.HEADLESS, Driver.INCOGNITO, ...]
    >>> linkedin = LinkedIn('ayush854032@gmail.com', 'xxx-xxx-xxx', 
    ...              chromedriver_abs_path(), chromedriver_options)
    """
    super(
        LinkedIn, self).__init__(
        driver_path=driver_path, options=opt_chromedriver_options)

    if user_email:
      self._user_email = user_email
    else:
      raise CredentialsNotGivenException(
          "'user_email' can not be empty!")
    if user_password:
      self._user_password = user_password
    else:
      raise CredentialsNotGivenException(
          "'user_password' can not be empty!")

  @classmethod
  def set_login_page_url(cls: LinkedIn, url: str) -> None:
    """Class method `set_login_page_url()` sets the value of static variable
    `LOGIN_PAGE_URL` to the given value in case the user wants to provide an
    explicit value for the url.

    Args:
      cls: (LinkedIn) Class.
      url: (str) Url.

    Example:
    >>> from linkedin.login import LinkedIn
    >>> LinkedIn.set_login_page_url('https://custom.url.com')
    """
    cls.LOGIN_PAGE_URL = url

  def _get_login_page(function_: function) -> function:
    """Decorator `get_login_page()` adds a `wrapper` around a function. This `wrapper`
    then takes you to the LinkedIn login page before executing the function given to it.

    Args:
      function_: (function) Function to decorate.

    Returns:
      `function`

    Raises:
      TimeoutException: If weak network is found.

    Example:
    >>> class LinkedIn(Driver):
    ...   @_get_login_page
    ...   def login(self: LinkedIn) -> None:
    ...     '''Method login() logs into your personal LinkedIn profile.
    ...
    ...     Args:
    ...       self: (LinkedIn) Self. 
    ...     '''
    ...     # Your login code here
    """
    @functools.wraps(function_)
    def wrapper(
            self: LinkedIn, *args: List[Any],
            **kwargs: Dict[Any, Any]):
      nonlocal function_
      try:
        self.driver.get(LinkedIn.LOGIN_PAGE_URL)
      except TimeoutException:
        raise TimeoutException(
            "ERR: Cannot log in due to weak network!")
      else:
        function_(self, *args, **kwargs)
    return wrapper

  def _enter_email(self: LinkedIn, return_: bool = False) -> None:
    """Method `_enter_email()` enters the email in the email input field.

    Args:
      self: (LinkedIn) Self.
      return_: (bool) Whether to send return key or not.

    Example:
    >>> class LinkedIn(Driver):
    ...   def foo(self: Driver) -> Any:
    ...     self._enter_email('ayush854032@gmail.com')
    """
    email_box = self.driver.find_element_by_name("session_key")
    email_box.clear()
    email_box.send_keys(self._user_email)
    if return_ == True:
      email_box.send_keys(Keys.RETURN)

  def _enter_passwd(self: LinkedIn, return_: bool = True) -> None:
    """Method `_enter_passwd()` enters the password in the password input field.

    Args:
      self: (LinkedIn) Self.
      return_: (bool) Whether to send return key or not.

    Example:
    >>> class LinkedIn(Driver):
    ...   def foo(self: Driver) -> Any:
    ...     self._enter_password('xxx-xxx-xxx')
    """
    password_box = self.driver.find_element_by_name(
        "session_password")
    password_box.clear()
    password_box.send_keys(self._user_password)
    if return_ == True:
      password_box.send_keys(Keys.RETURN)

  @_get_login_page
  def login(self: LinkedIn) -> None:
    """Method `login()` logs into your personal LinkedIn profile.

    Args:
      self: (LinkedIn) Self. 

    Example:
    >>> from lib import chromedriver_abs_path
    >>> from linkedin import Driver
    >>> from linkedin.login import LinkedIn
    >>>
    >>> chromedriver_options = [Driver.HEADLESS, Driver.INCOGNITO, ...]
    >>> linkedin = LinkedIn('ayush854032@gmail.com', 'xxx-xxx-xxx', 
    ...              chromedriver_abs_path(), chromedriver_options)
    >>> linkedin.login()
    """
    self._enter_email()
    self._enter_passwd()

  def __del__(self: LinkedIn) -> None:
    """LinkedIn class `destructor` to delete the instance.

    Args:
      self: (LinkedIn) Self.

    Example:
    >>> from lib import chromedriver_abs_path
    >>> from linkedin import Driver
    >>> from linkedin.login import LinkedIn
    >>>
    >>> chromedriver_options = [Driver.HEADLESS, Driver.INCOGNITO, ...]
    >>> linkedin = LinkedIn('ayush854032@gmail.com', 'xxx-xxx-xxx', 
    ...              chromedriver_abs_path(), chromedriver_options)
    >>> linkedin.login()
    >>> del linkedin
    """
    self.disable_webdriver_chrome()

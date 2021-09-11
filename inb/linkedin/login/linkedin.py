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

from typing import Any
from typing import Dict
from typing import List

from .. import Driver

from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.keys import Keys

from errors import CredentialsNotGivenException


class LinkedIn(Driver):
    LOGIN_PAGE_URL: str = "https://www.linkedin.com/login"

    def __init__(
        self: LinkedIn,
        user_email: str = '',
        user_password: str = '',
        driver_path: str = '',
        opt_chromedriver_options: list = []
    ) -> None:
        """LinkedIn class constructor to initialise LinkedIn object.

        :Args:
            - self: {LinkedIn} object
            - credentials: {dist} user's credentails in form of dictionary
            - driver_path: {str} chrome driver path
            - opt_chromedriver_options: {list} chromedriver options if any (optional)

        :Returns: 
            - {LinkedIn}

        :Raises:
            - KeyError if 'user_email' or 'user_password' keys are not present in the dictionary
                credentials
        """
        super(LinkedIn, self).__init__(driver_path=driver_path,
                                       options=opt_chromedriver_options)

        if not user_email:
            raise CredentialsNotGivenException(
                "ValueError: 'user_email' can not be empty!")
        self.__user_email = user_email
        if not user_password:
            raise CredentialsNotGivenException(
                "ValueError: 'user_password' can not be empty!")
        self.__user_password = user_password

    def _get_login_page(function_: function) -> function:
        """Method get_login_page() takes you to the LinkedIn login page by executing 
        function 'get()' on the webdriver object.

        :Args:
            - self: {LinkedIn} object
            - _url: {str} website url

        :Returns:
            - {None}

        :Raises:
            - DomainNameSystemNotResolveException if there's a TimeourException
        """
        @functools.wraps(function_)
        def wrapper(self: LinkedIn, *args: List[Any], **kwargs: Dict[Any, Any]):
            nonlocal function_
            try:
                self.driver.get(LinkedIn.LOGIN_PAGE_URL)
            except TimeoutException:
                raise TimeoutException(
                    "ERR: Cannot log in due to weak network!")
            else:
                function_(self, *args, **kwargs)
        return wrapper

    def __get_email_box(self: LinkedIn) -> webdriver.Chrome:
        """Method get_email_box() returns the input tag for entering email address.

        :Args:
            - self: {LinkedIn} object

        :Returns:
            - {WebElement} input tag

        :Raises:
            - NoSuchElementException if the element wasn't found
        """
        return self.driver.find_element_by_name("session_key")

    def __enter_email(self: LinkedIn, _return: bool = False) -> None:
        """Method enter_email() enters the email in the email input field.

        :Args:
            - self: {LinkedIn} object
            - hit_return: {bool} if to send return key or not

        :Returns: 
            - {None}
        """
        email_box = self.__get_email_box()
        email_box.clear()
        email_box.send_keys(self.__user_email)
        if _return == True:
            email_box.send_keys(Keys.RETURN)

    def __get_password_box(self: LinkedIn) -> webdriver.Chrome:
        """Method get_password_box() returns the input tag for entering password.

        :Args:
            - self: {LinkedIn} object

        :Returns:
            - {WebElement} input tag

        :Raises:
            - NoSuchElementException if the element wasn't found
        """
        return self.driver.find_element_by_name("session_password")

    def __enter_password(self: LinkedIn, _return: bool = True) -> None:
        """Method enter_password() enters the password in the password input field.

        :Args:
            - self: {LinkedIn} object
            - hit_return: {bool} if to send return key or not

        :Returns:
            - {None}
        """
        password_box = self.__get_password_box()
        password_box.clear()
        password_box.send_keys(self.__user_password)
        if _return == True:
            password_box.send_keys(Keys.RETURN)

    def __fill_credentials(self: LinkedIn) -> None:
        """Method fill_credentials() fills the user credentials in the specified fields.

        :Args:
            - self: {LinkedIn} object

        :Returns:
            - {None}
        """
        self.__enter_email()
        self.__enter_password()

    @_get_login_page
    def login(self: LinkedIn) -> None:
        """Method login() logs into your personal LinkedIn profile.

        :Args:
            - self: {LinkedIn} object 
            - credentials: {dict} user's credentials in the form of dictionary

        :Returns:
            - {None}
        """
        self.__fill_credentials()

    def __del__(self: LinkedIn) -> None:
        """LinkedIn class destructor to de-initialise LinkedIn object.

        :Args:
            - self: {LinkedIn} object

        :Returns:
            - {None}
        """
        self.disable_webdriver_chrome()

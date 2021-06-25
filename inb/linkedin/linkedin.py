"""from __future__ imports must occur at the beginning of the file. DO NOT CHANGE!"""
from __future__ import annotations

from typing import Any

from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.keys import Keys

from errors.error import CredentialsNotGivenException
from errors.error import WebDriverPathNotGivenException
from errors.error import DomainNameSystemNotResolveException


class LinkedIn(object):
    SESSION_ALREADY_EXISTS = False

    def __init__(self: LinkedIn, credentials: dict = {}, driver_path: str = '') -> LinkedIn:
        """LinkedIn class constructor to initialise LinkedIn object.

        :Args:
            - self: {LinkedIn} object
            - credentials: {dist} user's credentails in form of dictionary
            - driver_path: {str} chrome driver path

        :Returns: 
            - {LinkedIn}

        :Raises:
            - KeyError if 'user_email' or 'user_password' keys are not present in the dictionary
                credentials
        """
        self._credentials = {
            "user_email": '',
            "user_password": ''
        }

        if not driver_path:
            raise WebDriverPathNotGivenException(
                "User did not provide chromedriver's path!")

        self.driver_path = driver_path

        if credentials:
            if not "user_email" in credentials:
                raise KeyError(
                    "Key 'user_email' doesn't exists in dictionary 'credentials'!")

            if not "user_password" in credentials:
                raise KeyError(
                    "Key 'user_password' doesn't exists in dictionary 'credentials'!")

            self._credentials = {
                "user_email": credentials["user_email"],
                "user_password": credentials["user_password"]
            }

        self.options = webdriver.ChromeOptions()

    @property
    def user_email(self: LinkedIn) -> str:
        """Property method user_email to return user email address.

        :Args:
            - self: {LinkedIn} object

        :Returns:
            - {str} user email address

        :Raises:
            - KeyError if the key 'user_password' is not present in {dict} _credentials
        """
        return self._credentials["user_email"]

    @user_email.setter
    def user_email(self: LinkedIn, user_email: str) -> None:
        """Property method user_email to set user email address.

        :Args:
            - self: {LinkedIn} object
            - user_email: {str} user email address

        :Returns:
            - {None}

        :Raises:
            - KeyError if the key 'user_password' is not present in {dict} _credentials
        """
        self._credentials["user_email"] = user_email

    @property
    def user_password(self: LinkedIn) -> str:
        """Property method user_password to return user password.

        :Args:
            - self: LinkedIn object

        :Returns:
            - {str} user password

        :Raises:
            - KeyError if the key 'user_password' is not present in {dict} _credentials
        """
        return self._credentials["user_password"]

    @user_password.setter
    def user_password(self: LinkedIn, user_password: str) -> None:
        """Property method user_password to set user password.

        :Args:
            - self: {LinkedIn} object
            - user_email: {str} user email address

        :Returns:
            - {None}

        :Raises:
            - KeyError if the key 'user_password' is not present in {dict} _credentials
        """
        self._credentials["user_password"] = user_password

    def set_browser_incognito_mode(self: LinkedIn) -> None:
        """Method set_browser_incognito_mode() adds argument '--incognito' to chrome options to
        enable chromedriver in incognito mode to log in as a test user, with none of your admin
        history remembered.

        :Args:
            - self: {LinkedIn} object

        :Returns:
            - {None}

        :Raises:
            - ValueError if the argument is null
        """
        self.options.add_argument("--incognito")

    def set_ignore_certificate_error(self: LinkedIn) -> None:
        """Method set_ignore_certificate_error() is to disable the error windows related with 
        certificate errors. 

        :Args:
            - self: {LinkedIn} object

        :Returns:
            - {None}

        :Raises:
            - ValueError if the argument is null
        """
        self.options.add_argument("--ignore-certificate-errors")

    def set_headless(self: LinkedIn) -> None:
        """Method set_headless() is to set the chromedriver in headless mode.

        :Args:
            - self: {LinkedIn} object

        :Returns:
            - {None}

        :Raises:
            - ValueError if the argument is null
        """
        self.options.add_argument("--headless")

    def enable_automation(self: LinkedIn) -> None:
        """Method enable_automation() is to enable automation in chromedriver.

        :Args:
            - self: {LinkedIn} object

        :Returns:
            - {None}

        :Raises:
            - ValueError if the argument is null
        """
        self.options.add_argument("--enable-automation")

    def no_sandbox(self: LinkedIn) -> None:
        """Method no_sandbox() is to set the chromedriver in --no-sandbox mode.

        :Args:
            - self: {LinkedIn} object

        :Returns:
            - {None}

        :Raises:
            - ValueError if the argument is null
        """
        self.options.add_argument("--no-sandbox")

    def disable_setuid_sandbox(self: LinkedIn) -> None:
        """Method disable_setuid_sandbox() is to disable setuid sandbox.

        :Args:
            - self: {LinkedIn} object

        :Returns:
            - {None}

        :Raises:
            - ValueError if the argument is null
        """
        self.options.add_argument("--disable-setuid-sandbox")

    def disable_extensions(self: LinkedIn) -> None:
        """Method disable_extensions() is to disable chrome extensions.

        :Args:
            - self: {LinkedIn} object

        :Returns:
            - {None}

        :Raises:
            - ValueError if the argument is null
        """
        self.options.add_argument("--disable-extensions")

    def disable_info_bars(self: LinkedIn) -> None:
        """Method disable_info_bars() is to disable info bars in chromedriver.

        :Args:
            - self: {LinkedIn} object

        :Returns:
            - {None}

        :Raises:
            - ValueError if the argument is null
        """
        self.options.add_argument("--disable-infobars")

    def enable_full_screen(self: LinkedIn) -> None:
        """Method enable_full_screen() opens chromedriver in full screen.

        :Args:
            - self: {LinkedIn} object

        :Returns:
            - {None}

        :Raises:
            - ValueError if the argument is null
        """
        self.options.add_argument("--start-maximized")

    def disable_gpu(self: LinkedIn) -> None:
        """Method disable_gpu() is to disable gpu (for Windows).

        :Args:
            - self: {LinkedIn} object

        :Returns:
            - {None}

        :Raises:
            - ValueError if the argument is null
        """
        self.options.add_argument("--disable-gpu")

    def diable_notifications(self: LinkedIn) -> None:
        """Method disable_notifications() is to disable notifications.

        :Args:
            - self: {LinkedIn} object

        :Returns:
            - {None}

        :Raises:
            - ValueError if the argument is null
        """
        self.options.add_argument("--disable-notifications")

    def get_chrome_driver_options(self: LinkedIn) -> object:
        """Method get_chrome_driver_options() returns a set of chrome options to be added 
        during the execution of chromedriver. These options help in driver testing and automation.

        :Args:
            self: {LinkedIn} object

        :Returns:
            - {Options}
        """
        return self.options

    def enable_webdriver_chrome(self: LinkedIn, _options: object) -> None:
        """Method enable_web_driver() makes a webdriver object called by calling 
        'webdriver.Chrome()' constructor.

        :Args:
            - self: {LinkedIn} object
            - _options: {Options} to pass to webdriver.Chrome() constructor

        :Returns:
            - {None}

        :Reference:
            - http://peter.sh/experiments/chromium-command-line-switches/
        """
        if LinkedIn.SESSION_ALREADY_EXISTS:
            return

        LinkedIn.SESSION_ALREADY_EXISTS = True

        self.driver = webdriver.Chrome(
            self.driver_path, options=_options)

    def disable_webdriver_chrome(self: LinkedIn) -> None:
        """Method disable_webdriver_chrome() closes the webdriver session by 
        executing a function called 'close()' on webdriver object.

        :Args:
            - self: {LinkedIn} object

        :Returns:
            - {None}
        """
        self.driver.close()

    def get_login_page(self: LinkedIn, _url: str = "https://www.linkedin.com/login") -> None:
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
        try:
            self.driver.get(_url)
        except TimeoutException:
            raise DomainNameSystemNotResolveException("ERR_DNS_PROBE_STARTED")

    def get_email_box(self: LinkedIn) -> Any:
        """Method get_email_box() returns the input tag for entering email address.

        :Args:
            - self: {LinkedIn} object

        :Returns:
            - {WebElement} input tag

        :Raises:
            - NoSuchElementException if the element wasn't found

        :Usage:
            - email_box = self.get_email_box()
        """
        return self.driver.find_element_by_name("session_key")

    def enter_email(self: LinkedIn, hit_return: bool = False) -> None:
        """Method enter_email() enters the email in the email input field.

        :Args:
            - self: {LinkedIn} object
            - hit_return: {bool} if to send return key or not

        :Returns: 
            - {None}
        """
        email_box = self.get_email_box()
        email_box.clear()
        email_box.send_keys(self.user_email)

        if not hit_return:
            return

        email_box.send_keys(Keys.RETURN)

    def get_password_box(self: LinkedIn) -> Any:
        """Method get_password_box() returns the input tag for entering password.

        :Args:
            - self: {LinkedIn} object

        :Returns:
            - {WebElement} input tag

        :Raises:
            - NoSuchElementException if the element wasn't found

        :Usage:
            - password_box = self.get_password_box()
        """
        return self.driver.find_element_by_name("session_password")

    def enter_password(self: LinkedIn, hit_return: bool = True) -> None:
        """Method enter_password() enters the password in the password input field.

        :Args:
            - self: {LinkedIn} object
            - hit_return: {bool} if to send return key or not

        :Returns:
            - {None}
        """
        password_box = self.get_password_box()
        password_box.clear()
        password_box.send_keys(self.user_password)

        if not hit_return:
            return

        password_box.send_keys(Keys.RETURN)

    def fill_credentials(self: LinkedIn) -> None:
        """Method fill_credentials() fills the user credentials in the specified fields.

        :Args:
            - self: {LinkedIn} object

        :Returns:
            - {None}
        """
        self.enter_email()
        self.enter_password()

    def login(self: LinkedIn, credentials: dict = {}) -> None:
        """Method login() logs into your personal LinkedIn profile.

        :Args:
            - self: {LinkedIn} object 
            - credentials: {dict} user's credentials in the form of dictionary

        :Returns:
            - {None}
        """
        if not credentials and not self.user_email or not self.user_password:
            raise CredentialsNotGivenException(
                "User credentials are not given. Can't login!")

        if credentials:
            if not "user_email" in credentials:
                raise KeyError(
                    "Key 'user_email' doesn't exists in dictionary 'credentials'!")

            if not "user_password" in credentials:
                raise KeyError(
                    "Key 'user_password' doesn't exists in dictionary 'credentials'!")

            self._credentials = {
                "user_email": credentials["user_email"],
                "user_password": credentials["user_password"]
            }

        self.fill_credentials()

    def __del__(self: LinkedIn) -> None:
        """LinkedIn class destructor to de-initialise LinkedIn object.

        :Args:
            - self: {LinkedIn} object

        :Returns:
            - {None}
        """
        LinkedIn.SESSION_ALREADY_EXISTS = False

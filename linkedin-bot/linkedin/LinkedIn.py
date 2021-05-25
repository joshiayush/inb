"""from __future__ imports must occur at the beginning of the file. DO NOT CHANGE!"""
from __future__ import annotations

from selenium import webdriver
from errors.error import DomainNameSystemNotResolveException


class LinkedIn(object):
    """LinkedIn"""
    OLD_EMAIL = ''
    OLD_PASSWORD = ''
    SESSION_ALREADY_EXISTS = False

    def __init__(self: LinkedIn, credentials: dict = {}, driver_path: str = '') -> None:
        """Initializing the `LinkedIn` class."""
        self._credentials = {
            "user_email": '',
            "user_password": ''
        }

        from errors.error import WebDriverPathNotGivenException

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

        if not LinkedIn.OLD_EMAIL == self.user_email and not LinkedIn.OLD_PASSWORD == self.user_password:
            """Save email and password."""
            LinkedIn.OLD_EMAIL = self.user_email
            LinkedIn.OLD_PASSWORD = self.user_password

    @property
    def user_email(self: LinkedIn) -> str:
        return self._credentials["user_email"]

    @user_email.setter
    def user_email(self: LinkedIn, user_email: str) -> None:
        self._credentials["user_email"] = user_email

    @property
    def user_password(self: LinkedIn) -> str:
        return self._credentials["user_password"]

    @user_password.setter
    def user_password(self: LinkedIn, user_password: str) -> None:
        self._credentials["user_password"] = user_password

    def set_browser_incognito_mode(self: LinkedIn) -> None:
        """Setting the browser to incognito using a command line flag 
        `--incognito`. This is because using a incognito window makes 
        it possible to log in as a 'test' user, with none of your admin 
        history remembered on the browser and we want that. To know more 
        about chrome options go and visit the site,

        http://peter.sh/experiments/chromium-command-line-switches/
        """
        self.options.add_argument("--incognito")

    def set_ignore_certificate_error(self: LinkedIn) -> None:
        """To disable the error windows related with certificate errors 
        we are using a command line flag `--ignore-certificate-errors`. 
        If you are willing to know more about chrome options,

        http://peter.sh/experiments/chromium-command-line-switches/ 

        go and visit the site.
        """
        self.options.add_argument("--ignore-certificate-errors")

    def set_headless(self: LinkedIn) -> None:
        self.options.add_argument("headless")

    def get_chrome_driver_options(self: LinkedIn) -> object:
        """Function get_chrome_driver_options() returns a set of chrome 
        options to be added during the execution of chromedriver. These 
        options help in driver testing and automation.

        Args:
            self: is the object from which the options are to be updated
        """
        return self.options

    def enable_webdriver_chrome(self: LinkedIn, _options: object) -> None:
        """Function enable_web_driver() makes a webdriver object called 
        `self.driver` by executing the `webdriver.Chrome()` constructor 
        which takes following arguments.

        Args:
            executable_path: chromedriver absolute executable path
            options: chromedriver options

        If you want to know what chromedriver options are go check out 
        the following link,

        http://peter.sh/experiments/chromium-command-line-switches/
        """
        if LinkedIn.SESSION_ALREADY_EXISTS:
            return

        LinkedIn.SESSION_ALREADY_EXISTS = True

        self.driver = webdriver.Chrome(
            self.driver_path, options=_options)

    def disable_webdriver_chrome(self: LinkedIn) -> None:
        """Function `disable_webdriver_chrome()` close the webdriver session 
        by executing a function called `close()`.
        """
        self.driver.close()

    def get_login_page(self: LinkedIn, _url: str = "https://www.linkedin.com/login") -> None:
        """Redirecting to the LinkedIn login page using `get()` function of 
        our `webdriver` class.

        Args:
            url: page's url
        """
        from selenium.common.exceptions import TimeoutException

        try:
            self.driver.get(_url)
        except TimeoutException:
            raise DomainNameSystemNotResolveException("ERR_DNS_PROBE_STARTED")

    def get_email_box(self: LinkedIn):
        return self.driver.find_element_by_name("session_key")

    def enter_email(self: LinkedIn, hit_return: bool = False) -> None:
        """Function `enter_email()` enters the email in the email input 
        field using function `find_element_by_name()` which first finds 
        the email element by name `session_key` and then clears the field 
        using function `clear()` which is needed to clear previously input 
        value or to clear the buffer and then it sends the email address 
        using function `send_keys()`.

        find_element_by_name():
            Args:
                name: the name of the element to find.
        send_keys():
            Args:
                *value: A string for typing, or setting form fields. 
                For setting file input, this could be a local file path.
        """
        email_box = self.get_email_box()
        email_box.clear()
        email_box.send_keys(self.user_email)

        if not hit_return:
            return

        from selenium.webdriver.common.keys import Keys

        email_box.send_keys(Keys.RETURN)

    def get_password_box(self: LinkedIn):
        return self.driver.find_element_by_name("session_password")

    def enter_password(self: LinkedIn, hit_return: bool = True) -> None:
        """Function `enter_password()` enters the password in the 
        password input field using function `find_element_by_name()` 
        which first finds the password element by name 
        `session_password` and then clears the field using function 
        `clear()` which is needed to clear previously input value or 
        to clear the buffer and then it sends the password using 
        function `send_keys()`.

        find_element_by_name():
            Args:
                name: the name of the element to find.
        send_keys():
            Args:
                *value: A string for typing, or setting form fields. 
                For setting file input, this could be a local file path.

        This function unlike the `enter_email()` also sends the field
        object a `ENTER` event so to start the login process.
        """
        password_box = self.get_password_box()
        password_box.clear()
        password_box.send_keys(self.user_password)

        if not hit_return:
            return

        from selenium.webdriver.common.keys import Keys

        password_box.send_keys(Keys.RETURN)

    def fill_credentials(self: LinkedIn) -> None:
        """Function `fill_credentials()` fills the user credentials in 
        the desired fields by invoking function, `enter_email()` which 
        enters the email in the desired field and function `enter_password()` 
        which enters the password in the desired field.

        Args:
            self: object used to invoke the functions `enter_email()` and 
            `enter_password()`.
        """
        self.enter_email()
        self.enter_password()

    def login(self: LinkedIn, credentials: dict = {}) -> None:
        """Function `login()` logs into your personal LinkedIn profile.

        Args:
            self: object used to execute various functions in our 
            LinkedIn class.
        """
        from errors.error import CredentialsNotGivenException

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

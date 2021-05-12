#
# file src/Linkedin.py provides the driver access to other python files, here
# in this file I've added all the basic funcitionality required to login to
# linkedin before actually starting to automate the inner Linkedin.
#
# If you want to get in touch wtih me this is my email address
#
#                 ayush854032@gmail.com
#
#                         and
#
#             joshiayush.joshiayush@gmail.com
#
# and here is a link to my LinkedIn account you can connect to me here,
#
# https://www.linkedin.com/in/ayush-joshi-3600a01b7
#

from selenium import webdriver

from errors.error import DomainNameSystemNotResolveException


class LinkedIn(object):
    """LinkedIn"""
    OLD_EMAIL = ""
    OLD_PASSWORD = ""

    SESSION_ALREADY_EXISTS = False

    def __init__(self: object, data: dict) -> None:
        """Initializing the `LinkedIn` class."""
        self.data = data
        self.email = self.data["user_email"]
        self.password = self.data["user_password"]

        if not LinkedIn.SESSION_ALREADY_EXISTS:
            """Making an option object for our chromedriver."""
            self.options = webdriver.ChromeOptions()

            """Turning webdriver on."""
            self.enable_webdriver_chrome()

            LinkedIn.SESSION_ALREADY_EXISTS = True

        if LinkedIn.OLD_EMAIL != self.email and LinkedIn.OLD_PASSWORD != self.password:
            """Save email and password."""
            LinkedIn.OLD_EMAIL = self.email
            LinkedIn.OLD_PASSWORD = self.password

            """Calling `login()` function which will login for us."""
            self.login()

    def set_browser_incognito_mode(self: object) -> None:
        """Setting the browser to incognito using a command line flag 
        `--incognito`. This is because using a incognito window makes 
        it possible to log in as a 'test' user, with none of your admin 
        history remembered on the browser and we want that. To know more 
        about chrome options go and visit the site,

        http://peter.sh/experiments/chromium-command-line-switches/
        """
        self.options.add_argument("--incognito")

    def set_ignore_certificate_error(self: object) -> None:
        """To disable the error windows related with certificate errors 
        we are using a command line flag `--ignore-certificate-errors`. 
        If you are willing to know more about chrome options,

        http://peter.sh/experiments/chromium-command-line-switches/ 

        go and visit the site.
        """
        self.options.add_argument("--ignore-certificate-errors")

    def set_headless(self: object) -> None:
        self.options.add_argument("headless")

    def get_chrome_driver_options(self: object) -> "Webdriver Options":
        """Function get_chrome_driver_options() returns a set of chrome 
        options to be added during the execution of chromedriver. These 
        options help in driver testing and automation.

        Args:
            self: is the object from which the options are to be updated
        """
        self.set_browser_incognito_mode()
        self.set_ignore_certificate_error()

        self.set_headless() if self.data["headless"] else False

        return self.options

    def enable_webdriver_chrome(self: object) -> None:
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
        self.driver = webdriver.Chrome(
            self.data["driver_path"], options=self.get_chrome_driver_options())

    def disable_webdriver_chrome(self: object) -> None:
        """Function `disable_webdriver_chrome()` close the webdriver session 
        by executing a function called `close()`.
        """
        self.driver.close()

    def get_login_page(self: object) -> None:
        """Redirecting to the LinkedIn login page using `get()` function of 
        our `webdriver` class.

        Args:
            url: page's url
        """
        from selenium.common.exceptions import TimeoutException

        try:
            self.driver.get("https://www.linkedin.com/login")
        except TimeoutException:
            raise DomainNameSystemNotResolveException("ERR_DNS_PROBE_STARTED")

    def enter_email(self: object) -> None:
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
        login_email = self.driver.find_element_by_name("session_key")

        login_email.clear()
        login_email.send_keys(self.email)

    def enter_password(self: object) -> None:
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
        login_password = self.driver.find_element_by_name("session_password")

        login_password.clear()
        login_password.send_keys(self.password)

        from selenium.webdriver.common.keys import Keys

        login_password.send_keys(Keys.RETURN)

    def fill_credentials(self: object) -> None:
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

    def login(self: object) -> None:
        """Function `login()` logs into your personal LinkedIn profile.

        Args:
            self: object used to execute various functions in our 
            LinkedIn class.
        """
        from messages.console_messages import send_to_console

        send_to_console(f"""Connecting...""", color='b', pad='8', end='\r')

        try:
            self.get_login_page()
        except DomainNameSystemNotResolveException as error:
            send_to_console(f"""{error}""", color='r', style='b', pad='1')

        self.fill_credentials()

        send_to_console(' ', pad='80', end='\r')
        send_to_console(f"""Connected ✔""", color='g', style='b', pad='8')

    @property
    def get_job_keywords(self: object) -> str:
        """Function `get_job_keywords()` returns the job keywords."""
        return self.data["job_keywords"]

    @get_job_keywords.setter
    def set_job_keywords(self: object, _keyword: str):
        self.data["job_keywords"] = _keyword

    @property
    def get_job_location(self: object) -> str:
        """Function `get_job_location()` returns the job location."""
        return self.data["job_location"]

    @get_job_location.setter
    def set_job_location(self: object, _location: str):
        self.data["job_location"] = _location

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

import re
import sys
import time
import colorama

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support import expected_conditions
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import ElementNotInteractableException
from selenium.common.exceptions import ElementClickInterceptedException


class LinkedIn(object):
    SUCCESS_RATE = 0
    FAILURE_RATE = 0

    def __init__(self, data):
        """Initializing the `LinkedIn` class."""
        self.data = data
        self.email = self.data["user_email"]
        self.password = self.data["user_password"]

        """Making an option object for our chromedriver."""
        self.options = webdriver.ChromeOptions()

        """Turning webdriver on."""
        self.enable_webdriver_chrome()

        """Calling `login()` function which will login for us."""
        self.login()

    def set_browser_incognito_mode(self):
        """Setting the browser to incognito using a command line flag 
        `--incognito`. This is because using a incognito window makes 
        it possible to log in as a 'test' user, with none of your admin 
        history remembered on the browser and we want that. To know more 
        about chrome options go and visit the site,

        http://peter.sh/experiments/chromium-command-line-switches/
        """
        self.options.add_argument("--incognito")

    def set_ignore_certificate_error(self):
        """To disable the error windows related with certificate errors 
        we are using a command line flag `--ignore-certificate-errors`. 
        If you are willing to know more about chrome options,

        http://peter.sh/experiments/chromium-command-line-switches/ 

        go and visit the site.
        """
        self.options.add_argument("--ignore-certificate-errors")

    def set_headless(self):
        self.options.add_argument("headless")

    def get_chrome_driver_options(self):
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

    def enable_webdriver_chrome(self):
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

    def disable_webdriver_chrome(self):
        """Function `disable_webdriver_chrome()` close the webdriver session 
        by executing a function called `close()`.
        """
        self.driver.close()

    def get_login_page(self):
        """Redirecting to the LinkedIn login page using `get()` function of 
        our `webdriver` class.

        Args:
            url: page's url
        """
        self.driver.get("https://www.linkedin.com/login")

    def enter_email(self):
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

    def enter_password(self):
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

        login_password.send_keys(Keys.RETURN)

    def fill_credentials(self):
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

    def login(self):
        """Function `login()` logs into your personal LinkedIn profile.

        Args:
            self: object used to execute various functions in our 
            LinkedIn class.
        """
        self.get_login_page()

        self.fill_credentials()

    def get_job_keywords(self):
        """Function `get_job_keywords()` returns the job keywords."""
        return self.data["job_keywords"]

    def get_job_location(self):
        """Function `get_job_location()` returns the job location."""
        return self.data["job_location"]

    @staticmethod
    def get_page_y_offset(self):
        """Function get_page_y_offset() returns the window.pageYOffset 
        of the webpage, we need that so we can keep on scrolling untill 
        the page offset becomes constant. Declaration of this method is 
        static because we want to use this function across multiple 
        classes.

        Args:
            self: is not a object here but it is a parameter object 
            that has a property 'driver' and we need that

        return:
            window.pageYOffset
        """
        return self.driver.execute_script((
            "return (window.pageYOffset !== undefined)"
            "       ? window.pageYOffset"
            "       : (document.documentElement || document.body.parentNode || document.body);"
        ))

    @staticmethod
    def execute_javascript(self):
        """Function execute_javascript() scrolls the web page to the 
        very bottom of it using the 'document.scrollingElement.scrollTop' 
        property.

        Args:
            self: it is a parameter object that has a property 'driver' 
            in it and we need that to access the webpage.
        """
        self.driver.execute_script((
            "var scrollingElement = (document.scrollingElement || document.body);"
            "scrollingElement.scrollTop = scrollingElement.scrollHeight;"
        ))

    @staticmethod
    def inform_user(button, _type):
        """Function inform_user() retrieves the value of attribute 
        'aria-label' using the webdriver function 'get_attribute()' 
        which returns the value given to that attribute and then using
        that attribute we inform user that what is the status for the
        target.

        Args:
            button: button element in which the program has to click
            _type: is the status is it sending or failed
        """
        if (_type == "sending"):
            print(f"""{colorama.Style.BRIGHT}""", end="")
            print(f"""{colorama.Fore.BLUE}""", end="")

            print(
                f""" {button.get_attribute("aria-label").strip()} ({ _type.strip()}...)""", end="\r")
            time.sleep(0.5)
            print(f""" """*80, end="\r")

            print(f"""{colorama.Fore.RESET}""", end="")
            print(f"""{colorama.Style.RESET_ALL}""", end="")
        elif (_type == "sent"):
            print(f"""{colorama.Style.BRIGHT}""", end="")
            print(f"""{colorama.Fore.GREEN}""", end="")

            print(
                f""" {button.get_attribute("aria-label").strip()} ({_type.strip()} o)""", end="\r")
            time.sleep(0.5)
            print(f""" """*80, end="\r")

            print(f"""{colorama.Fore.RESET}""", end="")
            print(f"""{colorama.Style.RESET_ALL}""", end="")
        elif (_type == "failed"):
            print(f"""{colorama.Style.BRIGHT}""", end="")
            print(f"""{colorama.Fore.RED}""", end="")

            print(
                f""" {button.get_attribute("aria-label").strip()} ({_type.strip()} X)""", end="\n")

            print(f"""{colorama.Fore.RESET}""", end="")
            print(f"""{colorama.Style.RESET_ALL}""", end="")

    @staticmethod
    def print_status(obj=None, status=None, success=0, failed=0, elapsed_time=0):
        _stat = ''
        name = obj[0]
        occupation = obj[1]

        if len(occupation) >= 50:
            occupation = occupation[0:50] + "..."

        if LinkedIn.SUCCESS_RATE != 0 or LinkedIn.FAILURE_RATE != 0:
            sys.stdout.write("\033[F\033[F\033[F\033[F\033[F\033[F")

        if status == "sent":
            """_stat = ✔"""
            _stat = u"\u2714"
            _stat = f"""{colorama.Fore.GREEN}""" + \
                _stat + f"""{colorama.Fore.RESET}"""
            LinkedIn.SUCCESS_RATE += 1
        elif status == "failed":
            """_stat = ✘"""
            _stat = u"\u2718"
            _stat = f"""{colorama.Fore.RED}""" + \
                _stat + f"""{colorama.Fore.RESET}"""
            LinkedIn.FAILURE_RATE += 1

        print()
        print(
            f"""\t{_stat} {colorama.Style.BRIGHT}{name}{colorama.Style.RESET_ALL}""")
        print(
            f"""\t  {colorama.Style.DIM}{occupation}{colorama.Style.RESET_ALL}""")
        print()
        print(f"""\tSuccess: {colorama.Fore.GREEN}{LinkedIn.SUCCESS_RATE}{colorama.Fore.RESET}""",
              f"""  Failed: {colorama.Fore.RED}{LinkedIn.FAILURE_RATE}{colorama.Fore.RESET}""",
              f"""  Elapsed: {colorama.Fore.BLUE}{elapsed_time}{colorama.Fore.RESET}""")
        print()
        time.sleep(0.18)

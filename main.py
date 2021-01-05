# importing `webdriver` from `selenium`
from selenium import webdriver
# importing `Keys` from `common.keys`
from selenium.webdriver.common.keys import Keys
# importing `expected_conditions` from `support`
from selenium.webdriver.support import expected_conditions
# importing `WebDriverWait` from `support.ui`
from selenium.webdriver.support.ui import WebDriverWait
# importing `By` from `common.by`
from selenium.webdriver.common.by import By
# importing `NoSuchElementException` and `ElementClickInterceptedException` from `exceptions`
from selenium.common.exceptions import (
    NoSuchElementException,
    ElementClickInterceptedException
)
# importing `ActionChains` from `action_chains`
from selenium.webdriver.common.action_chains import ActionChains
# importing `json`
import json
# importing `regex`
import re


class LinkedIn:
    """
    Controls LinkedIn in various ways, finding for jobs is one of them,

    more functionality will be coded soon.
    """

    def __init__(self, data):
        """
        Parameter Initialization.

        Args:
            data: is the data including credentials, job search keywords

            and job location.

        Initializing, User Email, User Password, Job Keywords and Job location.
        """
        self.email = data["email"]

        self.password = data["password"]

        self.keywords = data["keywords"]

        self.location = data["location"]

        """
        Making an option object for our chromedriver
        """
        self.options = webdriver.ChromeOptions()

        """
        Turning webdriver on
        """
        self.enable_webdriver_chrome()

        """
        Calling `login()` function which will login for us
        """
        self.login()

    def enable_webdriver_chrome(self):
        """
        Function enable_web_driver() makes a webdriver object called

        `self.driver` by executing the `webdriver.Chrome()` constructor

        which takes following arguments.

        Args:
            executable_path: chromedriver absolute executable path
            options: chromedriver options

        If you want to know what chromedriver options are go check out the

        following link,

        http://peter.sh/experiments/chromium-command-line-switches/
        """
        self.driver = webdriver.Chrome(
            data["driver_path"], options=self.get_chrome_driver_options())

    def set_browser_incognito_mode(self):
        """
        Setting the browser to incognito using a command line

        flag `--incognito`. This is because using a incognito window

        makes it possible to log in as a 'test' user, with none of your

        admin history remembered on the browser and we want that.

        To know more about chrome options go and visit the site,

        http://peter.sh/experiments/chromium-command-line-switches/
        """
        self.options.add_argument("--incognito")

    def set_ignore_certificate_error(self):
        """
        To disable the error windows related with certificate errors

        we are using a command line flag `--ignore-certificate-errors`.

        If you are willing to know more about chrome options,

        http://peter.sh/experiments/chromium-command-line-switches/

        go and visit the site.
        """
        self.options.add_argument("--ignore-certificate-errors")

    def get_chrome_driver_options(self):
        """
        Function get_chrome_driver_options() returns a set of chrome options

        to be added during the execution of chromedriver. These options help

        in driver testing and automation.

        Args:
            self: is the object from which the options are to be updated
        """
        self.set_browser_incognito_mode()

        self.set_ignore_certificate_error()

        return self.options

    def get_login_page(self):
        """
        Redirecting to the LinkedIn login page using `get()` function

        of our `webdriver` class

        Args:
            url: page's url
        """
        self.driver.get("https://www.linkedin.com/login")

    def enter_email(self):
        """
        Function `enter_email()` enters the email in the email input field

        using function `find_element_by_name()` which first finds the email

        element by name `session_key` and then clears the field using function

        `clear()` which is needed to clear previously input value or to clear the

        buffer and then it sends the email address using function `send_keys()`.

        find_element_by_name():
            Args:
                name: the name of the element to find.
        send_keys():
            Args:
                *value: A string for typing, or setting form fields. For
                setting file input, this could be a local file path.
        """
        login_email = self.driver.find_element_by_name("session_key")

        login_email.clear()

        login_email.send_keys(self.email)

    def enter_password(self):
        """
        Function `enter_password()` enters the password in the password input field

        using function `find_element_by_name()` which first finds the password

        element by name `session_password` and then clears the field using function

        `clear()` which is needed to clear previously input value or to clear the

        buffer and then it sends the password using function `send_keys()`.

        find_element_by_name():
            Args:
                name: the name of the element to find.
        send_keys():
            Args:
                *value: A string for typing, or setting form fields. For
                setting file input, this could be a local file path.

        This function unlike the `enter_email()` also sends the field object

        a `ENTER` event so to start the login process.
        """
        login_password = self.driver.find_element_by_name("session_password")

        login_password.clear()

        login_password.send_keys(self.password)

        login_password.send_keys(Keys.RETURN)

    def fill_credentials(self):
        """
        Function `fill_credentials()` fills the user credentials in the

        desired fields by invoking function, `enter_email()` which enters the email

        in the desired field and function `enter_password()` which enters the

        password in the desired field.

        Args:
            self: object used to invoke the functions `enter_email()` and `enter_password()`
        """
        self.enter_email()

        self.enter_password()

    def click_on_job_box(self):
        """
        Function `click_on_job_box()` clicks on the job box as soon the page

        is loaded. This happens with the help of function `click()` which performs

        a click on the given object and to find the object we use the function

        `find_element_by_link_text()` that finds the job box element and then returns

        it.

        find_element_by_link_text():
            Args:
                link_text: the text of the element to be found
        """
        jobs_link = self.driver.find_element_by_link_text("Jobs")

        jobs_link.click()

    def enter_job_keyword(self):
        """
        Function `enter_job_keyword()` enters the given job keyword in the desired

        field, it first gets the field element using the function `find_element_by_css_selector()`

        and then stores it in the `search_keywords` object then executes a `clear()` function on

        that element so to clear the previously input value or the buffer and then sends the

        job keywords to the input field using the function `send_keys()` but before that it waits

        for the element to arrive using `WebDriverWait()` class constructor and applying a `until()`

        function on the returned object.

        find_element_by_css_selector():
            Args:
                css_selector: CSS selector string, ex: `a.#navhome`
        send_keys():
            Args:
                *value: A string for typing, or setting form fields. For
                setting file input, this could be a local file path.
        """
        try:
            search_keywords = WebDriverWait(self.driver, 5).until(
                expected_conditions.presence_of_element_located((
                    By.CSS_SELECTOR, ".jobs-search-box__text-input[aria-label='Search jobs']"
                ))
            )

            search_keywords.clear()

            search_keywords.send_keys(self.keywords)

        except NoSuchElementException as error:
            print("There is a problem finding the element.")

            print("Error: ", error)

    def enter_job_location(self):
        """
        Function `enter_job_location()` enters the given job location in the desired

        field, it first gets the field element using the function `find_element_by_css_selector()`

        and then stores it in the `search_location` object then executes a `clear()` function on

        that element so to clear the previously input value or the buffer and then sends the

        job location to the input field using the function `send_keys()` but before that it waits

        for the element to arrive using `WebDriverWait()` class constructor and applying a `until()`

        function on the returned object.

        find_element_by_css_selector():
            Args:
                css_selector: CSS selector string, ex: `a.#navhome`
        send_keys():
            Args:
                *value: A string for typing, or setting form fields. For
                setting file input, this could be a local file path.

        This function unlike `enter_job_keyword()` also sends the field object

        a `ENTER` event so to start searching for available jobs.
        """
        try:
            search_location = WebDriverWait(self.driver, 5).until(
                expected_conditions.presence_of_element_located((
                    By.CSS_SELECTOR, ".jobs-search-box__text-input[aria-label='Search location']"))
            )

            search_location.clear()

            search_location.send_keys(self.location)

            search_location.send_keys(Keys.RETURN)

        except NoSuchElementException as error:
            print("There is a problem finding the element.")

            print("Error: ", error)

    def apply_filter(self):
        pass

    def find_jobs(self):
        """
        Function `find_jobs()` searches for available jobs using functions

        `enter_job_keyword()` which enters the given keywords in the input field

        and function `enter_job_location()` which enters the given job loation in the

        input field.

        Args:
            self: object that is used to call the following functions
        """
        self.click_on_job_box()

        self.enter_job_keyword()

        self.enter_job_location()

        self.apply_filter()

    def login(self):
        """
        Function `login()` logs into your personal LinkedIn profile

        Args:
            self: object used to execute various functions in our LinkedIn class
        """
        self.get_login_page()

        self.fill_credentials()

        self.find_jobs()


if __name__ == "__main__":
    """
    Opening config.json file as `config` object
    """
    with open("/Python/LinkedIn Automater/config.json") as config:
        """
        Loading data in `data` object
        """
        data = json.load(config)

    """
    Executing LinkedIn constructor
    """
    LinkedIn(data=data)

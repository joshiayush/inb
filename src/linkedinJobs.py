"""
From `linkedin` importing `LinkedIn` class, `webdriver`, `Keys`,

`WebdriverWait`, `expected_conditions`, `By`, `NoSuchElementException`,

`ElementClickInterceptedException`, `ActionChains`, `json`, and `re`
"""
from linkedin import (
    LinkedIn,
    webdriver,
    Keys,
    WebDriverWait,
    expected_conditions,
    By,
    NoSuchElementException,
    ElementClickInterceptedException,
    ActionChains,
    json,
    re
)


class LinkedInJobs(LinkedIn):
    """
    Controls LinkedIn Jobs, more functionality will be coded soon.

    Parent:
        LinkedIn: our main LinkedIn class which takes care of enabling of 
        the webdriver and the login process.
    """

    def __init__(self):
        """
        Parameter Initialization.

        Args:
            data: is the data including credentials, job search keywords

            and job location.

        Initializing, User Email, User Password, Job Keywords and Job location.
        """
        super(LinkedInJobs, self).__init__()

        self.keywords = super(LinkedInJobs, self).get_job_keywords()

        self.location = super(LinkedInJobs, self).get_job_location()

        self.find_jobs()

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

        field, it first gets the field element using the function 

        `find_element_by_css_selector()` and then stores it in the `search_keywords` 

        object then executes a `clear()` function on that element so to clear the 

        previously input value or the buffer and then sends the job keywords to the 

        input field using the function `send_keys()` but before that it waits

        for the element to arrive using `WebDriverWait()` class constructor and 

        applying a `until()` function on the returned object.

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

        field, it first gets the field element using the function 

        `find_element_by_css_selector()` and then stores it in the `search_location` 

        object then executes a `clear()` function on that element so to clear the previously 

        input value or the buffer and then sends the job location to the input field using 

        the function `send_keys()` but before that it waits for the element to arrive using 

        `WebDriverWait()` class constructor and applying a `until()` function on the returned 

        object.

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
                    By.CSS_SELECTOR, ".jobs-search-box__text-input[aria-label='Search location']"
                ))
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


if __name__ == "__main__":
    """
    Executing LinkedIn constructor
    """
    LinkedInJobs()

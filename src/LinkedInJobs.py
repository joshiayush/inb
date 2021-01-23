from LinkedIn import (
    LinkedIn,  # importing `LinkedIn`
    webdriver,  # importing `webdriver`
    Keys,  # importing `keys`
    WebDriverWait,  # importing `WebDriverWait`
    expected_conditions,  # importing `expected_conditions`
    By,  # importing `By`
    NoSuchElementException,  # importing `NoSuchElementException`
    ElementClickInterceptedException,  # importing `ElementClickInterceptedException`
    ActionChains,  # importing `ActionChains`
    re  # importing `regex` (re)
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

        self.run()

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
        try:
            jobs_link = WebDriverWait(self.driver, 5).until(
                expected_conditions.presence_of_element_located(
                    (By.LINK_TEXT, "Jobs")
                )
            )
            jobs_link.click()

        except (
            NoSuchElementException,
            ElementClickInterceptedException,
        ) as error:
            print("There is a problem finding Job box.")
            print("Error: ", error)

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

        presence_of_element_located(): <- Class
            Args:
                locator: CSS selector string, ex: `a.#navhome`
        send_keys():
            Args:
                *value: A string for typing, or setting form fields. For
                setting file input, this could be a local file path.
        """
        try:
            search_keywords = WebDriverWait(self.driver, 5).until(
                expected_conditions.presence_of_element_located(
                    (By.CSS_SELECTOR,
                     "div.relative input[aria-label='Search by title, skill, or company']")
                )
            )
            search_keywords.clear()
            search_keywords.send_keys(self.keywords)

        except (
            NoSuchElementException,
            ElementClickInterceptedException,
        ) as error:
            print("There is a problem finding Job keyword box.")
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

        presence_Of_element_located(): <- Class
            Args:
                locator: CSS selector string, ex: `a.#navhome`
        send_keys():
            Args:
                *value: A string for typing, or setting form fields. For
                setting file input, this could be a local file path.

        This function unlike `enter_job_keyword()` also sends the field object

        a `ENTER` event so to start searching for available jobs.
        """
        try:
            search_location = WebDriverWait(self.driver, 5).until(
                expected_conditions.presence_of_element_located(
                    (By.CSS_SELECTOR,
                     "div.relative input[aria-label='City, state, or zip code']")
                )
            )
            search_location.clear()
            search_location.send_keys(self.location)
            search_location.send_keys(Keys.RETURN)

        except (
            NoSuchElementException,
            ElementClickInterceptedException,
        ) as error:
            print("There is a problem finding Job location box.")
            print("Error: ", error)

    def click_filter_button(self):
        """
        Function `click_filter_button()` clicks on the filter button which is

        on the linkedin page. It does so by using a constructor function of

        class `WebDriverWait()` which waits until the element arrives, the waiting

        process happens for one second if the element does not come then the `except`

        clause comes in play. If the element arrives before the dead line, it returns

        the element and stores in a object called `all_filters_button` then applies

        a `click()` function on it.
        """
        try:
            all_filters_button = WebDriverWait(self.driver, 1).until(
                expected_conditions.presence_of_element_located(
                    (By.XPATH, "//button[@data-control-name='all_filters']")
                )
            )
            all_filters_button.click()

        except (
            NoSuchElementException,
            ElementClickInterceptedException,
        ) as error:
            print("There is a problem finding filter button.")
            print("Error: ", error)

    def click_easy_apply(self):
        """
        Function `click_easy_apply()` clicks on the `easy apply` checkbox which is

        on the linkedin's filter page. It does so by using a constructor function of 

        class `WebDriverWait()` which waits until the element (checkbox or the filters page)

        arrives, the waiting  process happens for one second if the element does not

        come then the `except` clause comes in play. If the element arrives before

        the dead line, it returns the element and stores in a object called 

        `easy_apply_button` then applies a `click()` function on it.
        """
        try:
            easy_apply_button = WebDriverWait(self.driver, 5).until(
                expected_conditions.element_to_be_clickable(
                    (By.XPATH, "//label[@for='f_LF-f_AL']")
                )
            )
            easy_apply_button.click()

        except (
            NoSuchElementException,
            ElementClickInterceptedException,
        ) as error:
            print("There is a problem finding easy apply button.")
            print("Error: ", error)

    def click_apply_button(self):
        """
        Function `click_apply_button()` clicks on the apply button which is

        on the linkedin's filter page. It does so by using a constructor function of 

        class `WebDriverWait()` which waits until the element (apply button) arrives, 

        the waiting process happens for one second if the element does not come then 

        the `except` clause comes in play. If the element arrives before the dead line, 

        it returns the element and stores in a object called `apply_filter_button` 

        then applies a `click()` function on it.
        """
        try:
            apply_filter_button = WebDriverWait(self.driver, 5).until(
                expected_conditions.element_to_be_clickable(
                    (By.XPATH,
                     "//button[@data-control-name='all_filters_apply']")
                )
            )
            apply_filter_button.click()

        except (
            NoSuchElementException,
            ElementClickInterceptedException,
        ) as error:
            print("There is a problem finding apply button.")
            print("Error: ", error)

    def apply_filter(self):
        """
        Function `apply_filter()` starts applying filters for the job,

        for now it only applies a filter called `easy apply linkedin`, more 

        functionality for this function will be coded soon.

        This function first clicks the filter button then applies a filter

        and then clicks on apply button.

        Args:
            self: object used to call the following functions. 
        """
        self.click_filter_button()

        self.click_easy_apply()

        self.click_apply_button()

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

    def run(self):
        """
        Function run() is the main function from where the 

        bot starts searching for the jobs by executing the

        function called find_jobs()
        """
        self.find_jobs()


if __name__ == "__main__":
    """
    Executing LinkedIn constructor
    """
    LinkedInJobs()

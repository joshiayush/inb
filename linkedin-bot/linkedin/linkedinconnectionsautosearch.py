from .linkedin import By
from .linkedin import Keys
from .linkedin import LinkedIn
from .linkedin import WebDriverWait
from .linkedin import TimeoutException
from .linkedin import expected_conditions
from .linkedin import ElementNotInteractableException
from .linkedin import ElementClickInterceptedException


class LinkedInConnectionsAutoSearch(LinkedIn):
    def __init__(self, data):
        super(LinkedInConnectionsAutoSearch, self).__init__(data)

    def send_input_keywords(self):
        self.driver.find_element_by_css_selector(
            "input[aria-label='Search']").send_keys(self.data["search_keywords"], Keys.ENTER)

    def select_category_people(self):
        try:
            WebDriverWait(self.driver, 10).until(
                expected_conditions.presence_of_element_located(
                    (By.CSS_SELECTOR, "button[aria-label^='People']")
                )
            )
            self.driver.find_element_by_css_selector(
                "button[aria-label^='People']").click()
        except TimeoutException:
            pass

    def apply_search_location(self):
        pass

    def get_entity_results(self):
        try:
            WebDriverWait(self.driver, 10).until(
                expected_conditions.presence_of_element_located(
                    (By.CSS_SELECTOR, "div[class^='entity-result__actions']")
                )
            )
            return self.driver.find_elements_by_css_selector("div[class^='entity-result__actions']")
        except TimeoutException:
            pass

    def start_connecting(self):
        while_element_not_interactable = False

        for result in self.get_entity_results():
            try:
                result.find_element_by_tag_name("button").click()
                try:
                    WebDriverWait(self.driver, 10).until(
                        expected_conditions.presence_of_element_located(
                            (By.CSS_SELECTOR, "button[aria-label^='Send now']")
                        )
                    )
                    self.driver.find_element_by_css_selector(
                        "button[aria-label^='Send now']").click()
                except ElementClickInterceptedException:
                    pass
            except ElementNotInteractableException:
                while_element_not_interactable = True

        if while_element_not_interactable == False:
            self.driver.find_element_by_css_selector(
                "button[aria-label^='Next']").click()

            self.start_connecting()

    def run(self):
        self.send_input_keywords()

        self.select_category_people()

        if self.data["search_location"]:
            pass

        self.start_connecting()

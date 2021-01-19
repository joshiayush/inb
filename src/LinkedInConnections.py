"""
From `linkedin` importing `LinkedIn` class, `webdriver`, `Keys`,

`WebdriverWait`, `expected_conditions`, `By`, `NoSuchElementException`,

`ElementClickInterceptedException`, `ActionChains`, `json`, and `re`
"""
from LinkedIn import (
    LinkedIn,
    webdriver,
    Keys,
    WebDriverWait,
    expected_conditions,
    By,
    NoSuchElementException,
    ElementClickInterceptedException,
    ActionChains,
    re,
)
from selenium.common.exceptions import (
    TimeoutException,
    ElementClickInterceptedException
)
import time


class LinkedInConnections(LinkedIn):
    """
    Controls LinkedIn Connections, more functionality will be coded soon.

    Parent:
        LinkedIn: our main LinkedIn class which takes care of enabling of
        the webdriver and the login process.
    """

    def __init__(self):
        super(LinkedInConnections, self).__init__()

        self.run()

    def get_aria_label(self, button, _type):
        print(">>>", button.get_attribute("aria-label"), _type)

    def target_individual_list(self, lists):
        for _list in lists:
            list_bottom_container = _list.find_element_by_css_selector(
                ".discover-entity-type-card__bottom-container")
            list_footer = list_bottom_container.find_element_by_tag_name(
                "footer")
            invite_button = list_footer.find_element_by_tag_name("button")
            try:
                self.get_aria_label(invite_button, "sending")
                invite_button.click()
            except ElementClickInterceptedException:
                self.get_aria_label(invite_button, "failed")
                continue

    def get_list_items(self, suggestion_box):
        lists = suggestion_box.find_elements_by_tag_name("li")

        self.target_individual_list(lists)

    def get_suggestion_box_by_id(self, _id):
        suggestion_box = self.driver.find_element_by_id(_id)
        self.get_list_items(suggestion_box)

    def get_my_network(self):
        self.driver.get("https://www.linkedin.com/mynetwork/")

    def start_guided_mode(self):
        suggestion_box_id = input("Suggestio Box Id : ")
        self.get_suggestion_box_by_id(suggestion_box_id)

    def run(self):
        self.get_my_network()
        self.start_guided_mode()


if __name__ == "__main__":
    LinkedInConnections()

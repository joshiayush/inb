import time
import colorama

from .LinkedIn import re
from .LinkedIn import By
from .LinkedIn import Keys
from .LinkedIn import LinkedIn
from .LinkedIn import webdriver
from .LinkedIn import ActionChains
from .LinkedIn import WebDriverWait
from .LinkedIn import TimeoutException
from .LinkedIn import expected_conditions
from .LinkedIn import NoSuchElementException
from .LinkedIn import ElementNotInteractableException
from .LinkedIn import ElementClickInterceptedException


class LinkedInConnectionsGuided(LinkedIn):
    """Controls LinkedIn Connections, its name is LinkedInConnectionsGuided
    because it runs the program in guided mode i.e., you have to manually
    input the 'ID' which you want to target, LinkedInConnections with auto
    mode will be coded once finished coding LinkedInConnectionsGuided.

    Parent:
        LinkedIn: our main LinkedIn class which takes care of enabling of
        the webdriver and the login process.
    """

    def __init__(self, data):
        """Function __init__() is the constructor function of class
        LinkedInConnectionsGuided() which intializes objects for this
        class.
        """
        super(LinkedInConnectionsGuided, self).__init__(data)

    def target_individual_list(self, lists):
        """Function target_individual_list() targets <li> items individually
        and then finds the invite button which is nested inside <li> item and
        then performs a click() operation on it, if ElementClickIntercepted
        Exception comes which will come at one point then it handles it
        smoothly.

        Args:
            lists: it is a list object that contains <li> items in it
        """
        for _list in lists:
            list_bottom_container = _list.find_element_by_css_selector(
                ".discover-entity-type-card__bottom-container")
            list_footer = list_bottom_container.find_element_by_tag_name(
                "footer")
            invite_button = list_footer.find_element_by_tag_name("button")
            try:
                LinkedIn.print_status(invite_button, "sending")
                invite_button.click()
            except ElementNotInteractableException:
                LinkedIn.blocked()
                break
            except ElementClickInterceptedException:
                LinkedIn.inform_user(invite_button, "failed")
                continue

    def get_list_items(self, suggestion_box):
        """Function get_list_items() finds the list items available in the
        suggestion box and then sends it to function target_individual_list()
        which targets the list items individually.

        Args:
            suggestion_box: element that contains the list items
        """
        lists = suggestion_box.find_elements_by_tag_name("li")

        self.target_individual_list(lists)

    def get_suggestion_box_by_id(self, _id):
        """Function get_suggestion_box_by_id() targets the suggestion box
        given by the linkedin application (basically it is the box where
        linkedin keeps people that matches with my profile).

        Args:
            _id: id of the suggestion box
        """
        suggestion_box = self.driver.find_element_by_id(_id)

        self.get_list_items(suggestion_box)

    def get_my_network(self):
        """Function get_my_network() changes the url by executing function
        `get()` from webdriver.
        """
        try:
            self.driver.get("https://www.linkedin.com/mynetwork/")
        except TimeoutException:
            LinkedIn.err_loading_resource()

    def start_guided_mode(self):
        """Function start_guided_mode() starts the program in guided mode
        in which the user itself has to guide the program finding the
        suggestion box by entering the ID of the suggestion box manually.
        """
        suggestion_box_id = input("Suggestio Box Id : ")

        self.get_suggestion_box_by_id(suggestion_box_id)

    def run(self):
        """Function run() is the main function from where the program starts
        doing its job.
        """
        self.get_my_network()

        self.start_guided_mode()

import time
import colorama
import urllib.parse

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
                LinkedIn.inform_user(invite_button, "sending")
                invite_button.click()
            except ElementNotInteractableException:
                print("You got Blocked")
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
        self.driver.get("https://www.linkedin.com/mynetwork/")

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


class LinkedInConnectionsAuto(LinkedIn):
    """Controls LinkedIn Connections, its name is LinkedInConnectionsAuto
    because it runs the program in auto mode i.e., here you don't have to
    manually enter the required field for performing automation unlike the
    LinkedInConnectionsGuided class.

    Parent:
        LinkedIn: our main LinkedIn class which takes care of enabling
        of the webdriver and the login process.
    """
    ENTITY_TO_BE_CLICKED = 0

    def __init__(self, data):
        super(LinkedInConnectionsAuto, self).__init__(data)

    def get_my_network(self):
        """Function get_my_network() changes the url by executing function
        `get()` from webdriver.
        """
        print(
            f"""\t    {colorama.Fore.BLUE}{colorama.Style.DIM}Moving to 'mynetwork' page...{colorama.Style.RESET_ALL}\n""")

        self.driver.get("https://www.linkedin.com/mynetwork/")

    def get_people(self):
        people_name = WebDriverWait(self.driver, 10).until(
            expected_conditions.presence_of_all_elements_located(
                (By.CSS_SELECTOR, "span[class^='discover-person-card__name']")
            )
        )

        _people_name = []*len(people_name)

        for span in people_name:
            _people_name.append(span.text)

        del people_name

        people_occupation = WebDriverWait(self.driver, 10).until(
            expected_conditions.presence_of_all_elements_located(
                (By.CSS_SELECTOR,
                 "span[class^='discover-person-card__occupation']")
            )
        )

        _people_occupation = []*len(people_occupation)

        for span in people_occupation:
            _people_occupation.append(span.text)

        del people_occupation

        people_button = WebDriverWait(self.driver, 10).until(
            expected_conditions.presence_of_all_elements_located(
                (By.CSS_SELECTOR, "button[aria-label^='Invite']")
            )
        )

        return [_people_name, _people_occupation, people_button]

    def encode(self, obj):
        return list(zip(obj[0], obj[1], obj[2]))

    def click_buttons(self, obj):
        """Function find_buttons() finds the buttons in the network page
        using webdriver function `find_elements_by_css_selector()` and
        then if they are enabled it executes `click()` function on them
        if not it handles the exception smoothly.
        """
        old_entity_length = len(obj)
        new_entity_length = len(obj)

        start = time.time()

        while True:
            try:
                obj[LinkedInConnectionsAuto.ENTITY_TO_BE_CLICKED][2].click()
                LinkedIn.print_status(
                    obj=obj[LinkedInConnectionsAuto.ENTITY_TO_BE_CLICKED], status="sent", elapsed_time=(time.time() - start))
            except ElementClickInterceptedException:
                LinkedIn.print_status(
                    obj=obj[LinkedInConnectionsAuto.ENTITY_TO_BE_CLICKED], status="failed", elapsed_time=(time.time() - start))
                continue
            except ElementNotInteractableException:
                print(f"""{colorama.Style.BRIGHT}""", end="")
                print(f"""{colorama.Fore.RED}""", end="")

                print("\n It seems like you got blocked by LinkedIn!")

                print(f"""{colorama.Fore.RESET}""", end="")
                print(f"""{colorama.Style.RESET_ALL}""", end="")
                return

            LinkedInConnectionsAuto.ENTITY_TO_BE_CLICKED += 1

            if LinkedInConnectionsAuto.ENTITY_TO_BE_CLICKED == new_entity_length:
                while old_entity_length == new_entity_length:
                    obj = self.encode(self.get_people())
                    old_entity_length = new_entity_length
                    new_entity_length = len(obj)

        LinkedIn.reset_attributes()

    def prepare_page(self):
        """Method prepare_page() prepares the dynamically loading page before
        starting to send inivitations this functionality we needed because the
        page we are targetting loads dynamically and if we directly target the
        buttons on the page then we might end up with sending only 10 to 12
        invitations and that's not what we want we want to keep sending
        inviations until we get blocked by LinkedIn, so this function executes
        javascript (that requires to move to the bottom of the page) for 5000
        repetitions.
        """
        try:
            _ = WebDriverWait(self.driver, 10).until(
                expected_conditions.presence_of_all_elements_located(
                    (By.CSS_SELECTOR, "button[aria-label^='Invite']")
                )
            )

            spinner = "\\"
            _preparing_ = "[.........................]"

            k = 0
            s = 0

            for i in range(5001):
                LinkedIn.execute_javascript(self)
                if i % 200 == 0 and i != 0:
                    _preparing_ = "[" + "#"*(k+1) + _preparing_[k+2:]
                    k += 1
                if i % 50 == 0 and i != 0:
                    spinner = "-\\|/"[s]
                    s += 1
                    if s >= 4:
                        s = 0
                print(f"""{colorama.Fore.BLUE}""", end="")
                print(
                    f""" Preparing page, it might take some time {spinner} {_preparing_}""", end="\r")
                print(f"""{colorama.Fore.RESET}""", end="")

            print()
        except NoSuchElementException:
            pass

    def clear_msg_overlay(self):
        try:
            _ = WebDriverWait(self.driver, 10).until(
                expected_conditions.presence_of_element_located(
                    (By.CSS_SELECTOR, "div[class^='msg-overlay-list-bubble']")
                )
            )
            self.driver.execute_script((
                """document.querySelector("div[class^='msg-overlay-list-bubble']").style = 'display: none';"""
            ))
            return True
        except NoSuchElementException:
            return False

    def run(self):
        """Function run() is the main function from where the program
        starts doing its job.
        """
        self.get_my_network()

        self.clear_msg_overlay()

        """Don't need anymore -> self.prepare_page() ] click_buttons() moves the page for us."""

        self.click_buttons(self.encode(self.get_people()))


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

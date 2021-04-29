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

        try:
            self.driver.get("https://www.linkedin.com/mynetwork/")
        except TimeoutException:
            LinkedIn.err_loading_resource()
            return

    def get_people(self):
        while True:
            try:
                people_name = WebDriverWait(self.driver, 10).until(
                    expected_conditions.presence_of_all_elements_located(
                        (By.CSS_SELECTOR,
                         "span[class^='discover-person-card__name']")
                    )
                )

                _people_name = []*len(people_name)

                for span in people_name:
                    _people_name.append(span.text)

                del people_name
                break
            except TimeoutException:
                LinkedIn.err_loading_resource()
                continue

        while True:
            try:
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
                break
            except TimeoutException:
                LinkedIn.err_loading_resource()
                continue

        while True:
            try:
                people_button = WebDriverWait(self.driver, 10).until(
                    expected_conditions.presence_of_all_elements_located(
                        (By.CSS_SELECTOR, "button[aria-label^='Invite']")
                    )
                )
                break
            except TimeoutException:
                LinkedIn.err_loading_resource()
                continue

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

        red = 1

        start = time.time()

        while True:
            try:
                obj[LinkedInConnectionsAuto.ENTITY_TO_BE_CLICKED][2].click()
                LinkedIn.print_status(
                    obj=obj[LinkedInConnectionsAuto.ENTITY_TO_BE_CLICKED], status="sent", elapsed_time=(time.time() - start))
            except ElementClickInterceptedException:
                LinkedIn.print_status(
                    obj=obj[LinkedInConnectionsAuto.ENTITY_TO_BE_CLICKED], status="failed", elapsed_time=(time.time() - start))
            except ElementNotInteractableException:
                LinkedIn.blocked()

                LinkedInConnectionsAuto.ENTITY_TO_BE_CLICKED = 0

                return

            if LinkedInConnectionsAuto.ENTITY_TO_BE_CLICKED + 1 == new_entity_length:
                while old_entity_length == new_entity_length:
                    LinkedIn.execute_javascript(self)
                    _obj = self.encode(self.get_people())
                    if len(_obj) > len(obj):
                        old_entity_length = new_entity_length
                        new_entity_length = len(_obj)
                        obj = _obj
                        break

            LinkedInConnectionsAuto.ENTITY_TO_BE_CLICKED += 1

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
        except TimeoutException:
            LinkedIn.err_loading_resource()

    def run(self):
        """Function run() is the main function from where the program
        starts doing its job.
        """
        self.get_my_network()

        self.clear_msg_overlay()

        """Don't need anymore -> self.prepare_page() ] click_buttons() moves the page for us."""

        self.click_buttons(self.encode(self.get_people()))

"""from __future__ imports must occur at the beginning of the file. DO NOT CHANGE!"""
from __future__ import annotations

import time

from dom.cleaners import clear_msg_overlay
from dom.javascript import scroll_bottom
from dom.javascript import get_page_y_offset

from messages.console_messages import send_to_console

from errors.error import EmptyResponseException
from errors.error import FailedLoadingResourceException

from invitation.status import show
from invitation.status import reset


from .LinkedIn import By
from .LinkedIn import LinkedIn
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

    def __init__(self: object, data: dict) -> None:
        super(LinkedInConnectionsAuto, self).__init__(data)

    def get_my_network(self: object) -> None:
        """Function get_my_network() changes the url by executing function
        `get()` from webdriver.
        """
        try:
            self.driver.get("https://www.linkedin.com/mynetwork/")
        except TimeoutException:
            raise EmptyResponseException("ERR_EMPTY_RESPONSE")

    def get_entities(self: object) -> list:
        while 1:
            try:
                people_name = WebDriverWait(self.driver, 10).until(
                    expected_conditions.presence_of_all_elements_located(
                        (By.CSS_SELECTOR,
                         "span[class^='discover-person-card__name']")
                    )
                )

                _people_name = [span.text for span in people_name]

                del people_name
                break
            except TimeoutException:
                continue

        while 1:
            try:
                people_occupation = WebDriverWait(self.driver, 10).until(
                    expected_conditions.presence_of_all_elements_located(
                        (By.CSS_SELECTOR,
                         "span[class^='discover-person-card__occupation']")
                    )
                )

                _people_occupation = [span.text for span in people_occupation]

                del people_occupation
                break
            except TimeoutException:
                continue

        while 1:
            try:
                people_button = WebDriverWait(self.driver, 10).until(
                    expected_conditions.presence_of_all_elements_located(
                        (By.CSS_SELECTOR, "button[aria-label^='Invite']")
                    )
                )
                break
            except TimeoutException:
                continue

        return [_people_name, _people_occupation, people_button]

    def encode(self: object, obj: list) -> list:
        return [{"person_name": name, "person_occupation": occupation, "invite_button": button} for name, occupation, button in zip(obj[0], obj[1], obj[2])]

    def load_entities(self) -> None:
        _old_page_offset = get_page_y_offset(self)
        _new_page_offset = get_page_y_offset(self)

        while _old_page_offset == _new_page_offset:
            scroll_bottom(self)
            time.sleep(1)
            _new_page_offset = get_page_y_offset(self)

        return

    def get_person(self: LinkedInConnectionsAuto) -> dict:
        _person_list = self.encode(self.get_entities())

        while 1:
            for _person in _person_list:
                yield _person
            self.load_entities()
            _person_list = self.encode(self.get_entities())

    def click_buttons(self: object) -> None:
        """Function find_buttons() finds the buttons in the network page
        using webdriver function `find_elements_by_css_selector()` and
        then if they are enabled it executes `click()` function on them
        if not it handles the exception smoothly.
        """
        _start = time.time()

        for _person in self.get_person():
            try:
                if not _person["invite_button"].find_element_by_tag_name("span").text == "Connect":
                    continue
                _person["invite_button"].click()
                show(name=_person["person_name"], occupation=_person["person_occupation"],
                     status="sent", elapsed_time=time.time() - _start)
                continue
            except ElementNotInteractableException:
                show(name=_person["person_name"], occupation=_person["person_occupation"],
                     status="failed", elapsed_time=time.time() - _start)
                continue
            except ElementClickInterceptedException:
                reset()

        reset()

    def run(self: object) -> None:
        """Function run() is the main function from where the program
        starts doing its job.
        """
        try:
            self.get_my_network()
        except EmptyResponseException:
            send_to_console("ERR_EMPTY_RESPONSE",
                            color='r', style='b', pad='8')

        try:
            clear_msg_overlay(self)
        except FailedLoadingResourceException:
            send_to_console("ERR_LOADING_RESOURCE",
                            color='r', style='b', pad='8')

        self.click_buttons()

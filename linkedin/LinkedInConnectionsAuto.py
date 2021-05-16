"""from __future__ imports must occur at the beginning of the file. DO NOT CHANGE!"""
from __future__ import annotations

import time

from .LinkedIn import LinkedIn

from dom.javascript import scroll_bottom
from dom.javascript import get_page_y_offset

from errors.error import EmptyResponseException
from errors.error import PropertyNotExistException
from errors.error import ConnectionLimitExceededException

from selenium.webdriver.common.by import By

from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.ui import WebDriverWait

from selenium.common.exceptions import TimeoutException


class LinkedInConnectionsAuto(LinkedIn):
    """Controls LinkedIn Connections, its name is LinkedInConnectionsAuto
    because it runs the program in auto mode i.e., here you don't have to
    manually enter the required field for performing automation unlike the
    LinkedInConnectionsGuided class.

    Parent:
        LinkedIn: our main LinkedIn class which takes care of enabling
        of the webdriver and the login process.
    """
    SENT_INVITATION = 0

    def __init__(self: object, obj: object, limit: int = 40) -> None:
        if not hasattr(obj, "driver"):
            PropertyNotExistException(
                "Object 'obj' doesn't have property 'driver' in it!")

        setattr(self, "driver", getattr(obj, "driver"))

        if limit > 80:
            raise ConnectionLimitExceededException(
                "Daily invitation limit can't be greater than 80, we recommend 40!")

        self._limit = limit

    def get_my_network(self: object, url: str = "https://www.linkedin.com/mynetwork/") -> None:
        """Function get_my_network() changes the url by executing function
        `get()` from webdriver.
        """
        try:
            self.driver.get(url)
        except TimeoutException:
            raise EmptyResponseException("ERR_EMPTY_RESPONSE")

    def find_all_elements_by_css_selector(self, selector: str = '', wait_time: int = 10) -> object:
        """Method find_all_elements_by_css_selector()
        """
        while 1:
            try:
                return WebDriverWait(self.driver, wait_time).until(
                    expected_conditions.presence_of_all_elements_located(
                        (By.CSS_SELECTOR, selector)
                    )
                )
            except TimeoutException:
                continue

    def get_entities(self: object) -> list:
        """Method get_entities()
        """
        people_name = self.find_all_elements_by_css_selector(
            "span[class^='discover-person-card__name']")

        _people_name = [span.text for span in people_name]

        del people_name

        people_occupation = self.find_all_elements_by_css_selector(
            "span[class^='discover-person-card__occupation']")

        _people_occupation = [span.text for span in people_occupation]

        del people_occupation

        people_button = self.find_all_elements_by_css_selector(
            "button[aria-label^='Invite']")

        return [_people_name, _people_occupation, people_button]

    def encode(self: object, obj: list) -> list:
        """Method encode()
        """
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
        """Method get_person()
        """
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
        from invitation.status import show
        from invitation.status import reset

        from selenium.common.exceptions import ElementNotInteractableException
        from selenium.common.exceptions import ElementClickInterceptedException

        _start = time.time()

        for _person in self.get_person():
            try:
                if LinkedInConnectionsAuto.SENT_INVITATION == self._limit:
                    LinkedInConnectionsAuto.SENT_INVITATION = 0
                    break
                if not _person["invite_button"].find_element_by_tag_name("span").text == "Connect":
                    continue
                _person["invite_button"].click()
                show(name=_person["person_name"], occupation=_person["person_occupation"],
                     status="sent", elapsed_time=time.time() - _start)
                LinkedInConnectionsAuto.SENT_INVITATION += 1
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
        self.click_buttons()

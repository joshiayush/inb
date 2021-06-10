"""from __future__ imports must occur at the beginning of the file. DO NOT CHANGE!"""
from __future__ import annotations

import time

from linkedin.linkedin import LinkedIn

from DOM.javascript import scroll_bottom
from DOM.javascript import get_page_y_offset

from errors.error import EmptyResponseException
from errors.error import PropertyNotExistException
from errors.error import ConnectionLimitExceededException

from selenium.webdriver.common.by import By

from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.ui import WebDriverWait

from selenium.common.exceptions import TimeoutException


class LinkedInConnectionsAuto(object):
    SENT_INVITATION = 0

    def __init__(self: LinkedInConnectionsAuto, _linkedin: LinkedIn, limit: int = 40) -> None:
        """LinkedInConnectionsAuto class constructor to initialise LinkedInConnectionsAuto object.

        :Args:
            - self: {LinkedInConnectionsAuto} object
            - _linkedin: {LinkedIn} LinkedIn class object to access the driver object
            - limit: {int} daily invitation limit

        :Returns:
            - {LinkedInConnectionsAuto} LinkedInConnectionsAuto object

        :Raises:
            - PropertyNotExistException if object _linkedin doesn't have a property driver in it
            - ConnectionLimitExceededException if user gives a connection limit that exceeds 80

        :Usage:
            - _linkedin_connection_auto = LinkedInConnectionAuto(_linkedin, 40)
        """
        if not hasattr(_linkedin, "driver"):
            PropertyNotExistException(
                "Object '_linkedin' doesn't have property 'driver' in it!")

        setattr(self, "driver", getattr(_linkedin, "driver"))

        if limit > 80:
            raise ConnectionLimitExceededException(
                "Daily invitation limit can't be greater than 80, we recommend 40!")

        self._limit = limit

    def get_my_network(self: LinkedInConnectionsAuto, _url: str = "https://www.linkedin.com/mynetwork/") -> None:
        """Method get_my_network() sends a GET request to the network page of LinkedIn.

        :Args:
            - self: {LinkedInConnectionsAuto} object
            - _url: {str} url to send GET request to

        :Returns:
            - {None}

        :Raises:
            - EmptyResponseException if there is a TimeoutException

        :Usage:
            - _linkedin_connections_auto.get_my_network("https://www.linkedin.com/mynetwork/")
        """
        try:
            self.driver.get(_url)
        except TimeoutException:
            raise EmptyResponseException("ERR_EMPTY_RESPONSE")

    def find_all_elements_by_css_selector(self: LinkedInConnectionsAuto, selector: str = '', wait_time: int = 10) -> object:
        """Method find_all_elements_by_css_selector() finds all the elements with the given css
        selector, it also implicitly waits until the resource loads for the given wait time.

        :Args:
            - self: {LinkedInConnectionsAuto} object
            - selector: {str} css selector using which we will locate the resource
            - wait_time: {int} time to wait for until the resource loads

        :Returns:
            - {WebElement}
        """
        while 1:
            try:
                return WebDriverWait(self.driver, wait_time).until(
                    expected_conditions.presence_of_all_elements_located(
                        (By.CSS_SELECTOR, selector)))
            except TimeoutException:
                continue

    def get_entities(self: LinkedInConnectionsAuto) -> list:
        """Method get_entities() returns a list of the name, occupation and the connect button.

        :Args:
            - self: {LinkedInConnectionsAuto} object

        :Returns:
            - {list} a list of the name, occupation and the connect button
        """
        people_name = self.find_all_elements_by_css_selector(
            "span[class^='discover-person-card__name']")

        people_occupation = self.find_all_elements_by_css_selector(
            "span[class^='discover-person-card__occupation']")

        people_button = self.find_all_elements_by_css_selector(
            "button[aria-label^='Invite']")

        return [[span.text for span in people_name], [span.text for span in people_occupation], people_button]

    def encode(self: LinkedInConnectionsAuto, _obj: list) -> list:
        """Method encode() forms individual dictionaries for each person with its name,
        occupation and the connect button.

        :Args:
            - self: {LinkedInConnectionsAuto} object
            - _obj: {list} list object returned from method get_entities()

        :Returns:
            - {list} list of dictionaries with each person with its name, occupation and
                connect button
        """
        return [{"person_name": name, "person_occupation": occupation, "invite_button": button} for name, occupation, button in zip(_obj[0], _obj[1], _obj[2])]

    def load_entities(self: LinkedInConnectionsAuto) -> None:
        """Method load_entities() loads more person on the page by scrolling to the bottom.

        :Args:
            - self: {LinkedInConnectionsAuto} object

        :Returns:
            - {None}
        """
        _old_page_offset = get_page_y_offset(self)
        _new_page_offset = get_page_y_offset(self)

        while _old_page_offset == _new_page_offset:
            scroll_bottom(self)

            time.sleep(1)

            _new_page_offset = get_page_y_offset(self)

    def get_person(self: LinkedInConnectionsAuto) -> None:
        """Method get_person() yeilds one person at a time with its name, occupation and
        connect button.

        :Args:
            - self: {LinkedInConnectionsAuto} object

        :Returns:
            - {None}

        :Yeilds:
            - {dict} dictionary of a person with its name, occupation and connect button
        """
        _person_list = self.encode(self.get_entities())

        while 1:
            for _person in _person_list:
                yield _person

            self.load_entities()

            _person_list = self.encode(self.get_entities())

    def send_invitation(self: LinkedInConnectionsAuto) -> None:
        """Method send_invitation() starts sending invitation to people on linkedin.

        :Args:
            - self: {LinkedInConnectionsAuto} object

        :Returns:
            - {None}
        """
        from invitation.status import show
        from invitation.status import reset

        from selenium.common.exceptions import ElementNotInteractableException
        from selenium.common.exceptions import ElementClickInterceptedException

        _start = time.time()

        for _person in self.get_person():
            try:
                if LinkedInConnectionsAuto.SENT_INVITATION == self._limit:
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
                break

        reset()

    def run(self: LinkedInConnectionsAuto) -> None:
        """Method run() calls the send_invitation method, but first it assures that the object
        self has driver property in it.

        :Args:
            - self: {LinkedInConnectionsAuto} object

        :Returns:
            - {None}
        """
        if not hasattr(self, "driver"):
            PropertyNotExistException(
                "Object 'self' doesn't have property 'driver' in it!")

        self.send_invitation()

    def __del__(self: LinkedInConnectionsAuto) -> None:
        """LinkedInConnectionsAuto destructor to de-initialise LinkedInConnectionsAuto object.

        :Args:
            - self: {LinkedInConnectionsAuto} object

        :Returns:
            - {None}
        """
        LinkedInConnectionsAuto.SENT_INVITATION = 0

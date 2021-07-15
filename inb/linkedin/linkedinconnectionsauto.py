"""from __future__ imports must occur at the beginning of the file. DO NOT CHANGE!"""
from __future__ import annotations

import time

from invitation.status import show
from invitation.status import reset

from DOM.cleaners import ClearMessageOverlay

from . import __first_entity_list_container_xpath__
from . import __second_entity_list_container_xpath__

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
from selenium.common.exceptions import ElementNotInteractableException
from selenium.common.exceptions import ElementClickInterceptedException

from selenium.webdriver.common.action_chains import ActionChains


"""@TODO: Use xpath to target entities. This is the most efficient way of connecting to people automatically."""


class LinkedInConnectionsAuto(object):
    SENT_INVITATION = 0
    SUGGESTION_BOX_UL_XPATH = """/html/body/div[6]/div[3]/div/div/div/div/div/div/div/main/div[2]/section/section/ul/li[1]"""

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

    def discover_entity_list(self: LinkedInConnectionsAuto, xpath: str = "", wait_time: int = 10) -> object:
        """Method discover_entity_list() returns a WebElement that is located at the given xpath.

        :Args:
            - self: {LinkedInConnectionsAuto} object
            - xpath: {str} xpath to the WebElement
            - wait_time: {int} time to wait until the WebElement loads

        :Returns:
            - {WebElement}
        """
        while True:
            try:
                return WebDriverWait(self.driver, wait_time).until(
                    expected_conditions.presence_of_element_located(
                        (By.XPATH, xpath)))
            except TimeoutException:
                continue

    def discover_entities(self: LinkedInConnectionsAuto, xpath: str = '') -> list:
        """Method discover_entities() returns a list of WebElement that is inside of the WebElement
        at the given xpath.

        :Args:
            - self: {LinkedInConnectionsAuto} object
            - xpath: {str} xpath to the WebElement

        :Returns:
            - {list} list of web elements
        """
        return self.discover_entity_list(xpath=xpath, wait_time=10).find_elements_by_tag_name("li")

    def get_entities(self: LinkedInConnectionsAuto, _list: list) -> list:
        """Method get_entities() returns a list of entities (i.e., people object) that is in the network
        page.

        :Args:
            - self: {LinkedInConnectionsAuto} object
            - _list: {list} list of web elements

        :Returns:
            - {list} list of entities
        """
        return [li.find_element_by_tag_name("div").find_element_by_tag_name("section") for li in _list]

    def get_people(self: LinkedInConnectionsAuto) -> list:
        """Method get_people() returns a list of entities that are located at the __first_entity_list_container_xpath__
        and at the __second_entity_list_container_xpath__.

        :Args:
            - self: {LinkedInConnectionsAuto} object

        :Returns:
            - {list} list of entities
        """
        return self.get_entities(self.discover_entities(
            __first_entity_list_container_xpath__)) + self.get_entities(
                self.discover_entities(__second_entity_list_container_xpath__))

    def get_people_names(self: LinkedInConnectionsAuto, _people: list) -> list:
        """Method get_people_names() returns a list of names that are inside of this _people list.

        :Args:
            - self: {LinkedInConnectionsAuto} object
            - _people: {list} list of web elements

        :Returns:
            - {list} list of names
        """
        return [p.find_element_by_css_selector(
            "div[class='discover-entity-type-card__info-container']").find_element_by_css_selector(
            "span[class^='discover-person-card__name']").text for p in _people]

    def get_people_occupation(self: LinkedInConnectionsAuto, _people: list):
        """Method get_people_occupation() returns a list of occupation that are inside of this _people list.

        :Args:
            - self: {LinkedInConnectionsAuto} object
            - _people: {list} list of web elements

        :Returns:
            - {list} list of occupation
        """
        return [p.find_element_by_css_selector(
            "div[class='discover-entity-type-card__info-container']").find_element_by_css_selector(
            "span[class^='discover-person-card__occupation']").text for p in _people]

    def get_people_buttons(self: LinkedInConnectionsAuto, _people: list):
        """Method get_people_buttons() returns a list of buttons that are inside of this _people list.

        :Args:
            - self: {LinkedInConnectionsAuto} object
            - _people: {list} list of web elements

        :Returns:
            - {list} list of buttons
        """
        return [p.find_element_by_css_selector(
            "div[class='discover-entity-type-card__bottom-container']").find_element_by_tag_name(
            "footer").find_element_by_tag_name("button") for p in _people]

    def get_person_list(self: LinkedInConnectionsAuto):
        """Method get_person_list() returns a list containing list of names, occupation and buttons.

        :Args:
            - self: {LinkedInConnectionsAuto} object

        :Returns:
            - {list} list containing list of names, occupation and buttons
        """
        _people = self.get_people()

        return [self.get_people_names(_people), self.get_people_occupation(_people), self.get_people_buttons(_people)]

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
        _person_list = self.encode(self.get_person_list())

        while 1:
            for _person in _person_list:
                yield _person

            self.load_entities()

            _person_list = self.encode(self.get_person_list())

    def send_invitation(self: LinkedInConnectionsAuto) -> None:
        """Method send_invitation() starts sending invitation to people on linkedin.

        :Args:
            - self: {LinkedInConnectionsAuto} object

        :Returns:
            - {None}
        """
        _driver = getattr(self, "driver")

        _start = time.time()

        for _person in self.get_person():
            try:
                if LinkedInConnectionsAuto.SENT_INVITATION == self._limit:
                    break

                if not _person["invite_button"].find_element_by_tag_name("span").text == "Connect":
                    continue

                ActionChains(_driver).move_to_element(
                    _person["invite_button"]).click().perform()
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

    def execute_cleaners(self: LinkedInConnectionsAuto) -> None:
        ClearMessageOverlay(self)

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

        self.execute_cleaners()

        self.send_invitation()

    def __del__(self: LinkedInConnectionsAuto) -> None:
        """LinkedInConnectionsAuto destructor to de-initialise LinkedInConnectionsAuto object.

        :Args:
            - self: {LinkedInConnectionsAuto} object

        :Returns:
            - {None}
        """
        LinkedInConnectionsAuto.SENT_INVITATION = 0

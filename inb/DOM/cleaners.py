from __future__ import annotations

from selenium import webdriver
from selenium.webdriver.common.by import By

from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.ui import WebDriverWait

from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import NoSuchElementException


class Cleaner(object):
    def __init__(self: Cleaner, driver: webdriver.Chrome) -> None:
        """Constructor method to initialize a Cleaner object.

        :Args:
            - self: {Cleaner} self.
            - driver: {webdriver} Chromedriver

        :Raises:
            - {Exception} if 'driver' object is not a 'webdriver' instance.
        """
        if not isinstance(driver, webdriver.Chrome):
            raise Exception("'%(driver_type)s' object is not a 'webdriver' object" % {
                            "driver_type": type(driver)})

        self._driver = driver

    def clear_message_overlay(self: Cleaner, time_out: int = 60) -> None:
        """Function clear_msg_overlay() clears the message overlay that gets on the top of the
        network page.

        :Args:
            - self: {Cleaner} object from which 'driver' property has to accessed.
            - time_out: {int} timeout

        :Returns:
            - {None}
        """
        try:
            WebDriverWait(self._driver, time_out).until(
                expected_conditions.presence_of_element_located(
                    (By.CSS_SELECTOR, "div[class^='msg-overlay-list-bubble']")))

            self._driver.execute_script(
                """document.querySelector("div[class^='msg-overlay-list-bubble']").style = "display: none";""")
        except (NoSuchElementException, TimeoutException):
            return

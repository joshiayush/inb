from errors.error import PropertyNotExistException
from errors.error import FailedLoadingResourceException

from selenium.webdriver.common.by import By

from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.ui import WebDriverWait

from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import NoSuchElementException


def clear_msg_overlay(self: object) -> None:
    if not hasattr(self, "driver"):
        raise PropertyNotExistException(
            "Object 'self' must have a property 'driver' in it!")

    try:
        WebDriverWait(getattr(self, "driver"), 10).until(
            expected_conditions.presence_of_element_located(
                (By.CSS_SELECTOR, "div[class^='msg-overlay-list-bubble']")
            )
        )
        getattr(getattr(self, "driver"), "execute_script")((
            """document.querySelector("div[class^='msg-overlay-list-bubble']").style = 'display: none';"""
        ))
    except NoSuchElementException:
        raise NoSuchElementException(
            "There is not such element exist by css selector 'div[class^='msg-overlay-list-bubble']'!")
    except TimeoutException:
        raise FailedLoadingResourceException("ERR_LOADING_RESOURCE")

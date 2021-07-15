from errors.error import PropertyNotExistException

from selenium.webdriver.common.by import By

from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.ui import WebDriverWait

from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import NoSuchElementException


def ClearMessageOverlay(self: object) -> None:
    """Function clear_msg_overlay() clears the message overlay that gets on the top of the
    network page.

    :Args:
        - self: {object} object from which 'driver' property has to accessed.

    :Raises:
        - {PropertyNotExistException} if object 'self' does not has a property called 'driver'.

    :Returns:
        - {None}
    """
    if not hasattr(self, "driver"):
        raise PropertyNotExistException(
            "Object 'self' must have a property 'driver' in it!")

    while True:
        try:
            WebDriverWait(getattr(self, "driver"), 10).until(
                expected_conditions.presence_of_element_located(
                    (By.CSS_SELECTOR, "div[class^='msg-overlay-list-bubble']")))

            getattr(getattr(self, "driver"), "execute_script")(
                """document.querySelector("div[class^='msg-overlay-list-bubble']").style = "display: none";""")

            break
        except NoSuchElementException:
            return
        except TimeoutException:
            continue

from errors.error import PropertyNotExistException


def get_page_y_offset(self: object) -> int:
    """Function get_page_y_offset() returns the window.pageYOffset of the webpage, 
    we need that so we can keep on scrolling untill the page offset becomes constant.

    :Args:
        - self: {object} object from which 'driver' property is to be accessed.

    :Raises:
        - {PropertyNotExistException} if 'self' does not has a property called 'driver'.

    :Returns:
        - {int} window.pageYOffset
    """
    if not hasattr(self, "driver"):
        raise PropertyNotExistException(
            "Object 'self' must have a property 'driver' in it!")

    return self.driver.execute_script((
        "return (window.pageYOffset !== undefined)"
        "       ? window.pageYOffset"
        "       : (document.documentElement || document.body.parentNode || document.body);"
    ))


def scroll_bottom(self: object) -> None:
    """Function scroll_bottom() scrolls the web page to the very bottom of it using 
    the 'document.scrollingElement.scrollTop' property.

    :Args:
        - self: {object} object from which 'driver' property is to be accessed.

    :Raises:
        - {PropertyNotExistException} if 'self' does not has a property called 'driver'.

    :Returns:
        - {None}
    """
    if not hasattr(self, "driver"):
        raise PropertyNotExistException(
            "Object 'self' must have a property 'driver' in it!")

    self.driver.execute_script((
        "var scrollingElement = (document.scrollingElement || document.body);"
        "scrollingElement.scrollTop = scrollingElement.scrollHeight;"
    ))

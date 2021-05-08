def get_page_y_offset(self: object) -> int:
    """Function get_page_y_offset() returns the window.pageYOffset
    of the webpage, we need that so we can keep on scrolling untill
    the page offset becomes constant. Declaration of this method is
    static because we want to use this function across multiple
    classes.

    Args:
        self: is not a object here but it is a parameter object
        that has a property 'driver' and we need that

    return:
        window.pageYOffset
    """
    if not "driver" in self:
        return

    return self.driver.execute_script((
        "return (window.pageYOffset !== undefined)"
        "       ? window.pageYOffset"
        "       : (document.documentElement || document.body.parentNode || document.body);"
    ))


def execute_javascript(self: object) -> None:
    """Function execute_javascript() scrolls the web page to the 
    very bottom of it using the 'document.scrollingElement.scrollTop' 
    property.

    Args:
        self: it is a parameter object that has a property 'driver' 
        in it and we need that to access the webpage.
    """
    if not "driver" in self:
        return

    self.driver.execute_script((
        "var scrollingElement = (document.scrollingElement || document.body);"
        "scrollingElement.scrollTop = scrollingElement.scrollHeight;"
    ))

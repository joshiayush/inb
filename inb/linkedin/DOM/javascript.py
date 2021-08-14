# MIT License
#
# Copyright (c) 2019 Creative Commons
#
# Permission is hereby granted, free of charge, to any person obtaining a
# copy of this software and associated documentation files (the "Software"),
# to deal in the Software without restriction, including without limitation
# the rights to use, copy, modify, merge, publish, distribute, sublicense,
# and/or sell copies of the Software, and to permit persons to whom the
# Software is furnished to do so, subject to the following conditions
#
# The above copyright notice and this permission notice shall be included
# in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS
# OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.

"""from __future__ imports must occur at the beginning of the file. DO NOT CHANGE!"""
from __future__ import annotations

from selenium import webdriver


class JS(object):
    def __init__(self: JS, driver: webdriver.Chrome) -> None:
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

    def get_page_y_offset(self: JS) -> int:
        """Method get_page_y_offset() returns the window.pageYOffset of the webpage, 
        we need that so we can keep on scrolling untill the page offset becomes constant.

        :Args:
            - self: {object} object from which '_driver' property is to be accessed.

        :Returns:
            - {int} window.pageYOffset
        """
        return self._driver.execute_script((
            "return (window.pageYOffset !== undefined)"
            "       ? window.pageYOffset"
            "       : (document.documentElement || document.body.parentNode || document.body);"
        ))

    def scroll_bottom(self: JS) -> None:
        """Method scroll_bottom() scrolls the web page to the very bottom of it using 
        the 'document.scrollingElement.scrollTop' property.

        :Args:
            - self: {JS} object from which '_driver' property is to be accessed.

        :Returns:
            - {None}
        """
        self._driver.execute_script((
            "var scrollingElement = (document.scrollingElement || document.body);"
            "scrollingElement.scrollTop = scrollingElement.scrollHeight;"
        ))

"""from __future__ imports must occur at the beginning of the file. DO NOT CHANGE!"""
from __future__ import annotations

import json
import unittest

from .. import failed
from .. import message

from linkedin.linkedin import LinkedIn

from selenium.webdriver import Chrome
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.remote.webelement import WebElement

user_email = ''
user_password = ''
driver_path = ''

with open("/Python/linkedin-bot/linkedin-bot/tests/creds/creds.json") as _file:
    creds = json.load(_file)

    user_email = creds["user_email"]
    user_password = creds["user_password"]
    driver_path = creds["driver_path"]

_linkedin = LinkedIn(
    {"user_email": user_email, "user_password": user_password}, driver_path=driver_path)


class TestLinkedIn(unittest.TestCase):

    def test_getters(self: TestLinkedIn) -> None:
        self.assertIsInstance(_linkedin.user_email, str, message(
            f"_linkedin.user_email must return string type! Test failed {failed}", 'r'))
        self.assertIsInstance(_linkedin.user_password, str, message(
            f"_linkedin.user_password must return string type! Test failed {failed}", 'r'))

        self.assertEqual(_linkedin.user_email, user_email, message(
            f"_linkedin.user_email must be equal to the given user email! Test failed {failed}", 'r'))
        self.assertEqual(_linkedin.user_password, user_password, message(
            f"_linkedin.user_password must be equal to the given user password! Test failed {failed}", 'r'))

    def test_setters(self: TestLinkedIn) -> None:
        _linkedin.user_email = "xxx-xxx-xxx"

        self.assertIsInstance(_linkedin.user_email, str, message(
            f"_linkedin.user_email must set a string type! Test failed {failed}", 'r'))
        self.assertEqual(_linkedin.user_email, "xxx-xxx-xxx", message(
            f"_linkedin.user_email must set user email to the given user email! Test failed {failed}", 'r'))

        _linkedin.user_email = user_email

        _linkedin.user_password = "xxx-xxx-xxx"

        self.assertIsInstance(_linkedin.user_password, str, message(
            f"_linkedin.user_password must set a string type! Test failed {failed}", 'r'))
        self.assertEqual(_linkedin.user_password, "xxx-xxx-xxx", message(
            f"_linkedin.user_password must set user password to the given user password! Test failed {failed}", 'r'))

        _linkedin.user_password = user_password

    def test_get_chrome_driver_options(self: TestLinkedIn) -> None:
        _linkedin.set_headless()
        _linkedin.set_browser_incognito_mode()
        _linkedin.set_ignore_certificate_error()

        self.assertIsInstance(_linkedin.get_chrome_driver_options(), Options, message(
            f"_linkedin.get_chrome_driver_options method must return list type! Test failed {failed}", 'r'))

    def test_webdriver_chrome(self: TestLinkedIn) -> None:
        LinkedIn.SESSION_ALREADY_EXISTS = False

        _linkedin.set_headless()
        _linkedin.set_browser_incognito_mode()
        _linkedin.set_ignore_certificate_error()

        _linkedin.enable_webdriver_chrome(
            _linkedin.get_chrome_driver_options())

        self.assertIsInstance(_linkedin.driver, Chrome, message(
            f"_linkedin.driver must be of Chrome type! Test failed {failed}", 'r'))

        _linkedin.disable_webdriver_chrome()

        LinkedIn.SESSION_ALREADY_EXISTS = False

    def test_web_elements(self: TestLinkedIn) -> None:
        LinkedIn.SESSION_ALREADY_EXISTS = False

        _linkedin.set_headless()
        _linkedin.set_browser_incognito_mode()
        _linkedin.set_ignore_certificate_error()

        _linkedin.enable_webdriver_chrome(
            _linkedin.get_chrome_driver_options())

        _linkedin.get_login_page("https://www.linkedin.com/login")

        self.assertIsInstance(_linkedin.get_email_box(), WebElement, message(
            f"_linkedin.get_email_box method must return WebElement type! Test failed {failed}", 'r'))
        self.assertIsInstance(_linkedin.get_password_box(), WebElement, message(
            f"_linkedin.get_password_box method must return WebElement type! Test failed {failed}", 'r'))

        _linkedin.disable_webdriver_chrome()

        LinkedIn.SESSION_ALREADY_EXISTS = False

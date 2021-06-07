from __future__ import annotations

import json

from . import passed
from . import failed

from console.print import printBlue, printRed
from console.print import printGreen

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


def test_getters(_linkedin: LinkedIn) -> None:
    assert isinstance(_linkedin.user_email, str), \
        "tests/linkedintest.py _linkedin.user_email must return string type! Test failed " + failed
    assert isinstance(_linkedin.user_password, str), \
        "tests/linkedintest.py _linkedin.user_password must return string type! Test failed " + failed

    global user_email
    global user_password

    assert _linkedin.user_email == user_email, \
        "tests/linkedintest.py _linkedin.user_email must be equal to the given user email! Test failed " + failed
    assert _linkedin.user_password == user_password, \
        "tests/linkedintest.py _linkedin.user_password must be equal to the given user password! Test failed " + failed


def test_setters(_linkedin: LinkedIn) -> None:
    _linkedin.user_email = "xxx-xxx-xxx"

    assert isinstance(_linkedin.user_email, str), \
        "tests/linkedintest.py _linkedin.user_email must set a string type! Test failed " + failed
    assert _linkedin.user_email == "xxx-xxx-xxx", \
        "tests/linkedintest.py _linkedin.user_email must set user email to the given user email! Test failed " + failed

    global user_email
    _linkedin.user_email = user_email

    _linkedin.user_password = "xxx-xxx-xxx"

    assert isinstance(_linkedin.user_password, str), \
        "tests/linkedintest.py _linkedin.user_password must set a string type! Test failed " + failed
    assert _linkedin.user_password == "xxx-xxx-xxx", \
        "tests/linkedintest.py _linkedin.user_password must set user password to the given user password! Test failed " + failed

    global user_password
    _linkedin.user_password = user_password


def test_get_chrome_driver_options_method(_linkedin: LinkedIn) -> None:
    _linkedin.set_headless()
    _linkedin.set_browser_incognito_mode()
    _linkedin.set_ignore_certificate_error()

    assert isinstance(_linkedin.get_chrome_driver_options(), Options), \
        "tests/linkedintest.py _linkedin.get_chrome_driver_options method must return list type! Test failed " + failed


def test_webdriver_chrome(_linkedin: LinkedIn) -> None:
    _linkedin.set_headless()
    _linkedin.set_browser_incognito_mode()
    _linkedin.set_ignore_certificate_error()

    _linkedin.enable_webdriver_chrome(_linkedin.get_chrome_driver_options())

    assert isinstance(_linkedin.driver, Chrome), \
        "tests/linkedintest.py _linkedin.driver must be of Chrome type! Test failed " + failed

    _linkedin.disable_webdriver_chrome()

    LinkedIn.SESSION_ALREADY_EXISTS = False


def test_web_elements(_linkedin: LinkedIn) -> None:
    _linkedin.set_headless()
    _linkedin.set_browser_incognito_mode()
    _linkedin.set_ignore_certificate_error()

    _linkedin.enable_webdriver_chrome(_linkedin.get_chrome_driver_options())

    _linkedin.get_login_page("https://www.linkedin.com/login")

    assert isinstance(_linkedin.get_email_box(), WebElement), \
        "tests/linkedintest.py _linkedin.get_email_box method must return WebElement type! Test failed " + failed
    assert isinstance(_linkedin.get_password_box(), WebElement), \
        "tests/linkedintest.py _linkedin.get_password_box method must return WebElement type! Test failed " + failed

    _linkedin.disable_webdriver_chrome()

    LinkedIn.SESSION_ALREADY_EXISTS = False


def test_linkedin() -> list:
    LinkedInTestNumber = 0
    LinkedInTestFailed = 0
    LinkedInTestSuccess = 0

    global user_email
    global user_password
    global driver_path

    _linkedin = LinkedIn(
        {"user_email": user_email, "user_password": user_password}, driver_path=driver_path)

    try:
        printBlue(
            "tests/linkedintest.py getter methods testing ...", style='b', end='\r')
        test_getters(_linkedin)
        print(' '*80, end='\r')
        printGreen(
            "tests/linkedintest.py getter methods passed " + passed, style='b')
        LinkedInTestSuccess += 1
    except AssertionError as error:
        printRed(error)
        LinkedInTestFailed += 1
    finally:
        LinkedInTestNumber += 1

    try:
        printBlue(
            "tests/linkedintest.py setter methods testing ...", style='b', end='\r')
        test_setters(_linkedin)
        print(' '*80, end='\r')
        printGreen(
            "tests/linkedintest.py setter methods passed " + passed, style='b')
        LinkedInTestSuccess += 1
    except AssertionError as error:
        printRed(error)
        LinkedInTestFailed += 1
    finally:
        LinkedInTestNumber += 1

    try:
        printBlue(
            "tests/linkedintest.py chrome driver options testing ...", style='b', end='\r')
        test_get_chrome_driver_options_method(_linkedin)
        print(' '*80, end='\r')
        printGreen(
            "tests/linkedintest.py chrome driver options passed " + passed, style='b')
        LinkedInTestSuccess += 1
    except AssertionError as error:
        printRed(error)
        LinkedInTestFailed += 1
    finally:
        LinkedInTestNumber += 1

    try:
        printBlue(
            "tests/linkedintest.py chrome driver testing ...", style='b', end='\r')
        test_webdriver_chrome(_linkedin)
        print(' '*80, end='\r')
        printGreen(
            "tests/linkedintest.py chrome driver passed " + passed, style='b')
        LinkedInTestSuccess += 1
    except AssertionError as error:
        printRed(error)
        LinkedInTestFailed += 1
    finally:
        LinkedInTestNumber += 1

    try:
        printBlue(
            "tests/linkedintest.py web elements testing ...", style='b', end='\r')
        test_web_elements(_linkedin)
        print(' '*80, end='\r')
        printGreen(
            "tests/linkedintest.py web elements passed " + passed, style='b')
        LinkedInTestSuccess += 1
    except AssertionError as error:
        printRed(error)
        LinkedInTestFailed += 1
    finally:
        LinkedInTestNumber += 1

    return [LinkedInTestNumber, LinkedInTestSuccess, LinkedInTestFailed]

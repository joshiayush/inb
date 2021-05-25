from __future__ import annotations

import json

from . import passed
from . import failed

from console.print import printRed
from console.print import printGreen

from linkedin.LinkedIn import LinkedIn

from selenium.webdriver.chrome.options import Options

user_email = ''
user_password = ''
driver_path = ''

with open("/Python/linkedin-bot/linkedin-bot/tests/creds/creds.json") as _file:
    creds = json.load(_file)

    user_email = creds["user_email"]
    user_password = creds["user_password"]
    driver_path = creds["driver_path"]


def test_initial_state() -> None:
    assert LinkedIn.OLD_EMAIL == '', \
        "LinkedInTest.py 'LinkedIn.OLD_EMAIL' should be emtpy initially! test failed " + failed
    assert LinkedIn.OLD_PASSWORD == '', \
        "LinkedInTest.py 'LinkedIn.OLD_PASSWORD' should be empty initially! test failed " + failed
    assert LinkedIn.SESSION_ALREADY_EXISTS == False, \
        "LinkedInTest.py LinkedIn.SESSION_ALREADY_EXISTS' should be False initially! test failed " + failed


def test_after_initialisation(_linkedin: LinkedIn) -> None:
    global user_email
    global user_password

    assert _linkedin.OLD_EMAIL == user_email, \
        "LinkedInTest.py 'LinkedIn.OLD_EMAIL' should be equal to given user email! test failed " + failed
    assert _linkedin.OLD_PASSWORD == user_password, \
        "LinkedInTest.py 'LinkedIn.OLD_PASSWORD' should be equal to given user password! test failed " + failed
    assert _linkedin.SESSION_ALREADY_EXISTS == False, \
        "LinkedInTest.py LinkedIn.SESSION_ALREADY_EXISTS' should be equal to True after initialisation! test failed " + failed


def test_getters(_linkedin: LinkedIn) -> None:
    assert isinstance(_linkedin.user_email, str), \
        "LinkedInTest.py LinkedIn.user_email must return string type! test failed " + failed
    assert isinstance(_linkedin.user_password, str), \
        "LinkedInTest.py LinkedIn.user_password must return string type! test failed " + failed

    global user_email
    global user_password

    assert _linkedin.user_email == user_email, \
        "LinkedInTest.py LinkedIn.user_email must be equal to the given user email! test failed " + failed
    assert _linkedin.user_password == user_password, \
        "LinkedInTest.py LinkedIn.user_password must be equal to the given user password! test failed " + failed


def test_setters(_linkedin: LinkedIn) -> None:
    _linkedin.user_email = "xxx-xxx-xxx"

    assert isinstance(_linkedin.user_email, str), \
        "LinkedInTest.py LinkedIn.user_email must set a string type! test failed " + failed
    assert _linkedin.user_email == "xxx-xxx-xxx", \
        "LinkedInTest.py LinkedIn.user_email must set user email to the given user email! test failed " + failed

    global user_email
    _linkedin.user_email = user_email

    _linkedin.user_password = "xxx-xxx-xxx"

    assert isinstance(_linkedin.user_password, str), \
        "LinkedInTest.py LinkedIn.user_password must set a string type! test failed " + failed
    assert _linkedin.user_password == "xxx-xxx-xxx", \
        "LinkedInTest.py LinkedIn.user_password must set user password to the given user password! test failed " + failed

    global user_password
    _linkedin.user_password = user_password


def test_get_chrome_driver_options_method(_linkedin: LinkedIn) -> None:
    _linkedin.set_headless()
    _linkedin.set_browser_incognito_mode()
    _linkedin.set_ignore_certificate_error()

    assert isinstance(_linkedin.get_chrome_driver_options(), Options), \
        "LinkedInTest.py LinkedIn.get_chrome_driver_options method must return list type! test failed " + failed


def test_linkedin() -> list:
    LinkedInTestNumber = 0
    LinkedInTestFailed = 0
    LinkedInTestSuccess = 0

    try:
        test_initial_state()
        printGreen(
            "LinkedInTest.py initial state test passed " + passed, style='b')
        LinkedInTestSuccess += 1
    except AssertionError as error:
        printRed(error)
        LinkedInTestFailed += 1
    finally:
        LinkedInTestNumber += 1

    global user_email
    global user_password
    global driver_path

    _linkedin = LinkedIn(
        {"user_email": user_email, "user_password": user_password}, driver_path=driver_path)

    try:
        test_after_initialisation(_linkedin)
        printGreen(
            "LinkedInTest.py after initial state test passed " + passed, style='b')
        LinkedInTestSuccess += 1
    except AssertionError as error:
        printRed(error)
        LinkedInTestFailed += 1
    finally:
        LinkedInTestNumber += 1

    try:
        test_getters(_linkedin)
        printGreen(
            "LinkedInTest.py test getter methods passed " + passed, style='b')
        LinkedInTestSuccess += 1
    except AssertionError as error:
        printRed(error)
        LinkedInTestFailed += 1
    finally:
        LinkedInTestNumber += 1

    try:
        test_setters(_linkedin)
        printGreen(
            "LinkedInTest.py test setter methods passed " + passed, style='b')
        LinkedInTestSuccess += 1
    except AssertionError as error:
        printRed(error)
        LinkedInTestFailed += 1
    finally:
        LinkedInTestNumber += 1

    try:
        test_get_chrome_driver_options_method(_linkedin)
        printGreen(
            "LinkedInTest.py test for chrome driver options passed " + passed, style='b')
        LinkedInTestSuccess += 1
    except AssertionError as error:
        printRed(error)
        LinkedInTestFailed += 1
    finally:
        LinkedInTestNumber += 1

    return [LinkedInTestNumber, LinkedInTestSuccess, LinkedInTestFailed]

"""from __future__ imports must occur at the beginning of the file. DO NOT CHANGE!"""
from __future__ import annotations

import json

from . import passed
from . import failed

from console.print import printRed
from console.print import printBlue
from console.print import printGreen

from linkedin.linkedin import LinkedIn
from linkedin.linkedinconnectionsauto import LinkedInConnectionsAuto


user_email = ''
user_password = ''
driver_path = ''

with open("/Python/linkedin-bot/linkedin-bot/tests/creds/creds.json") as _file:
    creds = json.load(_file)

    user_email = creds["user_email"]
    user_password = creds["user_password"]
    driver_path = creds["driver_path"]


def test_initial_state(_linkedin_connections_auto: LinkedInConnectionsAuto) -> None:
    assert _linkedin_connections_auto.SENT_INVITATION == 0, \
        "tests/linkedinconnectionsautotest.py _linkedin_connections_auto.SENT_INVITATION must be 0! Test failed " + failed
    assert _linkedin_connections_auto._limit == 40, \
        "tests/linkedinconnectionsautotest.py _linkedin_connections_auto._limit must be 40! Test failed " + failed


def test_linkedin_connections_auto() -> list:
    LinkedInConnectionsAutoTestNumber = 0
    LinkedInConnectionsAutoTestFailed = 0
    LinkedInConnectionsAutoTestSuccess = 0

    global user_email
    global user_password
    global driver_path

    _linkedin = LinkedIn(
        {"user_email": user_email, "user_password": user_password}, driver_path=driver_path)

    _linkedin.set_headless()
    _linkedin.set_browser_incognito_mode()
    _linkedin.set_ignore_certificate_error()

    _linkedin.enable_webdriver_chrome(_linkedin.get_chrome_driver_options())

    _linkedin_connections_auto = LinkedInConnectionsAuto(_linkedin, 40)

    try:
        printBlue(
            "tests/linkedinconnectionsautotest.py initial state testing ...", style='b', end='\r')
        test_initial_state(_linkedin_connections_auto)
        print(' '*80, end='\r')
        printGreen(
            "tests/linkedinconnectionsautotest.py initial state passed " + passed, style='b')
        LinkedInConnectionsAutoTestSuccess += 1
    except AssertionError as error:
        printRed(error)
        LinkedInConnectionsAutoTestFailed += 1
    finally:
        LinkedInConnectionsAutoTestNumber += 1

    return [LinkedInConnectionsAutoTestNumber, LinkedInConnectionsAutoTestSuccess, LinkedInConnectionsAutoTestFailed]

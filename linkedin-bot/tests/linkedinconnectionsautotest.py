"""from __future__ imports must occur at the beginning of the file. DO NOT CHANGE!"""
from __future__ import annotations

import json

from . import passed
from . import failed

from console.print import printRed
from console.print import printBlue
from console.print import printGreen

from selenium.webdriver.remote.webelement import WebElement

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


def test_method_encode(_linkedin_connections_auto: LinkedInConnectionsAuto) -> None:
    person_name = [
        "Ayush Joshi", "Nikhil Negi", "Aryan Bisht", "Aman Bisht", "Mohika Negi",
        "Priya Negi", "Himanshi Rawat", "Adarsh Negi", "Abhinav Chandra"]
    person_occupation = [
        "Software Developer", "Pharmacist", "Software Developer", "Civil Engineer",
        "Doctor", "Mathematician", "Doctor", "Mechanical Engineer", "Mechanical Engineer"]
    person_button = [
        WebElement, WebElement, WebElement, WebElement,
        WebElement, WebElement, WebElement, WebElement, WebElement]

    expected_result = [
        {
            "person_name": "Ayush Joshi",
            "person_occupation": "Software Developer",
            "invite_button": WebElement
        },
        {
            "person_name": "Nikhil Negi",
            "person_occupation": "Pharmacist",
            "invite_button": WebElement
        },
        {
            "person_name": "Aryan Bisht",
            "person_occupation": "Software Developer",
            "invite_button": WebElement
        },
        {
            "person_name": "Aman Bisht",
            "person_occupation": "Civil Engineer",
            "invite_button": WebElement
        },
        {
            "person_name": "Mohika Negi",
            "person_occupation": "Doctor",
            "invite_button": WebElement
        },
        {
            "person_name": "Priya Negi",
            "person_occupation": "Mathematician",
            "invite_button": WebElement
        },
        {
            "person_name": "Himanshi Rawat",
            "person_occupation": "Doctor",
            "invite_button": WebElement
        },
        {
            "person_name": "Adarsh Negi",
            "person_occupation": "Mechanical Engineer",
            "invite_button": WebElement
        },
        {
            "person_name": "Abhinav Chandra",
            "person_occupation": "Mechanical Engineer",
            "invite_button": WebElement
        }]

    actual_result = _linkedin_connections_auto.encode(
        [person_name, person_occupation, person_button])

    assert len(expected_result) == len(actual_result), \
        "tests/linkedinconnectionsautotest.py expected results and actual results must have equal lengths! Test failed " + failed

    passed = False

    for person in actual_result:
        for expected_person in expected_result:
            if person["person_name"] == expected_person["person_name"] \
                    and person["person_occupation"] == expected_person["person_occupation"] \
                    and person["invite_button"] == expected_person["invite_button"]:
                passed = True
                break

        assert passed, \
            f"tests/linkedinconnectionsautotest.py {person['person_name']}, {person['person_occupation']}, WebElement does not exist in expected results! Test failed " + failed

        passed = False


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

    try:
        printBlue(
            "tests/linkedinconnectionsautotest.py encode method testing ...", style='b', end='\r')
        test_method_encode(_linkedin_connections_auto)
        print(' '*80, end='\r')
        printGreen(
            "tests/linkedinconnectionsautotest.py encode method passed " + passed, style='b')
        LinkedInConnectionsAutoTestSuccess += 1
    except AssertionError as error:
        printRed(error)
        LinkedInConnectionsAutoTestFailed += 1
    finally:
        LinkedInConnectionsAutoTestNumber += 1

    return [LinkedInConnectionsAutoTestNumber, LinkedInConnectionsAutoTestSuccess, LinkedInConnectionsAutoTestFailed]

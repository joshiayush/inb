"""from __future__ imports must occur at the beginning of the file. DO NOT CHANGE!"""
from __future__ import annotations

import json
import unittest

from .. import failed
from .. import message

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


_linkedin = LinkedIn(
    {"user_email": user_email, "user_password": user_password}, driver_path=driver_path)

_linkedin.set_headless()
_linkedin.set_browser_incognito_mode()
_linkedin.set_ignore_certificate_error()

_linkedin.enable_webdriver_chrome(
    _linkedin.get_chrome_driver_options())

_linkedin_connections_auto = LinkedInConnectionsAuto(_linkedin, 40)


class TestLinkedInConnectionsAuto(unittest.TestCase):

    def test_initial_state(self: TestLinkedInConnectionsAuto) -> None:
        """Method test_initial_state() tests the initial state of the newly constructed object.

        :Args:
            - self: {LinkedInConnectionsAuto} class object

        :Returns:
            - {None}
        """
        self.assertEqual(_linkedin_connections_auto.SENT_INVITATION, 0, message(
            f"_linkedin_connections_auto.SENT_INVITATION must be 0! Test failed {failed}", 'r'))
        self.assertEqual(_linkedin_connections_auto._limit, 40, message(
            f"_linkedin_connections_auto._limit must be 40! Test failed {failed}", 'r'))

    def test_encode(self: TestLinkedInConnectionsAuto) -> None:
        """Method test_encode() checks if the encode method of class LinkedInConnectionsAuto works
        fine or not by giving a bunch of data to that method and checking the results if found suspicious
        it asserts the problem.

        :Args:
            - self: {LinkedInConnectionsAuto} class object

        :Returns:
            - {None}
        """
        person_name = [
            "Ayush Joshi", "Nikhil Negi", "Aryan Bisht", "Aman Bisht", "Mohika Negi", "Priya Negi", "Himanshi Rawat", "Adarsh Negi",
            "Abhinav Chandra", "Abhishek Rawat", "Gaurav Chaudhry", "Mayank Aswal"]
        person_occupation = [
            "Software Developer", "Pharmacist", "Software Developer", "Civil Engineer", "Doctor", "Mathematician", "Doctor",
            "Mechanical Engineer", "Mechanical Engineer", "Mechanical Engineer", "Engineer", "Financer"]
        person_button = [
            WebElement, WebElement, WebElement, WebElement, WebElement, WebElement, WebElement, WebElement, WebElement, WebElement,
            WebElement, WebElement]

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
            },
            {
                "person_name": "Abhishek Rawat",
                "person_occupation": "Mechanical Engineer",
                "invite_button": WebElement
            },
            {
                "person_name": "Gaurav Chaudhry",
                "person_occupation": "Engineer",
                "invite_button": WebElement
            },
            {
                "person_name": "Mayank Aswal",
                "person_occupation": "Financer",
                "invite_button": WebElement
            }]

        actual_result = _linkedin_connections_auto.encode(
            [person_name, person_occupation, person_button])

        self.assertEqual(len(expected_result), len(actual_result), message(
            f"expected results and actual results must have equal lengths! Test failed {failed}", 'r'))

        # actually we first sort both the lists containing the expected and actual results and then
        # do a equality check.
        self.assertTrue(sorted(
            expected_result, key=lambda item: item["person_name"]) == sorted(actual_result, key=lambda item: item["person_name"]),
            message(f"There is a value that doesn't match! Test failed {failed}", 'r'))

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

import logging
import argparse

from typing import List

from console.print import inbprint

from errors import EmptyResponseException
from errors import DomainNameSystemNotResolveException

from linkedin import Driver

from linkedin.linkedin import LinkedIn
from linkedin.linkedinconnect import LinkedInConnect
from linkedin.linkedinsearchconnect import LinkedInSearchConnect

from . import DRIVER_PATH
from .commandhelper import CommandAide


class Command(CommandAide):

    def __init__(self: Command, namespace: argparse.Namespace) -> None:
        super().__init__(namespace=namespace)

    def send(self: Command) -> None:
        chrome_driver_options: List[str] = []

        chrome_driver_options.append(Driver.INCOGNITO)
        chrome_driver_options.append(Driver.IGNORE_CERTIFICATE_ERRORS)
        if self.headless == True:
            chrome_driver_options.append(Driver.HEADLESS)

        linkedin = LinkedIn(user_email=self.email,
                            user_password=self.password,
                            driver_path=DRIVER_PATH,
                            opt_chromedriver_options=chrome_driver_options)

        logging.basicConfig(format="%(levelname)s:%(message)s", level=logging.INFO)
        logging.info("Connecting")
        try:
            logging.info("Sending GET request to login page")
            linkedin.get_login_page()
            logging.info("Connected to login page")
        except DomainNameSystemNotResolveException as error:
            logging.critical(error)
            return

        logging.info("Logging in LinkedIn account (user-id=%(user_id)s)" %
                     {"user_id": self.email})
        linkedin.login()
        logging.info("Successfully connected")

        logging.info("Instantiating connection object")
        linkedin_connection = LinkedInConnect(driver=linkedin.driver,
                                              limit=self.limit)

        try:
            logging.info("Sending GET request to mynetwork page")
            linkedin_connection.get_my_network()
            logging.info("Successfully connected to mynetwork page")
        except EmptyResponseException as error:
            logging.critical(error)
            return

        logging.info("Starting sending invitation")
        linkedin_connection.run()

    def search(self: Command) -> None:
        _chrome_driver_options: list = []

        _chrome_driver_options.append(Driver.INCOGNITO)
        _chrome_driver_options.append(Driver.IGNORE_CERTIFICATE_ERRORS)

        if self.headless == True:
            _chrome_driver_options.append(Driver.HEADLESS)

        _linkedin = LinkedIn(user_email=self.email,
                             user_password=self.password,
                             driver_path=DRIVER_PATH,
                             opt_chromedriver_options=_chrome_driver_options)

        inbprint("Connecting ...", color="cyan", blink=True, end="\r")

        try:
            _linkedin.get_login_page()
        except DomainNameSystemNotResolveException as exc:
            inbprint(' '*80, end='\r')
            inbprint(f"{exc}", color="red", bold=True)
            return

        _linkedin.login()

        inbprint(' '*80, end='\r')
        inbprint(f"Connected ✔", color="green", bold=True)

        _linkedin_search_connect = LinkedInSearchConnect(driver=_linkedin.driver,
                                                         keyword=self.keyword,
                                                         location=self.location,
                                                         title=self.title,
                                                         first_name=self.first_name,
                                                         last_name=self.last_name,
                                                         school=self.school,
                                                         industry=self.industry,
                                                         current_company=self.current_company,
                                                         profile_language=self.profile_language,
                                                         limit=self.limit)
        _linkedin_search_connect.run()

    def show(self: Command) -> None:
        """Show the table formed by the CommandHelper() class."""
        pass

    def config(self: Command) -> None:
        """Throw the email and password in the database."""

        """Ask user to enter its email and password."""
        pass

    def delete(self: Command) -> None:
        """Delete the given value from the database."""

        """Check what the user wants to delete."""

        """Delete information from the database."""

        """Dump database if user wants so."""
        pass

    def developer(self: Command) -> None:
        """Show developer details."""

        """Check what flag is passed and then throw the information"""

        """Print every information if no flag is used."""
        pass

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

import sys
import json

from typing import Union
from typing import TextIO

import re
from selenium import webdriver


class Path_To_Element_By(object):
    SUGGESTION_BOX_ELEMENT_XPATH: str = \
        """/html/body/div[6]/div[3]/div/div/div/div/div[2]/div/div/main/div[2]/section/section/section/div/ul/li[1]"""
    SEARCH_RESULTS_PEOPLE_XPATH: str = """//*[@id="main"]/div/div/div[2]/ul/li[1]"""


class Person_Info(object):
    """Class Person_Info provides an object with person's necessary details fetched
    from linkedin's page.
    """

    def __init__(
            self: Person_Info,
            name: Union[str, None] = None,
            occupation: Union[str, None] = None,
            profile_url: Union[str, None] = None,
            photo_url: Union[str, None] = None,
            location: Union[str, None] = None,
            summary: Union[str, None] = None,
            connect_button: Union[webdriver.Chrome, None] = None
    ) -> None:
        """Constructor method initializes the Person_Info object with basic details
        about the person.

        :Args:
            - self: {Person_Info} self.
            - name: {str} person's name.
            - occupation: {str} person's occupation.
            - profile_url: {str} person's linkedin profile url.
            - photo_url: {str} person's linkedin profile photo url.
            - connect_button: {webdriver.Chrome} person's connect button instance.
        """
        self.name = name
        self.occupation = occupation
        self.profile_url = profile_url
        if "?" in photo_url:
            self.photo_url = photo_url.split("?")[0]
        else:
            self.photo_url = photo_url
        self.connect_button = connect_button
        self.location = location
        self.summary = summary
        self.id = self.person_id()

    def person_id(self: Person_Info) -> str:
        """Method person_id() returns the person id filtering the person's profile url.

        :Args:
            - self: {Person_Info} self.

        :Returns:
            - {str} person id.
        """
        _re = re.compile(r"([a-z]+-?)+([a-zA-Z0-9]+)?", re.IGNORECASE)
        return _re.search(self.profile_url)

    def freeze(
        self: Person_Info,
        file: Union[str, TextIO] = sys.stdout,
        mode: str = "w",
        _format: str = None
    ) -> None:
        """Method freeze() dumps the current object state in the given file in the given format.

        :Args:
            - self: {Person_Info} self.
            - file: {Union[str, TextIO]} file to dump the current object state in.
            - mode: {str} in what mode to open the file in.
            - _format: {str} in what format to write the data in.

        :Raises:
            - {Exception} if the format and the file is not identified.
        """
        message = ''

        if _format == "json":
            message = json.dump({
                "name": self.name,
                "person_id": self._person_id,
                "occupation": self.occupation,
                "profile_url": self.profile_url,
                "photo_url": self.photo_url,
                "location": self.location,
                "summary": self.summary
            })
        elif _format == "raw":
            message = ("name: %(name)s\n" +
                       "person_id: %(person_id)s\n" +
                       "occupation: %(occupation)s\n" +
                       "profile_url: %(profile_url)s\n" +
                       "photo_url: %(photo_url)s\m" +
                       "location: %(location)s\n" +
                       "summary: %(summary)s") % {
                "name": self.name,
                "person_id": self._person_id,
                "occupation": self.occupation,
                "profile_url": self.profile_url,
                "photo_url": self.photo_url,
                "location": self.location,
                "summary": self.summary}
        else:
            raise Exception("Format '%(frmt)s' is not supported!" %
                            {"frmt": _format})

        if isinstance(file, str):
            with open(file=file, mode=mode) as file:
                if file.endswith(".json"):
                    json.dump(message, file, indent=2)
                else:
                    file.write(message)
            return
        elif file == sys.stdout:
            file.write(message)
        else:
            raise Exception("File '%(file)s' is not supported!" %
                            {"file": file})

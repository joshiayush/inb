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

from selenium import webdriver


class Path_To_Element_By(object):
    SUGGESTION_BOX_ELEMENT_XPATH: str = \
        """/html/body/div[6]/div[3]/div/div/div/div/div[2]/div/div/main/div[2]/section/section/section/div/ul/li[1]"""
    SEARCH_RESULTS_PEOPLE_XPATH: str = """//*[@id="main"]/div/div/div[2]/ul/li[1]"""


class Person_Info(object):
    """Class Person_Info provides an object with person's necessary details fetched
    from linkedin's page.
    """
    BASE_LINKEDIN_URL: str = "https://www.linkedin.com"

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
        self._name = name
        self._occupation = occupation
        self._profile_url = profile_url
        if "?" in photo_url:
            self._photo_url = photo_url.split("?")[0]
        else:
            self._photo_url = photo_url
        self._connect_button = connect_button
        self._location = location
        self._summary = summary
        # type: bug
        # self._person_id = self.person_id()

    def person_id(self: Person_Info) -> str:
        """Method person_id() returns the person id filtering the person's profile url.

        :Args:
            - self: {Person_Info} self.

        :Returns:
            - {str} person id.
        """
        _url_base: str = self.BASE_LINKEDIN_URL + "/in/"
        _indx: int = self._profile_url.find(_url_base) + len(_url_base)

        _profile_url: str = self._profile_url

        while not _profile_url[_indx] == '/':
            _indx += 1
        _indx -= 1

        _id: str = ''
        while not _profile_url[_indx] == '-' and not _profile_url[_indx] == '/':
            _id += _profile_url[_indx]
            _indx -= 1

        return _id[::-1]

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
        _message: str = ''

        if _format == "json":
            _message = json.dump({
                "name": self._name,
                "person_id": self._person_id,
                "occupation": self._occupation,
                "profile_url": self._profile_url,
                "photo_url": self._photo_url,
                "location": self._location,
                "summary": self._summary
            })
        elif _format == "raw":
            _message = ("name: %(name)s\n" +
                        "person_id: %(person_id)s\n" +
                        "occupation: %(occupation)s\n" +
                        "profile_url: %(profile_url)s\n" +
                        "photo_url: %(photo_url)s\m" +
                        "location: %(location)s\n" +
                        "summary: %(summary)s") % {
                "name": self._name,
                "person_id": self._person_id,
                "occupation": self._occupation,
                "profile_url": self._profile_url,
                "photo_url": self._photo_url,
                "location": self._location,
                "summary": self._summary}
        else:
            raise Exception("Format '%(frmt)s' is not supported!" %
                            {"frmt": _format})

        if isinstance(file, str):
            with open(file=file, mode=mode) as file:
                if file.endswith(".json"):
                    json.dump(_message, file, indent=2)
                else:
                    file.write(_message)
            return
        elif file == sys.stdout:
            file.write(_message)
        else:
            raise Exception("File '%(file)s' is not supported!" %
                            {"file": file})

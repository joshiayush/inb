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

# from __future__ imports must occur at the beginning of the file. DO NOT CHANGE!
from __future__ import annotations

import logging
import argparse

from . import _type
from .command import Command


class Handler(object):
    def __init__(self: Handler, namespace: argparse.Namespace) -> None:
        """Constructor method initializes the logging object and the namespace object.

        :Args:
            - self: {Handler} self.
            - namespace: {argparse.Namespace} Argparse namespace.

        :Returns:
            - {None}

        :Raises:
            - {ValueError} If namespace given is None.
        """
        self.logger = logging.getLogger("inb")
        logging.basicConfig(
            format="%(levelname)s:%(message)s", level=logging.INFO)
        self.logger.setLevel(logging.DEBUG)

        if namespace:
            self.logger.debug("Handler: namespace OK")
            self.namespace = namespace
        else:
            raise ValueError("Handler: Namespace is a %(type)s object" % {
                             "type": _type(namespace)})

    def handle_command(self: Handler) -> None:
        """Method handle_command() handles the commands given by the user.

        :Args:
            - self: {Handler} self.

        :Returns:
            - {None}
        """
        if self.namespace.which == "send":
            try:
                Command(self.namespace).send()
            except Exception as e:
                self.logger.error(e)
                raise e
            return

        if self.namespace.which == "search":
            try:
                Command(self.namespace).search()
            except Exception as exc:
                raise exc
            return

        if self.namespace.which == "show":
            try:
                Command(self.namespace).show()
            except Exception as e:
                raise e
            return

        if self.namespace.which == "config":
            try:
                Command(self.namespace).config()
            except Exception as e:
                raise e
            return

        if self.namespace.which == "delete":
            try:
                Command(self.namespace).delete()
            except Exception as e:
                raise e
            return

        if self.namespace.which == "developer":
            try:
                Command(self.namespace).developer()
            except Exception as e:
                raise e
            return

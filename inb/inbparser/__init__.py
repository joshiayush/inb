"""
This module provides service to call methods according to the action selected
by the user.

Supported Actions
~~~~~~~~~~~~~~~~~

  - send                Sends invitation to people on linkedin.
  - connect             Connects you with the given profile.
  - search              Searches people on LinekdIn and then invites them.
  - config              Used to store user's credentials
  - show                Prints the information that is in the database
  - delete              Deletes the information stored in the database
  - developer           Prints the information about the author

  :author: Ayush Joshi, ayush854032@gmail.com
  :copyright: Copyright (c) 2019 Creative Commons
  :license: MIT License, see license for details
"""

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

import argparse

from inbparser.command import Command


class Parser:
  """Class `Parser` binds the actions specified by the user over the cli to the
  corresponding method calls.
  """

  def __init__(self: Parser, namespace: argparse.Namespace) -> None:
    """Constructor method initializes the logging object and the namespace object.

    Args:
      self: (Parser) Self.
      namespace: (argparse.Namespace) Argparse namespace.

    Raises:
      Exception: If namespace given is None.

    Example:
    >>> from argparse import Namespace
    >>> from inbparser import parser
    >>>
    >>> namespace = Namespace(which='send', email='email@gmail.com', password='xxx-xxx-xxx')
    >>> parser = Parser(namespace)
    """
    if namespace:
      self.namespace = namespace
    else:
      raise Exception("Namespace is not given!")

  def parse(self: Parser) -> None:
    """Method `parse()` handles the commands given by the user.

    Args:
      self: (Parser) Self.

    Example:
    >>> from argparse import Namespace
    >>> from inbparser import parser
    >>>
    >>> namespace = Namespace(which='send', email='email@gmail.com', password='xxx-xxx-xxx')
    >>> parser = Parser(namespace)
    >>> parser.parse() # This will call the send() method
    """
    if self.namespace.which == "send":
      Command(self.namespace).send()
    elif self.namespace.which == "search":
      Command(self.namespace).search()
    elif self.namespace.which == "show":
      Command(self.namespace).show()
    elif self.namespace.which == "config":
      Command(self.namespace).config()
    elif self.namespace.which == "delete":
      Command(self.namespace).delete()
    elif self.namespace.which == "developer":
      Command(self.namespace).developer()

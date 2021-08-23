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

import argparse

from .command import Command


def CommandHandler(namespace: argparse.Namespace) -> None:
    if namespace.which == "send":
        try:
            Command(namespace).send()
        except Exception as e:
            raise e
        return

    if namespace.which == "show":
        try:
            Command(namespace).show()
        except Exception as e:
            raise e
        return

    if namespace.which == "config":
        try:
            Command(namespace).config()
        except Exception as e:
            raise e
        return

    if namespace.which == "delete":
        try:
            Command(namespace).delete()
        except Exception as e:
            raise e
        return

    if namespace.which == "developer":
        try:
            Command(namespace).developer()
        except Exception as e:
            raise e
        return

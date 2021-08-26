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

from typing import Any
from typing import Tuple

from lib.utils import _type
from lib.utils.validator import Validator


class EmptyResponseException(Exception):
    """Thrown when recieved an empty response."""

    def __init__(self: EmptyResponseException, *args: Tuple[Any]) -> None:
        super(EmptyResponseException, self).__init__(*args)
        if args:
            if isinstance(args[0], str):
                self.message = args[0]
            else:
                raise Exception(
                    "EmptyResponseException: Constructor's first argument must be of type 'str' not '%(type)s'" % {
                        "type": _type(args[0])})
        else:
            self.message = None

    def __str__(self: EmptyResponseException) -> str:
        if self.message:
            return "EmptyResponseException: %(message)s" % {"message": self.message}
        else:
            return "EmptyResponseException has been raised!"


class FailedLoadingResourceException(Exception):
    """Thrown when failed loading the resources properly."""

    def __init__(self: FailedLoadingResourceException, *args: Tuple[Any]) -> None:
        super(FailedLoadingResourceException, self).__init__(*args)
        if args:
            if isinstance(args[0], str):
                self.message = args[0]
            else:
                raise Exception(
                    "FailedLoadingResourceException: Constructor's first argument must be of type 'str' not '%(type)s'" % {
                        "type": _type(args[0])})
        else:
            self.message = None

    def __str__(self: FailedLoadingResourceException) -> str:
        if self.message:
            return "FailedLoadingResourceException: %(message)s" % {"message": self.message}
        else:
            return "FailedLoadingResourceException has been raised!"


class LinkedInBlockException(Exception):
    """Thrown when LinkedIn blocks."""

    def __init__(self: LinkedInBlockException, *args: Tuple[Any]) -> None:
        super(LinkedInBlockException, self).__init__(*args)
        if args:
            if isinstance(args[0], str):
                self.message = args[0]
            else:
                raise Exception(
                    "LinkedInBlockException: Constructor's first argument must be of type 'str' not '%(type)s'" % {
                        "type": _type(args[0])})
        else:
            self.message = None

    def __str__(self: LinkedInBlockException) -> str:
        if self.message:
            return "LinkedInBlockException: %(message)s" % {"message": self.message}
        else:
            return "LinkedInBlockException has been raised!"


class DomainNameSystemNotResolveException(Exception):
    """Thrown when DNS could not be resolved."""

    def __init__(self: DomainNameSystemNotResolveException, *args: Tuple[Any]) -> None:
        super(DomainNameSystemNotResolveException, self).__init__(*args)
        if args:
            if isinstance(args[0], str):
                self.message = args[0]
            else:
                raise Exception(
                    "DomainNameSystemNotResolveException: Constructor's first argument must be of type 'str' not '%(type)s'" % {
                        "type": _type(args[0])})
            if len(args) > 1:
                if isinstance(args[1], str):
                    if Validator(args[1]).is_url():
                        self.url = args[1]
                    else:
                        raise ValidationError("DomainNameSystemNotResolveException: [URL] (%(url)s) is not a valid url!" % {
                            "url": args[1]})
                else:
                    raise Exception(
                        "DomainNameSystemNotResolveException: Constructor's second argument"
                        " (url) must be of type 'str' not '%(type)s'" % {
                            "type": _type(args[1])})
        else:
            self.message = None
            self.url = None

    def __str__(self: DomainNameSystemNotResolveException) -> str:
        if self.message and self.url:
            return "DomainNameSystemNotResolveException: %(message)s\n[URL] %(url)s" % {
                "message": self.message, "url": self.url}
        elif self.message:
            return "DomainNameSystemNotResolveException: %(message)s" % {"message": self.message}
        else:
            return "DomainNameSystemNotResolveException has been raised!"


class WebDriverPathNotGivenException(Exception):
    """Thrown when chrome driver's path is not given."""

    def __init__(self: WebDriverPathNotGivenException, *args: Tuple[Any]) -> None:
        super(WebDriverNotExecutableException, self).__init__(*args)
        if args:
            if isinstance(args[0], str):
                self.message = args[0]
            else:
                raise Exception(
                    "WebDriverNotExecutableException: Constructor's first argument must be of type 'str' not '%(type)s'" % {
                        "type": _type(args[0])})
        else:
            self.message = None

    def __str__(self: WebDriverNotExecutableException) -> str:
        if self.message:
            return "WebDriverNotExecutableException: %(message)s" % {"message": self.message}
        else:
            return "WebDriverNotExecutableException has been raised!"


class WebDriverNotExecutableException(Exception):
    """Thrown when chrome driver's path is not given."""

    def __init__(self: WebDriverNotExecutableException, *args: Tuple[Any]) -> None:
        super(WebDriverNotExecutableException, self).__init__(*args)
        if args:
            if isinstance(args[0], str):
                self.message = args[0]
            else:
                raise Exception(
                    "WebDriverNotExecutableException: Constructor's first argument must be of type 'str' not '%(type)s'" % {
                        "type": _type(args[0])})
        else:
            self.message = None

    def __str__(self: WebDriverNotExecutableException) -> str:
        if self.message:
            return "WebDriverNotExecutableException: %(message)s" % {"message": self.message}
        else:
            return "WebDriverNotExecutableException has been raised!"


class CredentialsNotGivenException(Exception):
    """Thrown when user's credentials are not given to the LinkedIn class."""

    def __init__(self: CredentialsNotGivenException, *args: Tuple[Any]) -> None:
        super(CredentialsNotGivenException, self).__init__(*args)
        if args:
            if isinstance(args[0], str):
                self.message = args[0]
            else:
                raise Exception(
                    "CredentialsNotGivenException: Constructor's first argument must be of type 'str' not '%(type)s'" % {
                        "type": _type(args[0])})
            if len(args) > 1:
                if isinstance(args[1], dict):
                    self.credentials_dict = args[1]
                    if not "user_email" in args[1] or not "user_password" in args[1]:
                        raise KeyError(
                            "CredentialsNotGivenException: Constructor's second argument's mapping key"
                            " 'user_email' or 'user_password' not found!")
                else:
                    raise Exception(
                        "CredentialsNotGivenException: Constructor's second argument"
                        " (credentials dictionary) must be of type 'dict' not '%(type)s'" % {
                            "type": _type(args[0])})
        else:
            self.message = None
            self.credentials_dict = None

    def __str__(self: CredentialsNotGivenException) -> str:
        if self.message and self.credentials_dict:
            return ("CredentialsNotGivenException: %(message)s\n"
                    "[credentials] {'user_email': %(user_email)s, 'user_password': %(user_password)s}") % {
                "message": self.message, "user_email": _type(self.credentials_dict["user_email"]),
                "user_password": _type(self.credentials_dict["user_password"])}
        elif self.message:
            return "CredentialsNotGivenException: %(message)s" % {"message": self.message}
        else:
            return "CredentialsNotGivenException has been raised!"


class ConnectionLimitExceededException(Exception):
    """Thrown when connections limit given by the user exceeds."""

    def __init__(self: ConnectionLimitExceededException, *args: Tuple[Any]) -> None:
        super(ConnectionLimitExceededException, self).__init__(*args)
        if args:
            if isinstance(args[0], str):
                self.message = args[0]
            else:
                raise Exception(
                    "ConnectionLimitExceededException: Constructor's first argument must be of type 'str' not '%(type)s'" % {
                        "type": _type(args[0])})
        else:
            self.message = None

    def __str__(self: ConnectionLimitExceededException) -> str:
        if self.message:
            return "ConnectionLimitExceededException: %(message)s" % {"message": self.message}
        else:
            return "ConnectionLimitExceededException has been raised!"


class DatabaseDoesNotExistException(Exception):
    """Thrown when database does not exist to perform read/write operations."""

    def __init__(self: DatabaseDoesNotExistException, *args: Tuple[Any]) -> None:
        super(DatabaseDoesNotExistException, self).__init__(*args)
        if args:
            if isinstance(args[0], str):
                self.message = args[0]
            else:
                raise Exception(
                    "DatabaseDoesNotExistException: Constructor's first argument must be of type 'str' not '%(type)s'" % {
                        "type": _type(args[0])})
            if len(args) > 1:
                if isinstance(args[1], str):
                    self.database_path = args[1]
                else:
                    raise Exception(
                        "DatabaseDoesNotExistException: Constructor's second argument "
                        "(database path) must be of type 'str' not '%(type)s'" % {
                            "type": _type(args[0])})
        else:
            self.message = None
            self.database_path = None

    def __str__(self: DatabaseDoesNotExistException) -> str:
        if self.message and self.database_path:
            return "DatabaseDoesNotExistException: %(message)s\n[database path] %(database_path)s" % {
                "message": self.message, "database_path": self.database_path}
        elif self.message:
            return "DatabaseDoesNotExistException: %(message)s" % {"message": self.message}
        else:
            return "DatabaseDoesNotExistException has been raised!"


class EmtpyDatabaseException(Exception):
    """Thrown when email and password are requested and database is empty."""

    def __init__(self: EmtpyDatabaseException, *args: Tuple[Any]) -> None:
        super(EmtpyDatabaseException, self).__init__(*args)
        if args:
            if isinstance(args[0], str):
                self.message = args[0]
            else:
                raise Exception(
                    "EmtpyDatabaseException: Constructor's first argument must be of type 'str' not '%(type)s'" % {
                        "type": _type(args[0])})
            if len(args) > 1:
                if isinstance(args[1], str):
                    self.database_path = args[1]
                else:
                    raise Exception(
                        "EmtpyDatabaseException: Constructor's second argument "
                        "(database path) must be of type 'str' not '%(type)s'" % {
                            "type": _type(args[0])})
        else:
            self.message = None
            self.database_path = None

    def __str__(self: EmtpyDatabaseException) -> str:
        if self.message and self.database_path:
            return "EmptyDatabaseException: %(message)s\n[database path] %(database_path)s" % {
                "message": self.message, "database_path": self.database_path}
        elif self.message:
            return "EmptyDatabaseException: %(message)s" % {"message": self.message}
        else:
            return "EmptyDatabaseException has been raised!"


class ValidationError(Exception):
    def __init__(self: ValidationError, *args: Tuple[Any]) -> None:
        super(ValidationError, self).__init__(*args)
        if args:
            if isinstance(args[0], str):
                self.message = args[0]
            else:
                raise Exception(
                    "ValidationError: Constructor's first argument must be of type 'str' not '%(type)s'" % {
                        "type": _type(args[0])})
        else:
            self.message = None

    def __str__(self: ValidationError) -> str:
        if self.message:
            return "ValidationError: %(message)s" % {"message": self.message}
        else:
            return "ValidationError has been raised!"

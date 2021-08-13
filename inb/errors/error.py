# MIT License
#
# Copyright (c) 2019 Creative Commons
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and sell copies
# of the Software, and to permit persons to whom the Software is furnished to do
# so, subject to the following conditions
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

"""from __future__ imports must occur at the beginning of the file. DO NOT CHANGE!"""
from __future__ import annotations


class EmptyResponseException(Exception):
    """Thrown when recieved an empty response."""

    def __init__(self: EmptyResponseException, message: str = '') -> None:
        super(EmptyResponseException, self).__init__(message)


class FailedLoadingResourceException(Exception):
    """Thrown when failed loading the resources properly."""

    def __init__(self: FailedLoadingResourceException, message: str = '') -> None:
        super(FailedLoadingResourceException, self).__init__(message)


class LinkedInBlockException(Exception):
    """Thrown when LinkedIn blocks."""

    def __init__(self: LinkedInBlockException, message: str = '') -> None:
        super(LinkedInBlockException, self).__init__(message)


class DomainNameSystemNotResolveException(Exception):
    """Thrown when DNS could not be resolved."""

    def __init__(self: DomainNameSystemNotResolveException, message: str = '') -> None:
        super(DomainNameSystemNotResolveException, self).__init__(message)


class PropertyNotExistException(Exception):
    """Thrown when a binding does not have a property name."""

    def __init__(self: PropertyNotExistException, message: str = '') -> None:
        super(PropertyNotExistException, self).__init__(message)


class UserCacheNotFoundException(Exception):
    """Thrown when user doesn't have any cache stored."""

    def __init__(self: UserCacheNotFoundException, message: str = '') -> None:
        super(UserCacheNotFoundException, self).__init__(message)


class WebDriverPathNotGivenException(Exception):
    """Thrown when chrome driver's path is not given."""

    def __init__(self: WebDriverPathNotGivenException, message: str = '') -> None:
        super(WebDriverPathNotGivenException, self).__init__(message)


class CredentialsNotGivenException(Exception):
    """Thrown when user's credentials are not given to the LinkedIn class."""

    def __init__(self: CredentialsNotGivenException, message: str = '') -> None:
        super(CredentialsNotGivenException, self).__init__(message)


class ConnectionLimitExceededException(Exception):
    """Thrown when connections limit given by the user exceeds."""

    def __init__(self: ConnectionLimitExceededException, message: str = '') -> None:
        super(ConnectionLimitExceededException, self).__init__(message)


class DatabaseDoesNotExistException(Exception):
    """Thrown when database does not exist to perform read/write operations."""

    def __init__(self: DatabaseDoesNotExistException, message: str = '') -> None:
        super(DatabaseDoesNotExistException, self).__init__(message)


class EmtpyDatabaseException(Exception):
    """Thrown when email and password are requested and database is empty."""

    def __init__(self: EmtpyDatabaseException, message: str = '') -> None:
        super(EmtpyDatabaseException, self).__init__(message)

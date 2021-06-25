"""Module User provides a linkedin user object with various attributes in it."""

from __future__ import annotations


class User(object):
    """Class User to create a user with email and password."""

    def __init__(self: User, email: str = '', password: str = '') -> None:
        self.user_email = email
        self.user_password = password


class UserWithSearchKeywords(User):
    """Class UserWithSearchKeywords to create a user with email and password and search keywords and search location."""

    def __init__(self: UserWithSearchKeywords, email: str = '', password: str = '', keywords: str = '', location: str = '') -> None:
        super(UserWithSearchKeywords, self).__init__(
            email=email, password=password)
        self.search_keywords = keywords
        self.search_location = location


class UserWithJobKeywords(User):
    """Class UserWithJobKeywords to create a user with email and password and job keywords and job location."""

    def __init__(self: UserWithJobKeywords, email: str = '', password: str = '', keywords: str = '', location: str = '') -> None:
        super(UserWithJobKeywords, self).__init__(
            email=email, password=password)
        self.job_keywords = keywords
        self.job_location = location

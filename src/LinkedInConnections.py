"""
From `linkedin` importing `LinkedIn` class, `webdriver`, `Keys`,

`WebdriverWait`, `expected_conditions`, `By`, `NoSuchElementException`,

`ElementClickInterceptedException`, `ActionChains`, `json`, and `re`
"""
from LinkedIn import (
    LinkedIn,
    webdriver,
    Keys,
    WebDriverWait,
    expected_conditions,
    By,
    NoSuchElementException,
    ElementClickInterceptedException,
    ActionChains,
    re
)


class LinkedInConnections(LinkedIn):
    """
    Controls LinkedIn Connections, more functionality will be coded soon.

    Parent:
        LinkedIn: our main LinkedIn class which takes care of enabling of 
        the webdriver and the login process.
    """

    def __init__(self):
        super(LinkedInConnections, self).__init__()

    def find_suggestion_box(self):
        pass

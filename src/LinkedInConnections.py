import time
import operator
import colorama
import functools
import urllib.parse

from LinkedIn import re
from LinkedIn import By
from LinkedIn import Keys
from LinkedIn import LinkedIn
from LinkedIn import webdriver
from LinkedIn import ActionChains
from LinkedIn import WebDriverWait
from LinkedIn import TimeoutException
from LinkedIn import expected_conditions
from LinkedIn import NoSuchElementException
from LinkedIn import ElementClickInterceptedException
from LinkedIn import ElementNotInteractableException


class LinkedInConnections(LinkedIn):

    def __init__(self, _type, data):
        super(LinkedInConnections, self).__init__(data)

    def init_vars(self):
        """Function init_vars() initializes all the variables
        that are required to implement search functionality.
        """
        self.linkedin = "https://www.linkedin.com/"

        self.search = "search/results/"

        self.people = "people/?"

        self.geoUrn = "geoUrn="

        self.__identifiers__ = {
            "india": '%5B"102713980"%5D&',
            "usa": '%5B"103644278"%5D&',
            "california": '%5B"102095887"%5D&',
            "sanfranciscoba": '%5B"90000084"%5D&',
            "sanfranciscoca": '%5B"102277331"%5D&'
        }

        self.location = self.geoUrn + \
            functools.reduce(operator.add, self.__identifiers__.values())

        self.origins = ["SWITCH_SEARCH_VERTICAL", "FACETED_SEARCH"]

        self.keywords = f"""keywords=__key__&origin={self.origins[0]}"""

        self.connections_link = ""

    def get_location_identifier(self, country):

        return self.__identifiers__.get(country, None)

    def quote_url(self, url, safe=f"~@#$&()*!+=:;,.?/\\"):
        """URL-encodes a string (either str (i.e. ASCII) or unicode)
        uses de-facto UTF-8 encoding to handle Unicode codepoints in
        given string.
        """
        return urllib.parse.quote(url.encode('utf-8'), safe)

    def form_connection_link(self):
        """Function form_connection_link() forms a linkedin connections
        link by encoding.
        """
        self.connections_link = self.quote_url(
            self.linkedin + self.search + self.people + self.location + self.keywords + self.origins[0])

        print(self.connections_link)

    def getUrn(self, key):
        Urns = {
            "India": self.get_location_identifier("india"),
            "United States": self.get_location_identifier("usa"),
            "California, United States": self.get_location_identifier("california"),
            "Sanfrancisco Bay Area": self.get_location_identifier("sanfranciscoba"),
            "Sanfrancisco, CA": self.get_location_identifier("sanfranciscoca")
        }

        return Urns[key]

    def apply_keyword(self, keyword):
        """Function apply_keyword() applies keyword to a part of the linkedin
        connections link.
        """
        self.keywords = self.keywords.replace("__key__", keyword[0])

        if (keyword[1] == "All"):
            self.keywords = f"""keywords=__key__&origin={self.origins[1]}"""
        else:
            self.keywords = f"""keywords=__key__&origin={self.origins[1]}"""
            self.location = self.getUrn(keyword[1])

    def get_keywords(self):
        """Function get_keywords() asks the user for the keywords that has to
        be applied when searching for people.
        """
        keyword = input("Enter Connection Keywords: ")

        print("Location available:")
        print("India")
        print("United States")
        print("California, United States")
        print("Sanfrancisco Bay Area")
        print("Sanfrancisco, CA")

        location = "All"
        location = input("Enter Location (default -> All): ")

        return [keyword, location]

    def run(self):
        """Function run() is our main function from where the LinkedIn
        automation starts.
        """
        self.init_vars()        # ? call init_vars to initialize the variables

        self.apply_keyword(self.get_keywords())

        self.form_connection_link()

        self.driver.get(self.connections_link)


class LinkedInConnectionsGuided(LinkedInConnections):
    """Controls LinkedIn Connections, its name is LinkedInConnectionsGuided
    because it runs the program in guided mode i.e., you have to manually
    input the 'ID' which you want to target, LinkedInConnections with auto
    mode will be coded once finished coding LinkedInConnectionsGuided.

    Parent:
        LinkedIn: our main LinkedIn class which takes care of enabling of
        the webdriver and the login process.
    """

    def __init__(self, data):
        """Function __init__() is the constructor function of class
        LinkedInConnectionsGuided() which intializes objects for this
        class.
        """
        super(LinkedInConnectionsGuided, self).__init__("guided", data)

        super(LinkedInConnectionsGuided, self).run()

    def target_individual_list(self, lists):
        """Function target_individual_list() targets <li> items individually
        and then finds the invite button which is nested inside <li> item and
        then performs a click() operation on it, if ElementClickIntercepted
        Exception comes which will come at one point then it handles it
        smoothly.

        Args:
            lists: it is a list object that contains <li> items in it
        """
        for _list in lists:
            list_bottom_container = _list.find_element_by_css_selector(
                ".discover-entity-type-card__bottom-container")
            list_footer = list_bottom_container.find_element_by_tag_name(
                "footer")
            invite_button = list_footer.find_element_by_tag_name("button")
            try:
                LinkedIn.inform_user(invite_button, "sending")
                invite_button.click()
            except ElementNotInteractableException:
                print("You got Blocked")
                break
            except ElementClickInterceptedException:
                LinkedIn.inform_user(invite_button, "failed")
                continue

    def get_list_items(self, suggestion_box):
        """Function get_list_items() finds the list items available in the
        suggestion box and then sends it to function target_individual_list()
        which targets the list items individually.

        Args:
            suggestion_box: element that contains the list items
        """
        lists = suggestion_box.find_elements_by_tag_name("li")

        self.target_individual_list(lists)

    def get_suggestion_box_by_id(self, _id):
        """Function get_suggestion_box_by_id() targets the suggestion box
        given by the linkedin application (basically it is the box where
        linkedin keeps people that matches with my profile).

        Args:
            _id: id of the suggestion box
        """
        suggestion_box = self.driver.find_element_by_id(_id)

        self.get_list_items(suggestion_box)

    def get_my_network(self):
        """Function get_my_network() changes the url by executing function
        `get()` from webdriver.
        """
        self.driver.get("https://www.linkedin.com/mynetwork/")

    def start_guided_mode(self):
        """Function start_guided_mode() starts the program in guided mode
        in which the user itself has to guide the program finding the
        suggestion box by entering the ID of the suggestion box manually.
        """
        suggestion_box_id = input("Suggestio Box Id : ")

        self.get_suggestion_box_by_id(suggestion_box_id)

    def run(self):
        """Function run() is the main function from where the program starts
        doing its job.
        """
        self.get_my_network()

        self.start_guided_mode()


class LinkedInConnectionsAuto(LinkedInConnections):
    """Controls LinkedIn Connections, its name is LinkedInConnectionsAuto
    because it runs the program in auto mode i.e., here you don't have to
    manually enter the required field for performing automation unlike the
    LinkedInConnectionsGuided class.

    Parent:
        LinkedIn: our main LinkedIn class which takes care of enabling
        of the webdriver and the login process.
    """

    def __init__(self, data):
        super(LinkedInConnectionsAuto, self).__init__("auto", data)

    def get_my_network(self):
        """Function get_my_network() changes the url by executing function
        `get()` from webdriver.
        """
        self.driver.get("https://www.linkedin.com/mynetwork/")

    def click_buttons(self):
        """Function find_buttons() finds the buttons in the network page
        using webdriver function `find_elements_by_css_selector()` and
        then if they are enabled it executes `click()` function on them
        if not it handles the exception smoothly.
        """
        invite_buttons = WebDriverWait(self.driver, 10).until(
            expected_conditions.presence_of_all_elements_located(
                (By.CSS_SELECTOR, "button[aria-label^='Invite']")
            )
        )
        sent = 0
        failed = 0
        for button in invite_buttons:
            try:
                LinkedIn.inform_user(button, "sending")
                button.click()
                LinkedIn.inform_user(button, "sent")
                sent += 1
            except ElementNotInteractableException:
                print(f"""{colorama.Style.BRIGHT}""", end="")
                print(f"""{colorama.Fore.RED}""", end="")

                print(" \nIt seems like you are blocked by LinkedIn!")

                print(f"""{colorama.Fore.RESET}""", end="")
                print(f"""{colorama.Style.RESET_ALL}""", end="")
                break
            except ElementClickInterceptedException:
                LinkedIn.inform_user(button, "failed")
                failed += 1
                continue

        print(f"""{colorama.Style.BRIGHT}""", end="")

        print(f"""{colorama.Fore.GREEN}""", end="")
        print(f""" Sent        : {sent}""")
        print(f"""{colorama.Fore.RED}""", end="")
        print(f""" Failed      : {failed}""")
        print(f"""{colorama.Fore.BLUE}""", end="")
        print(f""" Total hits  : {sent+failed}""")

        print(f"""{colorama.Style.RESET_ALL}""", end="")

    def prepare_page(self):
        """Method prepare_page() prepares the dynamically loading page before
        starting to send inivitations this functionality we needed because the
        page we are targetting loads dynamically and if we directly target the
        buttons on the page then we might end up with sending only 10 to 12
        invitations and that's not what we want we want to keep sending
        inviations until we get blocked by LinkedIn, so this function executes
        javascript (that requires to move to the bottom of the page) for 5000
        repetitions.
        """
        try:
            _ = WebDriverWait(self.driver, 10).until(
                expected_conditions.presence_of_all_elements_located(
                    (By.CSS_SELECTOR, "button[aria-label^='Invite']")
                )
            )

            _preparing_ = "[.........................]"

            k = 0

            for i in range(5001):
                LinkedIn.execute_javascript(self)
                if i % 200 == 0 and i != 0:
                    _preparing_ = "[" + "#"*(k+1) + _preparing_[k+2:]
                    k += 1
                print(" Preparing page, it might take some time %s" %
                      (_preparing_), end="\r")

            print()
        except NoSuchElementException:
            pass

    def run(self):
        """Function run() is the main function from where the program
        starts doing its job.
        """
        self.get_my_network()

        self.prepare_page()

        self.click_buttons()


class InvitationManager(LinkedIn):
    """

    """

    def __init__(self, data):
        """Constructor __init__() initializes the InvitationManager object.

        Args:
            data: user data field
        """
        super(InvitationManager, self).__init__(data)

    def show_sent(self):
        """

        """
        pass

    def show_recieved(self):
        """

        """
        pass

    def show(self, _type):
        """Method show() shows the invitations send or recieved.

        Args:
            _type: is the type of invitation user want to see
            send or recieved
        """
        pass

    def withdraw(self, mark):
        """

        """
        pass


class MyNetwork(LinkedIn):

    def __init__(self, data):
        super(MyNetwork, self).__init__(data)
        self.init_vars()

    def init_vars(self):
        self.connections_url = "https://www.linkedin.com/mynetwork/invite-connect/connections/"

    def get_connections_page(self):
        self.driver.get(self.connections_url)

    def get_profiles_container(self):
        return self.driver.find_element_by_css_selector(
            "section[class^=mn-connections]").find_element_by_tag_name("ul")

    def get_profiles(self):
        for _list in self.get_profiles_container().find_elements_by_tag_name("li"):
            pass

    def show(self):
        self.get_connections_page()
        self.get_profiles()

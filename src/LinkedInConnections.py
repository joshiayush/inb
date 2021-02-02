from LinkedIn import (
    LinkedIn,                           # * importing `LinkedIn` class
    webdriver,                          # * importing `webdriver`
    Keys,                               # * importing `keys`
    WebDriverWait,                      # * importing `WebDriverWait`
    expected_conditions,                # * importing `expected_conditions`
    By,                                 # * importing `By`
    NoSuchElementException,             # * importing `NoSuchElementException`
    ElementClickInterceptedException,   # * importing `ElementClickInterceptedException`
    TimeoutException,                   # * importing `TimeoutException`
    ActionChains,                       # * importing `ActionsChains`
    re,                                 # * importing `regex` module
)
# * importing `time` module
import time
# * importing `colorama`
import colorama
# * importing `urllib.parse`
import urllib.parse


class LinkedInConnections(LinkedIn):

    def __init__(self, _type, data):
        super(LinkedInConnections, self).__init__(data)

        self.method = input(
            "Search method [recommended auto for noobs] (default -> auto/A) or (keyword based/K): ")

        if _type == "auto" and self.method.lower() == "k":
            self.init_vars()        # ? call init_vars to initialize the variables
            self.run()              # ? call run function

    def init_vars(self):
        """
        Function init_vars() initializes all the variables

        that are required to implement search functionality
        """
        self.linkedin = "https://www.linkedin.com/"
        self.search = "search/results/"
        self.people = "people/?"
        self.geoUrn = "geoUrn="
        self.geoIndia = '%5B"102713980"%5D&'
        self.geoUSA = '%5B"103644278"%5D&'
        self.geoCalifornia = '%5B"102095887"%5D&'
        self.geoSanFranciscoBA = '%5B"90000084"%5D&'
        self.geoSanFranciscoCA = '%5B"102277331"%5D&'
        self.location = ""
        self.origins = ["SWITCH_SEARCH_VERTICAL", "FACETED_SEARCH"]
        self.origin = self.origins[0]
        self.keywords = f"keywords=__key__&origin={self.origin}"
        self.connections_link = ""

    def quote_url(self, url, safe=f"~@#$&()*!+=:;,.?/\\"):
        """
        URL-encodes a string (either str (i.e. ASCII) or unicode);

        uses de-facto UTF-8 encoding to handle Unicode codepoints

        in given string.
        """
        return urllib.parse.quote(url.encode('utf-8'), safe)

    def form_connection_link(self):
        """
        Function form_connection_link() forms a linkedin connections

        link by encoding 
        """
        self.connections_link = self.quote_url(
            self.linkedin + self.search + self.people + self.location + self.keywords + self.origin)

        print(self.connections_link)

    def getUrn(self, key):
        Urns = {
            "India": self.geoIndia,
            "United States": self.geoUSA,
            "California, United States": self.geoCalifornia,
            "Sanfrancisco Bay Area": self.geoSanFranciscoBA,
            "Sanfrancisco, CA": self.geoSanFranciscoCA
        }

        return Urns[key]

    def apply_keyword(self, keyword):
        """
        Function apply_keyword() applies keyword to a part of the

        linkedin connections link
        """
        self.keywords = self.keywords.replace("__key__", keyword[0])

        if (keyword[1] == "All"):
            self.origin = self.origins[1]
            self.keywords = f"keywords=__key__&origin={self.origin}"
            self.location = self.geoUrn + self.geoIndia + self.geoUSA + \
                self.geoCalifornia + self.geoSanFranciscoBA + \
                self.geoSanFranciscoCA
        else:
            self.origin = self.origins[1]
            self.keywords = f"keywords=__key__&origin={self.origin}"
            self.location = self.getUrn(keyword[1])

    def get_keywords(self):
        """
        Function get_keywords() asks the user for the keywords that

        has to be applied when searching for people
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
        """
        Function run() is our main function from where the

        LinkedIn automation starts
        """
        self.apply_keyword(self.get_keywords())

        self.form_connection_link()

        self.driver.get(self.connections_link)


class LinkedInConnectionsGuided(LinkedInConnections):
    """
    Controls LinkedIn Connections, its name is LinkedInConnectionsGuided

    because it runs the program in guided mode i.e., you have to manually

    input the 'ID' which you want to target, LinkedInConnections with

    auto mode will be coded once finished coding LinkedInConnectionsGuided.

    ! Parent:
        * LinkedIn: our main LinkedIn class which takes care of enabling of
        * the webdriver and the login process.
    """

    def __init__(self, data):
        """
        Function __init__() is the constructor function of class

        LinkedInConnectionsGuided() which intializes objects for

        this class
        """
        super(LinkedInConnectionsGuided, self).__init__("guided", data)

        self.run()

    def get_aria_label(self, button, _type):
        """
        Function get_aria_label() retrieves the value of

        attribute 'aria-label' using the webdriver function

        'get_attribute()' which returns the value given to

        that attribute.

        ! Args:
            * button: button element in which the program has
            * to click

            * _type: is the status is it sending or failed
        """
        if (_type == "sending"):
            print(
                "Sending invitation to Person labelled by >>> '",
                button.get_attribute("aria-label").strip(),
                "'",
                "(status -> ",
                _type.strip(),
                ")"
            )
        elif (_type == "failed"):
            print(f"{colorama.Fore.RED}",
                  "Sending invitation to Person labelled by >>> '",
                  button.get_attribute("aria-label").strip(),
                  "'",
                  "(status -> ",
                  _type.strip(),
                  ")",
                  f"{colorama.Fore.RESET}"
                  )

    def target_individual_list(self, lists):
        """
        Function target_individual_list() targets <li> items

        individually and then finds the invite button which is

        nested inside <li> item and then performs a click()

        operation on it, if ElementClickInterceptedException

        comes which will come at one point then it handles it

        smoothly.

        ! Args:
            * lists: it is a list object that contains <li> items
            * in it
        """
        # iterating through the lists
        for _list in lists:
            # targetting lists bottom container
            list_bottom_container = _list.find_element_by_css_selector(
                ".discover-entity-type-card__bottom-container")
            # targetting lists footer component
            list_footer = list_bottom_container.find_element_by_tag_name(
                "footer")
            # targetting lists invite button
            invite_button = list_footer.find_element_by_tag_name("button")
            try:
                self.get_aria_label(invite_button, "sending")
                # performing click on invite button using driver.click() method
                invite_button.click()
            except ElementClickInterceptedException:
                self.get_aria_label(invite_button, "failed")
                # continue if Exception
                continue

    def get_list_items(self, suggestion_box):
        """
        Function get_list_items() finds the list items available

        in the suggestion box and then sends it to function

        target_individual_list() which targets the list items

        individually

        ! Args:
            * suggestion_box: element that contains the list items
        """
        lists = suggestion_box.find_elements_by_tag_name("li")

        self.target_individual_list(lists)

    def get_suggestion_box_by_id(self, _id):
        """
        Function get_suggestion_box_by_id() targets the suggestion

        box given by the linkedin application (basically it is the

        box where linkedin keeps people that matches with my profile)

        ! Args:
            * _id: id of the suggestion box
        """
        suggestion_box = self.driver.find_element_by_id(_id)

        self.get_list_items(suggestion_box)

    def get_my_network(self):
        """
        Function get_my_network() changes the url by executing

        function `get()` from webdriver
        """
        self.driver.get("https://www.linkedin.com/mynetwork/")

    def start_guided_mode(self):
        """
        Function start_guided_mode() starts the program in guided

        mode in which the user itself has to guide the program

        finding the suggestion box by entering the ID of the

        suggestion box manually
        """
        suggestion_box_id = input("Suggestio Box Id : ")

        self.get_suggestion_box_by_id(suggestion_box_id)

    def run(self):
        """
        Function run() is the main function from where the

        program starts doing its job
        """
        self.get_my_network()

        self.start_guided_mode()


class LinkedInConnectionsAuto(LinkedInConnections):
    """
    Controls LinkedIn Connections, its name is LinkedInConnectionsAuto

    because it runs the program in auto mode i.e., here you don't have

    to manually enter the required field for performing automation unlike

    the LinkedInConnectionsGuided class.

    ! Parent:
        * LinkedIn: our main LinkedIn class which takes care of enabling of
        * the webdriver and the login process.
    """

    def __init__(self, data):
        super(LinkedInConnectionsAuto, self).__init__("auto", data)

        self.run()

    def get_my_network(self):
        """
        Function get_my_network() changes the url by executing

        function `get()` from webdriver
        """
        if self.method.lower() == "k":
            self.driver.get(self.connections_link)
        else:
            self.driver.get("https://www.linkedin.com/mynetwork/")

    def get_aria_label(self, button, _type):
        """
        Function get_aria_label() retrieves the value of

        attribute 'aria-label' using the webdriver function

        'get_attribute()' which returns the value given to

        that attribute.

        ! Args:
            * button: button element in which the program has
            * to click

            * _type: is the status is it sending or failed
        """
        if (_type == "sending"):
            print(
                "Sending invitation to Person labelled by >>> '",
                button.get_attribute("aria-label").strip(),
                "'",
                "(status -> ",
                _type.strip(),
                ")"
            )
        elif (_type == "failed"):
            print(f"{colorama.Fore.RED}",
                  "Sending invitation to Person labelled by >>> '",
                  button.get_attribute("aria-label").strip(),
                  "'",
                  "(status -> ",
                  _type.strip(),
                  ")",
                  f"{colorama.Fore.RESET}"
                  )

    def find_buttons(self):
        """
        Function find_buttons() finds the buttons in the network

        page using webdriver function `find_elements_by_css_selector()`

        and then if they are enabled it executes `click()` function

        on them if not it handles the exception smoothly
        """
        invite_buttons = self.driver.find_elements_by_css_selector(
            "button[aria-label^='Invite']")

        for button in invite_buttons:
            # accessing each list item
            try:
                # sending button to function get_aria_label()
                self.get_aria_label(button, "sending")
                # executing click() operation on the button
                button.click()
            except ElementClickInterceptedException:
                # handling ElementClickInterceptedException exception
                self.get_aria_label(button, "failed")
                continue

    def scroll_to_bottom(self):
        """
        Function scroll_to_bottom() scrolls the page to its maximum

        height it keeps doing this until the page height becomes limited

        we need this functionality because the page we are targetting here

        is a dynamically loading page with the help of function execute_script()

        we are able to scroll the page to its bottom, execute_script()

        takes javascript statements as its querry and then performs operations
        """
        old_position = 0

        new_position = None

        while new_position != old_position:
            # Get old scroll position
            old_position = self.driver.execute_script(
                ("return (window.pageYOffset !== undefined) ?"
                 " window.pageYOffset : (document.documentElement ||"
                 " document.body.parentNode || document.body);"))
            # call find_buttons() function once the page is loaded
            self.find_buttons()
            # sleep for atleast 1 second before the next move
            time.sleep(1)
            # execute script
            self.driver.execute_script((
                "var scrollingElement = (document.scrollingElement ||"
                " document.body);scrollingElement.scrollTop ="
                " scrollingElement.scrollHeight;"))
            # Get new position
            new_position = self.driver.execute_script(
                ("return (window.pageYOffset !== undefined) ?"
                 " window.pageYOffset : (document.documentElement ||"
                 " document.body.parentNode || document.body);"))

    def run(self):
        """
        Function run() is the main function from where the

        program starts doing its job
        """
        self.get_my_network()

        # sleep for 10 seconds after going to the network page
        time.sleep(10)

        self.scroll_to_bottom()

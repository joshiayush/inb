"""from __future__ imports must occur at the beginning of the file. DO NOT CHANGE!"""
from __future__ import annotations

import re
import sys

from DOM.cleaners import clear_msg_overlay

from console.print import printRed
from console.print import printGreen

from errors.error import ZeroFlagException
from errors.error import EmptyResponseException
from errors.error import CommandFlagNotFoundException
from errors.error import CredentialsNotFoundException
from errors.error import FailedLoadingResourceException
from errors.error import NoSuchConfigurationFoundException
from errors.error import DomainNameSystemNotResolveException

from selenium.common.exceptions import NoSuchElementException

from linkedin.linkedin import LinkedIn
from linkedin.linkedinconnectionsauto import LinkedInConnectionsAuto


class Main(object):
    """Class Main is the main class, this class gives the 'cli' (Command Line Interface) 
    to the user. We don't have `GUI` (Graphical User Interface) here because I don't have 
    any deign Idea in my mind yet.
    """

    def __init__(self: Main) -> None:
        """Main class constructor to initialise the commands and required variables.

        :Args:
            - self: {Main} object

        :Returns:
            - {Main}
        """
        self.init_commands()

        self.init_vars()

        Main.home()

    def init_commands(self: Main) -> None:
        """Method init_commands() to initialize the commands that LinkedIn Automater provides,

            COMMANDS
        ================

        +--------------+----------------------------------------+
        |   exit       |    exit from the program               |
        +--------------+----------------------------------------+
        |   show       |    shows the entered details           |
        +--------------+----------------------------------------+
        |   help       |    prints the commands and their usage |
        +--------------+----------------------------------------+
        |   clear      |    clears the screen                   |
        +--------------+----------------------------------------+ 
        |   theme      |    sets the given theme                |
        +--------------+----------------------------------------+
        |   config     |    shows how you can add fields        |
        +--------------+----------------------------------------+
        |   delete     |    deletes the cache stored            |
        +--------------+----------------------------------------+
        |   linkedin   |    activates the automation process    |
        +--------------+----------------------------------------+
        |   developer  |    prints the developer details        |
        +--------------+----------------------------------------+

        :Args:
            - self: {Main} object

        :Returns:
            - {None}
        """
        from helpers.command import help_with_configs

        self.commands = {
            "show": self.handle_show_commands,
            "help": self.handle_help_commands,
            "exit": self.handle_exit_commands,
            "theme": self.handle_theme_commands,
            "clear": self.handle_clear_commands,
            "config": help_with_configs,
            "delete": self.handle_delete_commands,
            "linkedin": self.handle_linkedin_commands,
            "developer": self.handle_developer_commands,
        }

    def init_vars(self: Main) -> None:
        """Method init_vars() to intialize variables like encrypted_email, encrypted_password,
        data, driver_path and if_headless.

        :Args:
            - self: {Main} object

        :Returns:
            - {None}
        """
        self.encrypted_email = ""
        self.encrypted_password = ""
        self.data = {
            "user_email": "",
            "user_password": "",
        }
        self.driver_path = "/Python/linkedin-bot/driver/chromedriver"
        self.if_headless = False

    @property
    def user_email(self: Main) -> str:
        """Property method user_email to return user email address.

        :Args:
            - self: {Main} object

        :Returns:
            - {str} user email address

        :Raises:
            - KeyError if the key 'user_password' is not present in {dict} _credentials

        :Usage:
            - user_email = self.user_email
        """
        return self.data["user_email"]

    @user_email.setter
    def user_email(self: Main, email: str) -> None:
        """Property method user_email to set user email address.

        :Args:
            - self: {LinkedIn} object
            - user_email: {str} user email address

        :Returns:
            - {None}

        :Raises:
            - KeyError if the key 'user_password' is not present in {dict} _credentials

        :Usage:
            - self.user_email = user_email
        """
        self.data["user_email"] = email

    @property
    def user_password(self: Main) -> str:
        """Property method user_password to return user password.

        :Args:
            - self: LinkedIn object

        :Returns:
            - {str} user password

        :Raises:
            - KeyError if the key 'user_password' is not present in {dict} _credentials

        :Usage:
            - user_password = self.user_password
        """
        return self.data["user_password"]

    @user_password.setter
    def user_password(self: Main, password: str) -> None:
        """Property method user_password to set user password.

        :Args:
            - self: {LinkedIn} object
            - user_email: {str} user email address

        :Returns:
            - {None}

        :Raises:
            - KeyError if the key 'user_password' is not present in {dict} _credentials

        :Usage:
            - self.user_password = user_password
        """
        self.data["user_password"] = password

    def store_cache(self: Main) -> None:
        """Method store_cache() applies encryption on the fields if both the fields are 
        available and then calls the method 'store_credentials' to store the credentials 
        as cache.

        :Args:
            - self: {Main} object

        :Returns:
            - {None}
        """
        if not self.user_email or not self.user_password:
            return

        from creds.crypto import encrypt_email

        from errors.error import PropertyNotExistException

        try:
            encrypt_email(self)
        except PropertyNotExistException as error:
            printRed(f"""{error}""", style='b', pad='1')

        from creds.crypto import encrypt_password

        try:
            encrypt_password(self)
        except PropertyNotExistException as error:
            printRed(f"""{error}""", style='b', pad='1')

        from creds.storage import store_credentials

        try:
            store_credentials(self)
        except PropertyNotExistException as error:
            printRed(f"""{error}""", style='b', pad='1')

    @staticmethod
    def home() -> None:
        """Method home() prints the home screen.

        :Args:
            - {None}

        :Returns:
            - {None}
        """
        from helpers.window import clear

        clear()

        printGreen(f"""Type help for more information!""",
                   style='b', start='\n', pad='1')

    @staticmethod
    def set_theme(_theme: str) -> None:
        """Function set_theme() sets the cli (Command Line Interface) theme according to 
        the value given.

        :Args:
            _theme: {str} theme

        :Returns:
            - {None}

        :Usage:
            - self.set_theme("--parrot")
            - self.set_theme("--normal")
        """
        from console import Theme

        if _theme == "--parrot":
            Theme.enable_theme_parrot()
            Main.home()
            return

        if _theme == "--normal":
            Theme.disable_theme_parrot()
            Main.home()
            return

        printRed(
            f"""'{_theme}' can't be recognized as a 'theme' command""", style='b', pad='1', force="+f")
        return

    def get_command_length(self: Main) -> int:
        """Method get_command_length() returns the lenght of the command entered. 

        :Args:
            - self: {Main} object

        :Returns:
            - {int} lenght of the command entered.

        :Usage:
            - command_length = self.get_command_length()
        """
        return len(self.command.split(" "))

    def get_command_at_index(self: Main, index: int) -> str:
        """Method get_command_at_index() returns a value at a given index of the command list.

        :Args:
            - self: {Main} object
            - index: {int} index

        :Returns:
            - {str} command at a specified index

        :Usage:
            - command_at_index_two = self.get_command_at_index(2)
        """
        try:
            return self.command.split(" ")[index].strip()
        except IndexError:
            return None

    def get_search_query(self: Main) -> None:
        """Method get_search_query() returns the search query entered by user.

        :Args:
            - self: {Main} object

        :Returns:
            - {None}
        """
        querry = self.get_command_at_index(4)

        if len(querry.split("&&")) != 2:
            return

        if not "industry=" in querry.split("&&")[0] or not ("location=" in querry.split("&&")[1] or True):
            return

        self.search_keywords = querry.split(
            "&&")[0][querry.split("&&")[0].find("=")+1::]

        if not "location" in querry.split("&&")[1]:
            return

        self.search_location = querry.split(
            "&&")[1][querry.split("&&")[1].find("=")+1::]

    def send_invitation(self: Main) -> None:
        """Method send_invitation executes the process of sending invitation to people.

        :Args:
            - self: {Main} object

        :Returns:
            - {None}
        """
        _linkedin = LinkedIn(
            {"user_email": self.user_email, "user_password": self.user_password}, self.driver_path)

        _linkedin.set_browser_incognito_mode()
        _linkedin.set_ignore_certificate_error()

        if self.if_headless:
            _linkedin.set_headless()

        _linkedin.enable_webdriver_chrome(
            _linkedin.get_chrome_driver_options())

        try:
            _linkedin.get_login_page()
        except DomainNameSystemNotResolveException as error:
            printRed(f"""{error}""", style='b', pad='4', force='+f')
            return

        _linkedin.login()

        _linkedin_connection = LinkedInConnectionsAuto(_linkedin, limit=20)

        try:
            _linkedin_connection.get_my_network()
        except EmptyResponseException:
            printRed(f"""{error}""", style='b', pad='4', force='+f')
            return

        try:
            clear_msg_overlay(_linkedin_connection)
        except NoSuchElementException as error:
            printRed(f"""{error}""", style='b', pad='4', force='+f')
        except FailedLoadingResourceException as error:
            printRed(f"""{error}""", style='b', pad='4', force='+f')

        _linkedin_connection.run()

    def handle_send_commands(self: Main) -> None:
        """Method handle_send_commands() handles the operations when you apply flag 'send' 
        with 'linkedin' command. We handle operation in two ways where one is when the user 
        enters exact number of flags with these commands and the other is when user ommits the 
        default flags.

        :Args:
            - self: {Main} object

        :Returns:
            - {None}

        :Raises:
            - CredentialsNotFoundException if user's credentials not found

        :Usage:
            - linkedin [send] [suggestions^] --auto^ [--headless] [--use--cache]
            - linkedin [send] [search* industry=example&&location=india+usa+...] --auto^ [--headless] [--use-cache]
        """
        if self.get_command_at_index(2) != "send":
            return

        if self.get_command_at_index(-1) == "--use-cache":
            from creds.storage import get_credentials
            get_credentials(self)

        if self.get_command_at_index(-2) == "--headless":
            self.if_headless = True

        if self.get_command_at_index(3) == "suggestions":
            if self.get_command_at_index(4) == "--auto" or True:
                if not self.user_email or not self.user_password:
                    raise CredentialsNotFoundException(
                        "Credentials not found! Need credentials first use config.user.email/password to add them!")

                self.send_invitation()
                return

        if self.get_command_at_index(3) == "--headless" or self.get_command_at_index(3) == "--use-cache":
            if not self.user_email or not self.user_password:
                raise CredentialsNotFoundException(
                    "Credentials not found! Need credentials first use config.user.email/password to add them!")

            self.send_invitation()
            return

        if self.get_command_length() == 3:
            if not self.user_email or not self.user_password:
                raise CredentialsNotFoundException(
                    "Credentials not found! Need credentials first use config.user.email/password to add them!")

            self.send_invitation()
            return

        self.command = self.command[3:]
        self.handle_commands()
        return

    def handle_invitation_manager_commands(self: Main) -> None:
        pass

    def handle_mynetwork_commands(self: Main) -> None:
        pass

    def handle_linkedin_commands(self: Main) -> None:
        """Method handle_linkedin_commands() handles the first flag given to the linkedin
        command.

        :Args:
            - self: {Main} object

        :Returns:
            - {None}

        :Raises:
            - ZeroFlagException if command 'linkedin' is referenced alone
            - CommandFlagNotFoundException if 'linkedin' command flag not found
        """
        if self.get_command_length() <= 2:
            raise ZeroFlagException(
                "Command 'linkedin' cannot be referenced without a flag!")

        if self.get_command_at_index(2) == "send":
            try:
                self.handle_send_commands()
            except CredentialsNotFoundException as error:
                printRed(f"""{error}""", style='b', pad='1')
            return

        if self.get_command_at_index(2) == "invitation-manager":
            self.handle_invitation_manager_commands()
            return

        if self.get_command_at_index(2) == "mynetwork":
            self.handle_mynetwork_commands()
            return

        if self.get_command_at_index(2) == "--help":
            from helpers.command import help_with_linkedin
            help_with_linkedin()
            return

        raise CommandFlagNotFoundException(
            f"""'{self.get_command_at_index(2)}' is not a 'linkedin' command!""")

    def show_job_details(self: Main) -> None:
        """Method show_job_details() prints the job details that the user entered.

        :Args:
            self: {Main} object

        :Returns:
            - {None}
        """
        if not self.job_keywords and not self.job_keywords:
            return

        printGreen(f"""Job Keywords -> %s""" % (self.job_keywords if self.job_keywords else None),
                   style='b', pad='1')
        printGreen(f"""Job Location -> %s""" % (self.job_keywords if self.job_keywords else None),
                   style='b', pad='1')

    def ask_to_show_password(self: Main) -> None:
        """Method ask_to_show_password() asks the user if (s)he want to see the password 
        if yes show them if not don't show them, this is for security purpose. 

        :Args:
            self: {Main} object

        :Returns:
            - {None}
        """
        try:
            from console.scan import scanBlue

            ch = scanBlue(f"""Show password anyway? [y/N]:""", style='b',
                          pad='1', end=' ', force="+f") if self.user_password else 'n'

            if ch.lower() != 'y':
                return

            printGreen(f"""%s""" % (
                self.user_email if self.user_email else "use config.user.email to add user email"),
                style='b', pad='1')
            printGreen(f"""%s""" % (
                self.user_password if self.user_password else "use config.user.password to add user password"),
                style='b', pad='1')
        except KeyboardInterrupt:
            printGreen(f"""Piece""", start='\n', pad='1')
            sys.exit()

    def handle_show_commands(self: Main) -> None:
        """Method show() gets executed once the user hit the command 'show' this basically 
        prints the information that user had entered like email, password, job keys/location.

        :Args:
            - self: {Main} object

        :Returns:
            - {None}

        :Raises:
            - CommandFlagNotFoundException if 'show' is referenced with an unrecognized flag 
        """
        if self.get_command_length() > 2 and self.get_command_at_index(2) == "--help":
            from helpers.command import help_with_show
            help_with_show()
            return

        printGreen(f"""%s""" % (
            self.user_email if self.user_email else "use config.user.email to add user email"),
            style='b', pad='1')
        printGreen(f"""%s""" % (
            "*"*len(self.user_password) if self.user_password else "use config.user.password to add user password"),
            style='b', pad='1')

        self.show_job_details()
        self.ask_to_show_password()

        if self.get_command_length() > 2 and self.get_command_at_index(2) != "--help":
            raise CommandFlagNotFoundException(
                f"""'{self.get_command_at_index(2)}' is not a 'show' command!""")

        return

    def handle_delete_commands(self: Main) -> None:
        """Method handle_delete_commands() gets executed once the user hits the command
        'delete' this basically deletes the cache stored (User credentials) if exists.

        :Args:
            - slef: {Main} object

        :Returns:
            - {None}

        :Raises:
            - ZeroFlagException if command 'delete' is referenced alone
            - CommandFlagNotFoundException if 'delete' is referenced with an unrecognized flag
        """
        from creds.storage import delete_key
        from creds.storage import delete_cache

        if self.get_command_length() <= 2:
            raise ZeroFlagException(
                "command 'delete' cannot be referenced alone!")

        if self.get_command_at_index(2) == "--help":
            from helpers.command import help_with_delete
            help_with_delete()
            return

        if self.get_command_at_index(2) == "--cache":
            delete_cache()
            return

        if self.get_command_at_index(2) == "--key":
            delete_key()
            return

        if self.get_command_at_index(2) == "--cache&&--key":
            delete_cache()
            delete_key()
            return

        raise CommandFlagNotFoundException(
            f"""{self.get_command_at_index(2)} is not recognized as a 'delete' command!""")

    def handle_developer_commands(self: Main) -> None:
        """Method developer() gets executed once the user hits the command 'developer'
        it basically shows the developer's network profiles and mail address.

        :Args:
            - self: {Main} object

        :Returns:
            - {None}

        :Raises:
            - CommandFlagNotFoundException if command 'developer' is referenced with an unrecognized flag
        """
        if self.get_command_length() > 2:
            if self.get_command_at_index(2) != "--help":
                raise CommandFlagNotFoundException(
                    f"""{self.get_command_at_index(2)} is not a 'developer' command!""")

            if self.get_command_at_index(2) == "--help":
                from helpers.command import help_with_developer
                help_with_developer()
                return

            return

        printGreen(f"""Name     :  Ayush Joshi""",
                   style='b', pad='1', force="+f")
        printGreen(f"""Email    :  ayush854032@gmail.com (primary)""",
                   style='b', pad='1', force="+f")
        printGreen(f"""Email    :  joshiayush.joshiayush@gmail.com""",
                   style='b', pad='1', force="+f")
        printGreen(f"""Mobile   :  +91 8941854032 (Only WhatsApp)""",
                   style='b', pad='1', force="+f")
        printGreen(f"""GitHub   :  https://github.com/JoshiAyush""",
                   style='b', pad='1', force="+f")
        printGreen(f"""LinkedIn :  https://www.linkedin.com/in/ayush-joshi-3600a01b7/""",
                   style='b', pad='1', force="+f")

    def handle_theme_commands(self: Main) -> None:
        """Method handle_theme_commands() handles the 'theme' commands it calls the 
        set_theme() function once it confirms that the flag that is given with the theme 
        command is an actual theme flag.

        :Args:
            - self: {Main} object

        :Returns:
            - {None}

        :Raises:
            - ZeroFlagException if command 'theme' is referenced alone
            - CommandFlagNotFoundException if command 'theme' is referenced with an unrecognized flag
        """
        if self.get_command_length() < 3:
            raise ZeroFlagException(
                "command 'theme' can not be referenced alone!")

        if self.get_command_at_index(2) == "--parrot" or self.get_command_at_index(2) == "--normal":
            Main.set_theme(self.get_command_at_index(2).strip())
            return

        if self.get_command_at_index(2) == "--help":
            from helpers.command import help_with_theme
            help_with_theme()
            return

        raise CommandFlagNotFoundException(
            f"""'{self.get_command_at_index(2)}' is not a 'theme' command!""")

    def handle_clear_commands(self: Main) -> None:
        """Method handle_clear_commands() handles the 'clear' commands it calls the home() 
        function once it confirms that the given command is exactly a 'clear' command.

        :Args:
            - self: {Main} object

        :Returns:
            - {None}

        :Raises:
            - CommandFlagNotFoundException if command 'clear' is referenced with an unrecognized command
        """
        if self.get_command_length() == 2:
            Main.home()
            return

        if self.get_command_at_index(2) == "--help":
            from helpers.command import help_with_clear
            help_with_clear()
            return

        raise CommandFlagNotFoundException(
            f"""'{self.get_command_at_index(2)}' is not a clear command""")

    def handle_help_commands(self: Main) -> None:
        """Method handle_help_commands() handles the 'help' command it provides a manual to 
        the user if it identifies that the given command is an actual help command.

        :Args:
            - self: {Main} object

        :Returns:
            - {None}

        :Raises:
            - CommandFlagNotFoundException if command 'help' is referenced with an unrecognized flag
        """
        if self.get_command_length() > 2:
            if self.get_command_at_index(2) == "--help":
                from helpers.command import help_with_help
                help_with_help()
                return

            raise CommandFlagNotFoundException(
                f"""'{self.get_command_at_index(2)}' is not recognized as a 'help' command!""")

        printGreen(f"""LinkedIn Bash, version 1.31.9(1)-release (lnkdbt-1.31.9)""",
                   style='b', pad='1')
        printGreen(f"""These commands are defined internally. Type 'help' to see this list.""",
                   style='b', pad='1')
        printGreen(f"""Type 'command' --help to know more about that command.""",
                   style='b', pad='1')
        printGreen(f"""A ([]) around a command means that the command is optional.""",
                   start='\n', style='b', pad='1')
        printGreen(f"""A (^) next to command means that the command is the default command.""",
                   style='b', pad='1')
        printGreen(f"""A (<>) around a name means that the field is required.""",
                   style='b', pad='1')
        printGreen(f"""A (/) between commands means that you can write either of these but not all.""",
                   style='b', pad='1')
        printGreen(f"""A (*) next to a name means that the command is disabled.""",
                   style='b', pad='1')
        printGreen(f"""linkedin [send] [suggestions^] --auto^ [--headless] [--use-cache]""",
                   start='\n', style='b', pad='1')
        printGreen(f"""linkedin [send] [search* industry=example&&location=india+usa+...] --auto^ [--headless] [--use-cache]""",
                   style='b', pad='1')
        printGreen(f"""linkedin [invitation-manager*] [show*] --sent*^/--recieved* [--headless] [--use-cache]""",
                   style='b', pad='1')
        printGreen(f"""linkedin [invitation-manager*] [ignore*/withdraw*] [all*^/over > <days>*] [--headless] [--use-cache]""",
                   style='b', pad='1')
        printGreen(f"""linkedin [mynetwork*] [show*] [all*^/page > 1^+2+3+...*] [--headless] [--use-cache]""",
                   style='b', pad='1')
        printGreen(f"""linkedin [mynetwork*] [sendmessage*] [all*^] [--greet*^] [--headless] [--use-cache]""",
                   style='b', pad='1')
        printGreen(f"""config""",
                   style='b', pad='1', start='\n')
        printGreen(f"""show""",
                   style='b', pad='1', start='\n')
        printGreen(f"""delete""",
                   style='b', pad='1', start='\n')
        printGreen(f"""developer""",
                   style='b', pad='1', start='\n')
        printGreen(f"""theme [--parrot^/--normal]""",
                   style='b', pad='1', start='\n')
        printGreen(f"""clear""",
                   style='b', pad='1', start='\n')
        printGreen(f"""exit""",
                   style='b', pad='1', start='\n')

    def handle_exit_commands(self: Main) -> None:
        """Method handle_exit_commands() handles the 'exit' commands it calls the python's 
        exit() function once it confirms that the given command is exactly a 'exit' command.

        :Args:
            - self: {Main} object

        :Returns:
            - {None}

        :Raises:
            - CommandFlagNotFoundException if command 'exit' is referenced with an unrecognized flag
        """
        if self.get_command_length() < 3:
            printGreen(f"""Piece""", style='b', pad='1')
            sys.exit()

        if self.get_command_at_index(2) == "--help":
            from helpers.command import help_with_exit
            help_with_exit()
            return

        raise CommandFlagNotFoundException(
            f"""'{self.get_command_at_index(2)}' is not recognized as a 'exit' flag!""")

    def Error(self: Main) -> None:
        """Method Error() gets called when the entered command is not recognized. 

        :Args:
            - self: {Main} object

        :Returns:
            - {None}
        """
        if not self.command:
            return

        printRed(
            f"""`{self.command[8:]}` is not recognized as an internal command.""", style='b', pad='1', force="+f")

    def slice_keyword(self: Main) -> str:
        """Method slice_keyword() slice the keywords that comes between double quotes.

        For example, if there is a query like "ayush854032@gmail.com" then this method only returns 
        whatever is in between the double quotes.

        :Args:
            - self: {Main} object

        :Returns:
            - {str} keyword that is in between the double quotes
        """
        try:
            return self.command.split(' ')[2][self.command.split(" ")[2].find('"')+1:self.command.split(" ")[2].rfind('"')]
        except IndexError:
            return None

    def get_email(self: Main) -> str:
        """Method check_email() checks the email field for its validness if the email is valid
        email or not if not it returns False otherwise returns the email.

        This method apply a regex on the email to check if the email is a custom email or a normal 
        email address if it finds yes then it return the email address otherwise it returns False.

        :Args:
            - self: {Main} object

        :Returns:
            - {str} valid email address
        """
        email = self.slice_keyword()

        if re.search(r"^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$", email):
            return email

        if re.search(r"^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w+$", email):
            return email

        return None

    def if_password_given(self: Main) -> bool:
        """Method if_password_given() checks if the password if given with the command

        user.config.password "xxx-xxx-xxx"

        :Args:
            - self: {Main} object

        :Returns:
            - {bool} True/False 
        """
        if re.search(r'"[a-zA-z0-9~`!@#\$%\^&\*\(\)_\+=-\\\|\[\]\{\}\"\'\?<>,\.:;\/]*"', self.command.split(" ")[2].strip()):
            return True

        return False

    def handle_configs(self: Main) -> None:
        """Method handle_configs() saves the user's configurations.

        We use re.compile() and re.search() method here to find the pattern in the commands.

        :Args:
            - self: {Main} object

        :Returns:
            - {None}

        :Raises:
            - NoSuchConfigurationFoundException if the configuration command is not recognized
        """
        if self.get_command_length() <= 2:
            if self.get_command_at_index(1) != "config.user.password":
                return

            import getpass

            self.user_password = getpass.getpass(
                prompt=" Password: ")

            if self.get_command_at_index(2) != "--cached":
                return

            self.store_cache()
            return

        if re.compile(r"(config\.user\.email)", re.IGNORECASE).search(self.command):
            email = self.get_email()

            if not email:
                printRed(f"""'{self.command.split(" ")[2].strip()}' is not a valid email address!""",
                         style='b', pad='1')
                return

            self.user_email = email

            if self.get_command_at_index(3) == "--cached":
                self.store_cache()
                self.command = "command config.user.password --cached"
            else:
                self.command = "command config.user.password"

            try:
                self.handle_configs()
            except NoSuchConfigurationFoundException as error:
                printRed(f"""{error}""", style='b', pad='1')

            return

        if "config.user.password" == self.get_command_at_index(1):
            self.user_password = self.slice_keyword()

            if self.get_command_at_index(3) != "--cached":
                self.store_cache()

            return

        if re.compile(r"(config\.job\.keywords)=\w+", re.IGNORECASE).search(self.command):
            self.job_keywords = self.command[self.command.find(
                "=")+1:].strip()
            return

        if re.compile(r"(config\.job\.location)=\w+", re.IGNORECASE).search(self.command):
            self.job_keywords = self.command[self.command.find(
                "=")+1:].strip()
            return

        raise NoSuchConfigurationFoundException("No such configuration found!")

    def handle_commands(self: Main) -> None:
        """Method handle_commands() does the actual handling of the commands entered.

        We find patterns for 'configuration' commands using the re.compile() and re.search()
        method, which finds the pattern in the entered command and calls 'handle_configs()' method 
        if it finds any match if not it calls the functions according to the commands entered.

        :Args:
            - self: {Main} object

        :Returns:
            - {None}
        """
        if re.compile(
            r"(config\.user\.email)|(config\.user\.password)|(config\.job\.keywords)|(config\.job\.location)",
                re.IGNORECASE).search(self.get_command_at_index(1)):
            try:
                self.handle_configs()
            except NoSuchConfigurationFoundException as error:
                printRed(f"""{error}""", style='b', pad='1')
        else:
            try:
                self.commands.get(self.command.split(" ")[1], self.Error)()
            except CredentialsNotFoundException as error:
                printRed(f"""{error}""", style='b', pad='1', force="+f")
            except CommandFlagNotFoundException as error:
                printRed(f"""{error}""", style='b', pad='1', force="+f")
            except ZeroFlagException as error:
                printRed(f"""{error}""", style='b', pad='1', force="+f")
            except FileNotFoundError as error:
                printRed(f"""{error}""", style='b', pad='1', force="+f")

    def run(self: Main) -> None:
        """Method run() runs a infinite loop and starts the 'cli' (Command Line Interface),
        it actually starts listening to the commands and then it calls the function handle_commands()
        which handles the commands.

        We first get the command and add 'command ' in it this way we can handle the commands by
        accessing their position in list.

        Then we call function handle commands that is going to perform operations as per command.

        :Args:
            - self: {Main} object

        :Returns:
            - {None}
        """
        from console.scan import scanGreen

        """Use `while 1` instead of `while True` for performace reason. DO NOT CHANGE!"""
        while 1:
            try:
                self.command = ("command " + scanGreen("LinkedIn/>",
                                style='b', pad='1', start='\n', end=' ')).strip()
            except KeyboardInterrupt:
                break

            if self.get_command_length() > 1:
                self.handle_commands()

        printGreen(f"""Piece""", style='b', start='\n', pad='1')
        sys.exit()


"""Execute program"""
if __name__ == "__main__":
    Main().run()

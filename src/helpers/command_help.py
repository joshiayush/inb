from console.print import printBlue


def help_with_configs() -> None:
    """Function help_with_configs()
    """
    printBlue(f"""config.user.email "example@email.com" --cached""",
              style='b', pad='1')
    printBlue(
        f"""config.user.password "example@password" --cached""", style='b', pad='1')
    printBlue(
        f"""Or you can use the following command if you don't want to show the password on the screen""",
        style='b', pad='1')
    printBlue(f"""config.user.password --cached (hit enter)""",
              style='b', pad='1')
    printBlue(f"""Password: """, style='b', pad='1')
    printBlue(
        f"""config.job.keywords "Data%Science" (use '%' for space)""", style='b', pad='1')
    printBlue(f"""config.job.location "Sanfrancisco%CA" """,
              style='b', pad='1')


def help_with_linkedin() -> None:
    """Method help_with_linkedin() shows how you can use the linkedin
    command in case you missed the flags with the linkedin command or
    mistakenly applied wrong flags with the linkedin command. We declare
    this function static because we don't need to give this function an
    access to the object it's no use giving this function access to the
    object.
    """
    printBlue(
        f"""linkedin [send] [suggestions^] --auto/--guided [--headless] [--use-cache]""", style='b', pad='1')
    printBlue(
        f"""'linkedin' command handles the linkedin process.""", style='b', pad='1')
    printBlue(
        f"""'send' flag sends invitations according to the path given to it.""", style='b', pad='1')
    printBlue(
        f"""'suggestions' flag lets linkedin know that it must use""", style='b', pad='1')
    printBlue(f"""'MyNetwork' tab as a target.""", style='b', pad='1')
    printBlue(
        f"""'--auto/--guided' flag tells the linkedin to start process in auto(recommended) or guided mode.""",
        style='b', pad='1')
    printBlue(
        f"""'--headless' flag tells the program to start automation without opening the browser.""", style='b', pad='1')
    printBlue(
        f"""'--use-cache' uses cache (if stored) for authentication.""", style='b', pad='1')
    printBlue(
        f"""linkedin [send] [search industry=example&&location=india+usa+...] --auto^/--guided [--headless]""", start='\n', style='b', pad='1')
    printBlue(
        f"""'linkedin' command handles the linkedin process.""", style='b', pad='1')
    printBlue(
        f"""'send' flag sends invitations according to the path given to it.""", style='b', pad='1')
    printBlue(
        f"""'search industry=example&&location=india+usa+...' flag lets linkedin know that it must""", style='b', pad='1')
    printBlue(
        f"""go and search for people associated to the given industry (use (%) for space between words in industry)""",
        style='b', pad='1')
    printBlue(
        f"""and living in the given location. You can always add location.""", style='b', pad='1')
    printBlue(
        f"""'--auto/--guided' flag tells the linkedin to start process in auto(recommended) or guided mode.""",
        style='b', pad='1')
    printBlue(
        f"""'--headless' flag tells the program to start automation without opening the browser.""", style='b', pad='1')
    printBlue(
        f"""'--use-cache' uses cache (if stored) for authentication.""", style='b', pad='1')
    printBlue(
        f"""linkedin [invitation-manager*] [show*] --sent*/--recieved* [--headless]""", start='\n', style='b', pad='1')
    printBlue(
        f"""'linkedin' command handles the linkedin process.""", style='b', pad='1')
    printBlue(
        f"""'invitation-manager' flag tells the linkedin to start performing operations on""", style='b', pad='1')
    printBlue(f"""invitation manager tab.""", style='b', pad='1')
    printBlue(
        f"""'show' flag show tells the linkedin to show the people my account want to connect with.""", style='b', pad='1')
    printBlue(
        f"""'--sent/--recieved' flag tells the linkedin to fetch either sent invitations or recieved ones.""",
        style='b', pad='1')
    printBlue(
        f"""'--headless' flag tells the program to start automation without opening the browser.""", style='b', pad='1')
    printBlue(
        f"""'--use-cache' uses cache (if stored) for authentication.""", style='b', pad='1')
    printBlue(
        f"""linkedin [invitation-manager*] [ignore*/withdraw*] [all*^/over > <days>*] [--headless]""",
        start='\n', style='b', pad='1')
    printBlue(
        f"""'linkedin' command handles the linkedin process.""", style='b', pad='1')
    printBlue(
        f"""'invitation-manager' flag tells the linkedin to start performing operations on""", style='b', pad='1')
    printBlue(
        f"""'ignore/withdraw' flag tells the linkedin that you want to activate invitation ignoring or withdrawing process.""",
        style='b', pad='1')
    printBlue(
        f"""'all/over > <days>' flag tell to either withdraw all the sent invitations or""", style='b', pad='1')
    printBlue(
        f"""use the amount of days given to withdraw sent invitations accordingly.""", style='b', pad='1')
    printBlue(
        f"""'--headless' flag tells the program to start automation without opening the browser.""", style='b', pad='1')
    printBlue(
        f"""'--use-cache' uses cache (if stored) for authentication.""", style='b', pad='1')
    printBlue(
        f"""linkedin [mynetwork*] [show*] [all*/page > 1^+2+3+...*] [--headless]""", start='\n', style='b', pad='1')
    printBlue(
        f"""'linkedin' command handles the linkedin process.""", style='b', pad='1')
    printBlue(
        f"""'mynetwork' flag tell the linkedin to start operating on MyNetworks.""", style='b', pad='1')
    printBlue(
        f"""'all/page > 1+2+3+...' flag tells either show all connections or use the pages given.""", style='b', pad='1')
    printBlue(
        f"""'--headless' flag tells the program to start automation without opening the browser.""", style='b', pad='1')
    printBlue(
        f"""'--use-cache' uses cache (if stored) for authentication.""", style='b', pad='1')
    printBlue(
        f"""linkedin [mynetwork*] [sendmessage*] [all*] [--greet*^] [--headless]""", start='\n', style='b', pad='1')
    printBlue(
        f"""'linkedin' command handles the linkedin process.""", style='b', pad='1')
    printBlue(
        f"""'mynetwork' flag tell the linkedin to start operating on MyNetworks.""", style='b', pad='1')
    printBlue(
        f"""'sendmessage' flag tells the linkedin to send messages to connections.""", style='b', pad='1')
    printBlue(
        f"""'all' flag tells the linkedin to use all connections.""", style='b', pad='1')
    printBlue(
        f"""'--greet' flag tells the linkedin to send greet message.""", style='b', pad='1')
    printBlue(
        f"""'--headless' flag tells the program to start automation without opening the browser.""", style='b', pad='1')
    printBlue(
        f"""'--use-cache' uses cache (if stored) for authentication.""", style='b', pad='1')


def help_with_show() -> None:
    """Function help_with_show() shows you how you can use the
    'show' command in case you entered wrong command. We declare
    this function static because we don't need to give this function
    an access to the object it's no use giving this function access
    to the object.
    """
    printBlue(
        f"""'show' shows all the details you have entered like:""", style='b', pad='1')
    printBlue(f"""user.email,""", style='b', pad='1')
    printBlue(
        f"""user.password (asks first if you want to see it really or not),""", style='b', pad='1')
    printBlue(f"""job.keywords,""", style='b', pad='1')
    printBlue(f"""job.location""", style='b', pad='1')


def help_with_delete() -> None:
    printBlue(f"""'delete' command deletes the cache stored.""",
              style='b', pad='1')
    printBlue(f"""Usage: delete --cache""", style='b', pad='1')


def help_with_developer() -> None:
    """Function help_with_developer() shows you how you can use the
    'developer' command in case you entered wrong command. We declare
    this function static because we don't need to give this function
    an access to the object it's no use giving this function access to
    the object.
    """
    printBlue(f"""'developer' shows the developer details like:""",
              style='b', pad='1')
    printBlue(f"""his number, email, profiles ...""",
              style='b', pad='1')


def help_with_theme() -> None:
    """Function help_with_theme() shows you how you can use the
    'theme' command in case you entered wrong command or entered
    a un-matching flag. We declare this function static because
    we don't need to give this function an access to the object
    it's no use giving this function access to the object.
    """
    printBlue(
        f"""'theme --parrot/--normal' changes the cli (command line theme) according to the given theme value.""",
        style='b', pad='1')


def help_with_clear() -> None:
    """Function help_with_clear() shows you how you can use the
    'clear' command in case you entered wrong command. We declare
    this function static because we don't need to give this function
    an access to the object it's no use giving this function access
    to the object.
    """
    printBlue(f"""'clear' clears the screen""", style='b', pad='1')


def help_with_exit() -> None:
    """Function help_with_exit() shows you how you can use the
    'exit' command in case you entered wrong command. We declare
    this function static because we don't need to give this function
    an access to the object it's no use giving this function access
    to the object.
    """
    printBlue(
        f"""'exit' exits the program and also does flushing jobs.""", style='b', pad='1')


def help_with_help() -> None:
    """Function help_with_help() shows you how you can use the
    'help' command in case you entered wrong command. We declare
    this function static because we don't need to give this function
    an access to the object it's no use giving this function access
    to the object.
    """
    printBlue(
        f"""'help' prints a list of commands that the Linkedin Automater have.""",
        style='b', pad='1')

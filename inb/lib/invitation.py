from . import driver_path

from console.print import printRed
from console.print import printBlue
from console.print import printGreen

from errors.error import EmptyResponseException
from errors.error import FailedLoadingResourceException
from errors.error import DomainNameSystemNotResolveException

from DOM.cleaners import clear_msg_overlay

from linkedin.linkedin import LinkedIn
from linkedin.linkedinconnectionsauto import LinkedInConnectionsAuto

from selenium.common.exceptions import NoSuchElementException


def SendInvitation(_creds: dict, _limit: int, headless: bool) -> None:
    """Method send_invitation executes the process of sending invitation to people.

    :Args:
        - {None}

    :Returns:
        - {None}
    """
    _linkedin = LinkedIn(
        {"user_email": _creds["user_email"], "user_password": _creds["user_password"]}, driver_path=driver_path)

    _linkedin.set_browser_incognito_mode()
    _linkedin.set_ignore_certificate_error()

    if headless:
        _linkedin.set_headless()

    _linkedin.enable_webdriver_chrome(
        _linkedin.get_chrome_driver_options())

    printBlue(f"""Connecting ...""", style='n', pad='1', end='\r')

    try:
        _linkedin.get_login_page()
    except DomainNameSystemNotResolveException as error:
        print(' '*80, end='\r')
        printRed(f"""{error}""", style='b', pad='4', force='+f')
        return

    _linkedin.login()

    print(' '*80, end='\r')
    printGreen(f"""Connected ✔""", style='b', pad='1')

    _linkedin_connection = LinkedInConnectionsAuto(_linkedin, limit=_limit)

    printBlue(
        f"""Moving to Network page ...""", style='n', pad='1', end='\r')

    try:
        _linkedin_connection.get_my_network()
    except EmptyResponseException:
        print(' '*80, end='\r')
        printRed(f"""{error}""", style='b', pad='4', force='+f')
        return

    print(' '*80, end='\r')
    printBlue(
        f"""Cleaning message overlay ...""", style='n', pad='1', end='\r')

    while True:
        try:
            clear_msg_overlay(_linkedin_connection)
            break
        except NoSuchElementException as error:
            printRed(f"""{error}""", style='b', pad='4', force='+f')
            break
        except FailedLoadingResourceException as error:
            printRed(f"""{error}""", style='b', pad='4', force='+f')
            continue

    print(' '*80, end='\r')
    printGreen(f"""Cleared message overlay ✔""", style='b', pad='1')

    printGreen(f"""Starting sending invitation ...""", style='b', pad='1')

    _linkedin_connection.run()

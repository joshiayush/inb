import sys

from argparse import RawDescriptionHelpFormatter

from linkedin import __version__

from lib.handler import CommandHandler

from helpers.parser.parser import CreateParser

from helpers.command import get_send_help
from helpers.command import get_show_help
from helpers.command import get_config_help
from helpers.command import get_delete_help
from helpers.command import get_developer_help
from helpers.command import get_invitation_limit_help

from helpers.command import get_lbot_description
from helpers.command import get_send_description
from helpers.command import get_show_description
from helpers.command import get_config_description
from helpers.command import get_delete_description
from helpers.command import get_developer_description
from helpers.command import get_invitation_limit_description


# usage: lbot [-h] {send,config,show,delete,developer} ...
#
#  _     _       _            _ ___         ____        _
# | |   (_)_ __ | | _____  __| |_ _|_ __   | __ )  ___ | |_
# | |   | | '_ \| |/ / _ \/ _` || || '_ \  |  _ \ / _ \| __|
# | |___| | | | |   <  __/ (_| || || | | | | |_) | (_) | |_
# |_____|_|_| |_|_|\_\___|\__,_|___|_| |_| |____/ \___/ \__|
#
#
# LinkedIn Bash, version 1.51.35(1)-release (lbot-1.51.35)
# These commands are defined internally. Type '--help' to see this list
# Type (command) --help to know more about that command
#
# positional arguments:
#   {send,config,show,delete,developer}
#                         available actions
#     send                Command 'send' sends invitation to people on linkedin.
#     config              Command 'config' is used to store user's credentials
#     show                Command 'show' prints the information that is in the database
#     delete              Command 'delete' deletes the information stored in the database
#     developer           Command 'developer' prints the information about the author
#
# optional arguments:
#   -h, --help            show this help message and exit


parser = CreateParser(
    prog="inb", description=get_lbot_description(), formatter_class=RawDescriptionHelpFormatter)

subparsers = parser.add_subparsers(help="available actions", metavar=None)


# Usage: inb send [-h] [-e [EMAIL]] [-p [PASSWORD]] [-c] [-i] [-ngpu] [-m]
#                 {limit} ...
#
#  _     _       _            _ ___         ____        _
# | |   (_)_ __ | | _____  __| |_ _|_ __   | __ )  ___ | |_
# | |   | | '_ \| |/ / _ \/ _` || || '_ \  |  _ \ / _ \| __|
# | |___| | | | |   <  __/ (_| || || | | | | |_) | (_) | |_
# |_____|_|_| |_|_|\_\___|\__,_|___|_| |_| |____/ \___/ \__|
#
#
# Command 'send' sends invitation to people on linkedin.
#
# positional arguments:
#   {limit}               available actions
#     limit               Flag 'limit' sets the daily invitation limit
#
# optional arguments:
#   -h, --help            show this help message and exit
#   -e [EMAIL], --email [EMAIL]
#                         User's email address
#   -p [PASSWORD], --password [PASSWORD]
#                         User's password
#   -c, --cookies         uses cookies for authentication
#   -i, --incognito       set browser in incognito mode
#   -ngpu, --headless     starts chrome in headless mode
#   -m, --start-maximized
#                         set browser in full screen

send = subparsers.add_parser(
    "send", description=get_send_description(), formatter_class=RawDescriptionHelpFormatter, help=get_send_help())

send.add_argument(
    "-e", "--email", type=str, nargs="?", default=None, help="User's email address")
send.add_argument(
    "-p", "--password", type=str, nargs="?", default=None, help="User's password")

# usage: lbot send limit [-h] [limit]
#
#  _     _       _            _ ___         ____        _
# | |   (_)_ __ | | _____  __| |_ _|_ __   | __ )  ___ | |_
# | |   | | '_ \| |/ / _ \/ _` || || '_ \  |  _ \ / _ \| __|
# | |___| | | | |   <  __/ (_| || || | | | | |_) | (_) | |_
# |_____|_|_| |_|_|\_\___|\__,_|___|_| |_| |____/ \___/ \__|
#
#
# Flag 'limit' is used to set the daily invitation limit
# Limit must not exceed by 80 otherwise you'll be blocked for a entire
# week
#
# positional arguments:
#   limit
#
# optional arguments:
#   -h, --help  show this help message and exit


limit_subparsers = send.add_subparsers(
    help="available actions", metavar=None)

limit = limit_subparsers.add_parser(
    "limit",  description=get_invitation_limit_description(), formatter_class=RawDescriptionHelpFormatter,
    help=get_invitation_limit_help())

limit.add_argument("limit", type=int, nargs="?", default=20)

limit.set_defaults(limit=20)


send.add_argument(
    "-c", "--cookies", action="store_true", help="uses cookies for authentication")
send.add_argument(
    "-i", "--incognito", action="store_true", help="set browser in incognito mode")
send.add_argument(
    "-ngpu", "--headless", action="store_true", help="starts chrome in headless mode")
send.add_argument(
    "-m", "--start-maximized", action="store_true", help="set browser in full screen")

send.set_defaults(
    which="send", email=None, password=None, headless=False, limit=20, cookies=False, incognito=False, start_maximized=False)


# usage: inb config [-h] [EMAIL] [PASSWORD]
#
#  _     _       _            _ ___         ____        _
# | |   (_)_ __ | | _____  __| |_ _|_ __   | __ )  ___ | |_
# | |   | | '_ \| |/ / _ \/ _` || || '_ \  |  _ \ / _ \| __|
# | |___| | | | |   <  __/ (_| || || | | | | |_) | (_) | |_
# |_____|_|_| |_|_|\_\___|\__,_|___|_| |_| |____/ \___/ \__|
#
#
# Command 'config' is used to add user's credentials to the database
# Adding user's credentials to the database for ever or until user deletes
# them makes it feasible for user to send invitations without entering the
# fields again and again
#
# positional arguments:
#   EMAIL       user's email address
#   PASSWORD    user's password
#
# optional arguments:
#   -h, --help  show this help message and exit


config = subparsers.add_parser(
    "config", description=get_config_description(), formatter_class=RawDescriptionHelpFormatter, help=get_config_help())

config.add_argument(
    "EMAIL", type=str, nargs="?", default=None, help="user's email address")
config.add_argument(
    "PASSWORD", type=str, nargs="?", default=None, help="user's password")

config.set_defaults(which="config", EMAIL=None, PASSWORD=None)


# usage: lbot show [-h] [-e] [-p] [keyword]
#
#  _     _       _            _ ___         ____        _
# | |   (_)_ __ | | _____  __| |_ _|_ __   | __ )  ___ | |_
# | |   | | '_ \| |/ / _ \/ _` || || '_ \  |  _ \ / _ \| __|
# | |___| | | | |   <  __/ (_| || || | | | | |_) | (_) | |_
# |_____|_|_| |_|_|\_\___|\__,_|___|_| |_| |____/ \___/ \__|
#
#
# Command 'show' prints the information stored in the database
# For example -> email, password ...
#
# positional arguments:
#   keyword
#
# optional arguments:
#   -h, --help      show this help message and exit
#   -e, --email     print user's email address
#   -p, --password  print user's password


show = subparsers.add_parser(
    "show", description=get_show_description(), formatter_class=RawDescriptionHelpFormatter, help=get_show_help())

show.add_argument("keyword", type=str, nargs="?", default=None)

show.add_argument(
    "-e", "--email", action="store_true", help="print user's email address")
show.add_argument(
    "-p", "--password", action="store_true", help="print user's password")
show.add_argument(
    "-d", "--decrypt", action="store_true", help="print information in decrypt form")

show.set_defaults(which="show", keyword=None, email=None, password=None)


# usage: lbot delete [-h] keyword
#
#  _     _       _            _ ___         ____        _
# | |   (_)_ __ | | _____  __| |_ _|_ __   | __ )  ___ | |_
# | |   | | '_ \| |/ / _ \/ _` || || '_ \  |  _ \ / _ \| __|
# | |___| | | | |   <  __/ (_| || || | | | | |_) | (_) | |_
# |_____|_|_| |_|_|\_\___|\__,_|___|_| |_| |____/ \___/ \__|
#
#
# Command 'delete' deletes the information stored in the database
# 'delete' deletes information like 'key', 'cookies' ...
#
# positional arguments:
#   keyword
#
# optional arguments:
#   -h, --help  show this help message and exit


delete = subparsers.add_parser(
    "delete", description=get_delete_description(), formatter_class=RawDescriptionHelpFormatter, help=get_delete_help())

delete.add_argument("keyword", type=str)

delete.set_defaults(which="delete", keyword=None)


# usage: lbot developer [-h] [-n] [-l] [-g] [-m] [-e]
#
#  _     _       _            _ ___         ____        _
# | |   (_)_ __ | | _____  __| |_ _|_ __   | __ )  ___ | |_
# | |   | | '_ \| |/ / _ \/ _` || || '_ \  |  _ \ / _ \| __|
# | |___| | | | |   <  __/ (_| || || | | | | |_) | (_) | |_
# |_____|_|_| |_|_|\_\___|\__,_|___|_| |_| |____/ \___/ \__|
#
#
# Command 'developer' prints the information about the author
#
# optional arguments:
#   -h, --help      show this help message and exit
#   -n, --name      print developer name
#   -l, --linkedin  print developer linkedin
#   -g, --github    print developer github
#   -m, --mobile    print developer mobile number
#   -e, --email     print developer email address


developer = subparsers.add_parser(
    "developer", description=get_developer_description(), formatter_class=RawDescriptionHelpFormatter,
    help=get_developer_help())

developer.add_argument(
    "-n", "--name", action="store_true", help="print developer name")
developer.add_argument(
    "-l", "--linkedin", action="store_true", help="print developer linkedin")
developer.add_argument(
    "-g", "--github", action="store_true", help="print developer github")
developer.add_argument(
    "-m", "--mobile", action="store_true", help="print developer mobile number")
developer.add_argument(
    "-e", "--email", action="store_true", help="print developer email address")

developer.set_defaults(
    which="developer", name=False, linkedin=False, github=False, mobile=False, email=False)

if len(sys.argv) <= 1:
    exit()

try:
    CommandHandler(parser.parse_args())
except Exception as e:
    parser.error(e)

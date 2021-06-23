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

from helpers.parser import CreateParser

from linkedin import __version__

from argparse import RawDescriptionHelpFormatter

parser = CreateParser(
    prog="lbot", description=get_lbot_description(), formatter_class=RawDescriptionHelpFormatter)

subparsers = parser.add_subparsers(help="available actions", metavar=None)

# usage: lbot send [-h] [-c] [-ngpu] {limit} ...
#
# Command 'send' sends invitation to people on linkedin.
#
# positional arguments:
#   {limit}            sets the daily connection limit
#     limit            sets the daily connection limit
#
# optional arguments:
#   -h, --help         show this help message and exit
#   -c, --cookies      uses cookies for authentication
#   -ngpu, --headless  starts chrome in headless mode

send = subparsers.add_parser(
    "send", description=get_send_description(), formatter_class=RawDescriptionHelpFormatter, help=get_send_help())

# usage: lbot send limit [-h] [limit]
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
    "-ngpu", "--headless", action="store_true", help="starts chrome in headless mode")

send.set_defaults(headless=False, cookies=False)

# usage: lbot config [-h] [-e] [-p] [value]
#
# Command 'config' is used to add user's credentials to the database
# Adding user's credentials to the database for ever or until user deletes
# them makes it feasible for user to send invitations without entering the
# fields again and again
#
# positional arguments:
#   value
#
# optional arguments:
#   -h, --help      show this help message and exit
#   -e, --email     store user's email address
#   -p, --password  stores user's password

config = subparsers.add_parser(
    "config", description=get_config_description(), formatter_class=RawDescriptionHelpFormatter, help=get_config_help())

config.add_argument("value", type=str, nargs="?", default=None)

config.add_argument(
    "-e", "--email", action="store_true", help="store user's email address")
config.add_argument(
    "-p", "--password", action="store_true", help="stores user's password")

config.set_defaults(email=False, password=False)

# usage: lbot show [-h] [-e] [-p] cookies
#
# Command 'show' prints the information stored in the database
# For example -> email, password ...
#
# positional arguments:
#   cookies
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

show.set_defaults(keyword=None, email=None, password=None)

# usage: lbot delete [-h] value
#
# Command 'delete' deletes the information stored in the database
# 'delete' deletes information like 'key', 'cookies' ...
#
# positional arguments:
#   value
#
# optional arguments:
#   -h, --help  show this help message and exit

delete = subparsers.add_parser(
    "delete", description=get_delete_description(), formatter_class=RawDescriptionHelpFormatter, help=get_delete_help())

delete.add_argument("keyword", type=str)

delete.set_defaults(keyword=None)

# usage: lbot developer [-h] [-n] [-l] [-g] [-m] [-e]
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
    name=False, linkedin=False, github=False, mobile=False, email=False)

args = parser.parse_args()

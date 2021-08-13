# MIT License
#
# Copyright (c) 2019 Creative Commons
#
# Permission is hereby granted, free of charge, to any person obtaining a
# copy of this software and associated documentation files (the "Software"),
# to deal in the Software without restriction, including without limitation
# the rights to use, copy, modify, merge, publish, distribute, sublicense,
# and/or sell copies of the Software, and to permit persons to whom the
# Software is furnished to do so, subject to the following conditions
#
# The above copyright notice and this permission notice shall be included
# in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS
# OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN 
# THE SOFTWARE.

import sys

from argparse import RawDescriptionHelpFormatter

from linkedin import __version__

from lib.handler import CommandHandler

from helpers.figlet import CreateFigletString

from helpers.parser import NARGS
from helpers.parser import ArgumentParser
from helpers.parser import OPT_ARGS_ACTION

from errors.error import EmtpyDatabaseException
from errors.error import UserCacheNotFoundException
from errors.error import CredentialsNotGivenException
from errors.error import DatabaseDoesNotExistException
from errors.error import DomainNameSystemNotResolveException


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


parser = ArgumentParser(prog="inb",
                        description=(
                             f"""{CreateFigletString("LinkedIn Bot")}\n"""
                             f"""LinkedIn Bash, version {__version__}(1)-release (lbot-{__version__})\n"""
                             """These commands are defined internally. Type '--help' to see this list\n"""
                             """Type (command) --help to know more about that command"""),
                        formatter_class=RawDescriptionHelpFormatter)

subparsers = parser.add_subparsers(help="available actions",
                                   metavar=None)


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

send = subparsers.add_parser("send",
                             description=(
                                 f"""{CreateFigletString("LinkedIn Bot")}\n"""
                                 """Command 'send' sends invitation to people on linkedin."""),
                             formatter_class=RawDescriptionHelpFormatter,
                             help=("""Command 'send' sends invitation to people on linkedin."""))

send.add_argument("-e", "--email",
                  type=str,
                  nargs=NARGS.OPTIONAL,
                  default=None,
                  help="User's email address")
send.add_argument("-p", "--password",
                  type=str,
                  nargs=NARGS.OPTIONAL,
                  default=None,
                  help="User's password")

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


limit_subparsers = send.add_subparsers(help="available actions",
                                       metavar=None)

limit = limit_subparsers.add_parser("limit",
                                    description=(
                                        f"""{CreateFigletString("LinkedIn Bot")}\n"""
                                        """Flag 'limit' is used to set the daily invitation limit\n"""
                                        """Limit must not exceed by 80 otherwise you'll be blocked for a entire\n"""
                                        """week"""),
                                    formatter_class=RawDescriptionHelpFormatter,
                                    help=("""Flag 'limit' sets the daily invitation limit"""))

limit.add_argument("limit",
                   type=int,
                   nargs=NARGS.OPTIONAL,
                   default=20)

limit.set_defaults(limit=20)


send.add_argument("-c", "--cookies",
                  action=OPT_ARGS_ACTION.STORE_TRUE,
                  help="uses cookies for authentication")
send.add_argument("-i", "--incognito",
                  action=OPT_ARGS_ACTION.STORE_TRUE,
                  help="set browser in incognito mode")
send.add_argument("-ngpu", "--headless",
                  action=OPT_ARGS_ACTION.STORE_TRUE,
                  help="starts chrome in headless mode")
send.add_argument("-m", "--start-maximized",
                  action=OPT_ARGS_ACTION.STORE_TRUE,
                  help="set browser in full screen")

send.set_defaults(which="send",
                  email=None,
                  password=None,
                  headless=False,
                  limit=20,
                  cookies=False,
                  incognito=False,
                  start_maximized=False)


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


config = subparsers.add_parser("config",
                               description=(
                                   f"""{CreateFigletString("LinkedIn Bot")}\n"""
                                   """Command 'config' is used to add user's credentials to the database\n"""
                                   """Adding user's credentials to the database for ever or until user deletes\n"""
                                   """them makes it feasible for user to send invitations without entering the\n"""
                                   """fields again and again"""),
                               formatter_class=RawDescriptionHelpFormatter,
                               help=("""Command 'config' is used to store user's credentials"""))

config.add_argument("EMAIL",
                    type=str,
                    nargs=NARGS.OPTIONAL,
                    default=None,
                    help="user's email address")
config.add_argument("PASSWORD",
                    type=str,
                    nargs=NARGS.OPTIONAL,
                    default=None,
                    help="user's password")

config.set_defaults(which="config",
                    EMAIL=None,
                    PASSWORD=None)


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


show = subparsers.add_parser("show",
                             description=(
                                 f"""{CreateFigletString("LinkedIn Bot")}\n"""
                                 """Command 'show' prints the information stored in the database\n"""
                                 """For example -> email, password ..."""),
                             formatter_class=RawDescriptionHelpFormatter,
                             help=("""Command 'show' prints the information that is in the database"""))

show.add_argument("keyword",
                  type=str,
                  nargs=NARGS.OPTIONAL,
                  default=None)

show.add_argument("-e", "--email",
                  action=OPT_ARGS_ACTION.STORE_TRUE,
                  help="print user's email address")
show.add_argument("-p", "--password",
                  action=OPT_ARGS_ACTION.STORE_TRUE,
                  help="print user's password")
show.add_argument("-d", "--decrypt",
                  action=OPT_ARGS_ACTION.STORE_TRUE,
                  help="print information in decrypt form")

show.set_defaults(which="show",
                  keyword=None,
                  email=None,
                  password=None)


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


delete = subparsers.add_parser("delete",
                               description=(
                                   f"""{CreateFigletString("LinkedIn Bot")}\n"""
                                   """Command 'delete' deletes the information stored in the database\n"""
                                   """'delete' deletes information like 'key', 'cookies' ..."""),
                               formatter_class=RawDescriptionHelpFormatter,
                               help=("""Command 'delete' deletes the information stored in the database"""))

delete.add_argument("keyword",
                    type=str)

delete.set_defaults(which="delete",
                    keyword=None)


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


developer = subparsers.add_parser("developer",
                                  description=(
                                      f"""{CreateFigletString("LinkedIn Bot")}\n"""
                                      """Command 'developer' prints the information about the author"""),
                                  formatter_class=RawDescriptionHelpFormatter,
                                  help=("""Command 'developer' prints the information about the author"""))

developer.add_argument("-n", "--name",
                       action=OPT_ARGS_ACTION.STORE_TRUE,
                       help="print developer name")
developer.add_argument("-l", "--linkedin",
                       action=OPT_ARGS_ACTION.STORE_TRUE,
                       help="print developer linkedin")
developer.add_argument("-g", "--github",
                       action=OPT_ARGS_ACTION.STORE_TRUE,
                       help="print developer github")
developer.add_argument("-m", "--mobile",
                       action=OPT_ARGS_ACTION.STORE_TRUE,
                       help="print developer mobile number")
developer.add_argument("-e", "--email",
                       action=OPT_ARGS_ACTION.STORE_TRUE,
                       help="print developer email address")

developer.set_defaults(which="developer",
                       name=False,
                       linkedin=False,
                       github=False,
                       mobile=False,
                       email=False)

if len(sys.argv) <= 1:
    exit()

# Exceptions that are not in this tuple will be printed with their stacktrace.
#
# These exceptions are custom exceptions to inform the user about their unexpected
# input or unexpected demand like when database is not present but the user wants
# to see the content of the database
exceptions = tuple([EmtpyDatabaseException,
                    UserCacheNotFoundException,
                    CredentialsNotGivenException,
                    DatabaseDoesNotExistException,
                    DomainNameSystemNotResolveException])

try:
    CommandHandler(parser.parse_args())
except exceptions as e:
    parser.error(e, usage=False)

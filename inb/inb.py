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

from lib import NARGS
from lib import ArgumentParser
from lib import OPT_ARGS_ACTION
from lib.utils import CreateFigletString
from lib.handler import Handler

from errors import EmtpyDatabaseException
from errors import CredentialsNotGivenException
from errors import DatabaseDoesNotExistException
from errors import InternetNotConnectedException
from errors import DomainNameSystemNotResolveException

#
# Usage: inb [-h] {send,connect,search,config,show,delete,developer} ...
# 
#  _       _     
# (_)_ __ | |__  
# | | '_ \| '_ \ 
# | | | | | |_) |
# |_|_| |_|_.__/ 
#    
# 
# inb Bash, version 1.51.35(1)-release (inb-1.51.35)
# These commands are defined internally. Type '--help' to see this list
# Type (command) --help to know more about that command
# 
# positional arguments:
#   {send,connect,search,config,show,delete,developer}
#                         available actions
#     send                sends invitation to people on linkedin.
#     connect             connects you with the given profile.
#     search              searches people on LinekdIn and then invites them.
#     config              used to store user's credentials
#     show                prints the information that is in the database
#     delete              deletes the information stored in the database
#     developer           prints the information about the author
# 
# optional arguments:
#   -h, --help            show this help message and exit
#

parser = ArgumentParser(prog="inb",
                        description=(
                             f"""{CreateFigletString("inb")}\n"""
                             f"""inb Bash, version {__version__}(1)-release (inb-{__version__})\n"""
                             f"""These commands are defined internally. Type '--help' to see this list\n"""
                             f"""Type (command) --help to know more about that command"""),
                        formatter_class=RawDescriptionHelpFormatter)

subparsers = parser.add_subparsers(help="available actions",
                                   metavar=None)

#
# Usage: inb send [-h] [-e [EMAIL]] [-p [PASSWORD]] [-c] [-i] [-ngpu] [-m]
#                 {limit} ...
#
#  _       _
# (_)_ __ | |__
# | | '_ \| '_ \
# | | | | | |_) |
# |_|_| |_|_.__/
#
#
# Sends invitation to people on linkedin.
#
# positional arguments:
#   {limit}               available actions
#     limit               sets the daily invitation limit
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
#

send = subparsers.add_parser("send",
                             description=(
                                 f"""{CreateFigletString("inb")}\n"""
                                 """Sends invitation to people on linkedin."""),
                             formatter_class=RawDescriptionHelpFormatter,
                             help=("""sends invitation to people on linkedin."""))

send.add_argument("-e", "--email",
                  type=str,
                  nargs=1,
                  default=None,
                  help="User's email address")
send.add_argument("-p", "--password",
                  type=str,
                  nargs=1,
                  default=None,
                  help="User's password")

#
# Usage: inb send limit [-h] [limit]
#
#  _       _
# (_)_ __ | |__
# | | '_ \| '_ \
# | | | | | |_) |
# |_|_| |_|_.__/
#
#
# It is used to set the daily invitation limit
# Limit must not exceed by 80 otherwise you'll be blocked for a entire
# week
#
# positional arguments:
#   limit
#
# optional arguments:
#   -h, --help  show this help message and exit
#

limit_subparsers = send.add_subparsers(help="available actions",
                                       metavar=None)

limit = limit_subparsers.add_parser("limit",
                                    description=(
                                        f"""{CreateFigletString("inb")}\n"""
                                        """It is used to set the daily invitation limit\n"""
                                        """Limit must not exceed by 80 otherwise you'll be blocked for a entire\n"""
                                        """week"""),
                                    formatter_class=RawDescriptionHelpFormatter,
                                    help=("""sets the daily invitation limit"""))

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

# 
# Usage: inb connect [-h] [-c] [-i] [-ngpu] [-m] profileid
# 
#  _       _     
# (_)_ __ | |__  
# | | '_ \| '_ \ 
# | | | | | |_) |
# |_|_| |_|_.__/ 
#    
# 
# Connects you with the given profile.
# 
# positional arguments:
#   profileid             Profile id of person to connect with.
# 
# optional arguments:
#   -h, --help            show this help message and exit
#   -c, --cookies         uses cookies for authentication
#   -i, --incognito       set browser in incognito mode
#   -ngpu, --headless     starts chrome in headless mode
#   -m, --start-maximized
#                         set browser in full screen
# 

connect = subparsers.add_parser("connect",
                                description=(
                                    f"""{CreateFigletString("inb")}\n"""
                                    """Connects you with the given profile."""),
                                formatter_class=RawDescriptionHelpFormatter,
                                help=("""connects you with the given profile."""))

connect.add_argument("profileid",
                     type=str,
                     nargs=1,
                     default=None,
                     help="Profile id of person to connect with.")

connect.add_argument("-c", "--cookies",
                     action=OPT_ARGS_ACTION.STORE_TRUE,
                     help="uses cookies for authentication")
connect.add_argument("-i", "--incognito",
                     action=OPT_ARGS_ACTION.STORE_TRUE,
                     help="set browser in incognito mode")
connect.add_argument("-ngpu", "--headless",
                     action=OPT_ARGS_ACTION.STORE_TRUE,
                     help="starts chrome in headless mode")
connect.add_argument("-m", "--start-maximized",
                     action=OPT_ARGS_ACTION.STORE_TRUE,
                     help="set browser in full screen")

connect.set_defaults(which="connect",
                     cookies=False,
                     headless=False,
                     incognito=False,
                     start_maximized=False)

#
# Usage: inb search [-h] [-e [EMAIL]] [-p [PASSWORD]] [-k [KEYWORD]]
#                   [-l [LOCATION]] [-t [TITLE]] [-fn [FIRST_NAME]]
#                   [-ln [LAST_NAME]] [-s [SCHOOL]] [-inds [INDUSTRY]]
#                   [-cc [CURRENT_COMPANY]] [-pl [PROFILE_LANGUAGE]] [-c] [-i]
#                   [-ngpu] [-m]
#                   {limit} ...
#
#  _       _
# (_)_ __ | |__
# | | '_ \| '_ \
# | | | | | |_) |
# |_|_| |_|_.__/
#
#
# Searches people on LinkedIn and then invites them.
#
# positional arguments:
#   {limit}               available actions
#     limit               sets the daily invitation limit
#
# optional arguments:
#   -h, --help            show this help message and exit
#   -e [EMAIL], --email [EMAIL]
#                         User's email address
#   -p [PASSWORD], --password [PASSWORD]
#                         User's password
#   -k [KEYWORD], --keyword [KEYWORD]
#                         Keyword to search for
#   -l [LOCATION], --location [LOCATION]
#                         Location(s) to search in (separated by (:) colon)
#   -t [TITLE], --title [TITLE]
#                         Match title
#   -fn [FIRST_NAME], --first-name [FIRST_NAME]
#                         Match first name
#   -ln [LAST_NAME], --last-name [LAST_NAME]
#                         Match last name
#   -s [SCHOOL], --school [SCHOOL]
#                         Person's school
#   -inds [INDUSTRY], --industry [INDUSTRY]
#                         Industry(ies) to search in (separated by (:) colon)
#   -cc [CURRENT_COMPANY], --current-company [CURRENT_COMPANY]
#                         Person's current company
#   -pl [PROFILE_LANGUAGE], --profile-language [PROFILE_LANGUAGE]
#                         Person's profile language
#   -c, --cookies         uses cookies for authentication
#   -i, --incognito       set browser in incognito mode
#   -ngpu, --headless     starts chrome in headless mode
#   -m, --start-maximized
#                         set browser in full screen
#

search = subparsers.add_parser("search",
                               description=(
                                   f"""{CreateFigletString("inb")}\n"""
                                   """Searches people on LinkedIn and then invites them."""),
                               formatter_class=RawDescriptionHelpFormatter,
                               help=("""searches people on LinekdIn and then invites them."""))

search.add_argument("-e", "--email",
                    type=str,
                    nargs=1,
                    default=None,
                    help="User's email address")
search.add_argument("-p", "--password",
                    type=str,
                    nargs=1,
                    default=None,
                    help="User's password")
search.add_argument("-k", "--keyword",
                    type=str,
                    nargs=1,
                    default=None,
                    help="Keyword to search for")
search.add_argument("-l", "--location",
                    type=str,
                    nargs=NARGS.OPTIONAL,
                    default=None,
                    help="Location(s) to search in (separated by (:) colon)")
search.add_argument("-t", "--title",
                    type=str,
                    nargs=NARGS.OPTIONAL,
                    default=None,
                    help="Match title")
search.add_argument("-fn", "--first-name",
                    type=str,
                    nargs=NARGS.OPTIONAL,
                    default=None,
                    help="Match first name")
search.add_argument("-ln", "--last-name",
                    type=str,
                    nargs=NARGS.OPTIONAL,
                    default=None,
                    help="Match last name")
search.add_argument("-s", "--school",
                    type=str,
                    nargs=NARGS.OPTIONAL,
                    default=None,
                    help="Person's school")
search.add_argument("-inds", "--industry",
                    type=str,
                    nargs=NARGS.OPTIONAL,
                    default=None,
                    help="Industry(ies) to search in (separated by (:) colon)")
search.add_argument("-cc", "--current-company",
                    type=str,
                    nargs=NARGS.OPTIONAL,
                    default=None,
                    help="Person's current company")
search.add_argument("-pl", "--profile-language",
                    type=str,
                    nargs=NARGS.OPTIONAL,
                    default=None,
                    help="Person's profile language")

#
# Usage: inb search limit [-h] [limit]
#
#  _       _
# (_)_ __ | |__
# | | '_ \| '_ \
# | | | | | |_) |
# |_|_| |_|_.__/
#
#
# It is used to set the daily invitation limit
# Limit must not exceed by 80 otherwise you'll be blocked for a entire
# week
#
# positional arguments:
#   limit
#
# optional arguments:
#   -h, --help  show this help message and exit
#

limit_subparsers = search.add_subparsers(help="available actions",
                                         metavar=None)

limit = limit_subparsers.add_parser("limit",
                                    description=(
                                        f"""{CreateFigletString("inb")}\n"""
                                        """It is used to set the daily invitation limit\n"""
                                        """Limit must not exceed by 80 otherwise you'll be blocked for a entire\n"""
                                        """week"""),
                                    formatter_class=RawDescriptionHelpFormatter,
                                    help=("""sets the daily invitation limit"""))

limit.add_argument("limit",
                   type=int,
                   nargs=NARGS.OPTIONAL,
                   default=20)

limit.set_defaults(limit=20)

search.add_argument("-c", "--cookies",
                    action=OPT_ARGS_ACTION.STORE_TRUE,
                    help="uses cookies for authentication")
search.add_argument("-i", "--incognito",
                    action=OPT_ARGS_ACTION.STORE_TRUE,
                    help="set browser in incognito mode")
search.add_argument("-ngpu", "--headless",
                    action=OPT_ARGS_ACTION.STORE_TRUE,
                    help="starts chrome in headless mode")
search.add_argument("-m", "--start-maximized",
                    action=OPT_ARGS_ACTION.STORE_TRUE,
                    help="set browser in full screen")

search.set_defaults(which="search",
                    email=None,
                    password=None,
                    keyword=None,
                    location=None,
                    title=None,
                    first_name=None,
                    last_name=None,
                    school=None,
                    industry=None,
                    current_company=None,
                    profile_language=None,
                    headless=False,
                    limit=20,
                    cookies=False,
                    incognito=False,
                    start_maximized=False)

#
# Usage: inb config [-h] [EMAIL] [PASSWORD]
#
#  _       _
# (_)_ __ | |__
# | | '_ \| '_ \
# | | | | | |_) |
# |_|_| |_|_.__/
#
#
# It is used to add user's credentials to the database
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
#

config = subparsers.add_parser("config",
                               description=(
                                   f"""{CreateFigletString("inb")}\n"""
                                   """It is used to add user's credentials to the database\n"""
                                   """Adding user's credentials to the database for ever or until user deletes\n"""
                                   """them makes it feasible for user to send invitations without entering the\n"""
                                   """fields again and again"""),
                               formatter_class=RawDescriptionHelpFormatter,
                               help=("""used to store user's credentials"""))

config.add_argument("EMAIL",
                    type=str,
                    nargs=1,
                    default=None,
                    help="user's email address")
config.add_argument("PASSWORD",
                    type=str,
                    nargs=1,
                    default=None,
                    help="user's password")

config.set_defaults(which="config",
                    EMAIL=None,
                    PASSWORD=None)

#
# Usage: inb show [-h] [-e] [-p] [-d] [keyword]
#
#  _       _
# (_)_ __ | |__
# | | '_ \| '_ \
# | | | | | |_) |
# |_|_| |_|_.__/
#
#
# It prints the information stored in the database
# For example -> email, password ...
#
# positional arguments:
#   keyword
#
# optional arguments:
#   -h, --help      show this help message and exit
#   -e, --email     print user's email address
#   -p, --password  print user's password
#   -d, --decrypt   print information in decrypt form
#

show = subparsers.add_parser("show",
                             description=(
                                 f"""{CreateFigletString("inb")}\n"""
                                 """It prints the information stored in the database\n"""
                                 """For example -> email, password ..."""),
                             formatter_class=RawDescriptionHelpFormatter,
                             help=("""prints the information that is in the database"""))

show.add_argument("keyword",
                  type=str,
                  nargs=1,
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

#
# Usage: inb delete [-h] keyword
#
#  _       _
# (_)_ __ | |__
# | | '_ \| '_ \
# | | | | | |_) |
# |_|_| |_|_.__/
#
#
# It deletes the information stored in the database
# 'delete' deletes information like 'key', 'cookies' ...
#
# positional arguments:
#   keyword
#
# optional arguments:
#   -h, --help  show this help message and exit
#

delete = subparsers.add_parser("delete",
                               description=(
                                   f"""{CreateFigletString("inb")}\n"""
                                   """It deletes the information stored in the database\n"""
                                   """'delete' deletes information like 'key', 'cookies' ..."""),
                               formatter_class=RawDescriptionHelpFormatter,
                               help=("""deletes the information stored in the database"""))

delete.add_argument("keyword",
                    type=str)

delete.set_defaults(which="delete",
                    keyword=None)

#
# Usage: inb developer [-h] [-n] [-l] [-g] [-m] [-e]
#
#  _       _
# (_)_ __ | |__
# | | '_ \| '_ \
# | | | | | |_) |
# |_|_| |_|_.__/
#
#
# It prints the information about the author
#
# optional arguments:
#   -h, --help      show this help message and exit
#   -n, --name      print developer name
#   -l, --linkedin  print developer linkedin
#   -g, --github    print developer github
#   -m, --mobile    print developer mobile number
#   -e, --email     print developer email address
#

developer = subparsers.add_parser("developer",
                                  description=(
                                      f"""{CreateFigletString("inb")}\n"""
                                      """It prints the information about the author"""),
                                  formatter_class=RawDescriptionHelpFormatter,
                                  help=("""prints the information about the author"""))

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
                    CredentialsNotGivenException,
                    DatabaseDoesNotExistException,
                    InternetNotConnectedException,
                    DomainNameSystemNotResolveException])

try:
    Handler(parser.parse_args())
except exceptions as e:
    parser.error(e, usage=False)

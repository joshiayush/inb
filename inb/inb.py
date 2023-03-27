#!/usr/bin/python3

# Copyright 2023 The inb Authors. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Command line interface for automation tool inb."""

import time
import click

import api

from api import linkedin_api, client
from api.invitation import status

try:
  from gettext import gettext as _  # pylint: disable=unused-import
except ImportError:
  _ = lambda msg: msg  # pylint: disable=unnecessary-lambda-assignment


# pylint: disable=pointless-statement
@click.group()
def Inb():
  f"""inb version {api.__version__}

  Command line utility to automate the world of LinkedIn.

  Usage:

    ./inb/inb.py search --email "username" --password "password"

  To know more:

    ./inb/inb.py search --help
  """
  pass


@click.command()
@click.option('--email',
              type=str,
              required=True,
              help=_('LinkedIn username.'))
@click.password_option('--password',
                       type=str,
                       required=True,
                       help=_('LinkedIn password.'))
@click.option('--keyword',
              type=str,
              required=True,
              help=_('Keyword to search for.'))
@click.option('--regions',
              multiple=True,
              required=False,
              help=_('Search people based on these regions.'))
@click.option('--connection-of',
              type=str,
              required=False,
              help=_('Profile id for mutual connection.'))
@click.option('--network_depths',
              multiple=True,
              required=False,
              help=_('Network depths to dig into.'))
@click.option('--network-depth',
              type=str,
              required=False,
              help=_('Network depth to dig into.'))
@click.option('--industries',
              multiple=True,
              required=False,
              help=_('Search people from these industries.'))
@click.option('--current-company',
              type=str,
              required=False,
              help=_('Search people working at this company.'))
@click.option('--profile-languages',
              multiple=True,
              required=False,
              help=_('Person profile languages.'))
@click.option('--schools',
              multiple=True,
              required=False,
              help=_('Search for profiles mentioning this school.'))
@click.option('--refresh-cookies',
              is_flag=True,
              required=False,
              help=_('Update cookies if given.'))
@click.option('--limit',
              type=int,
              required=False,
              help=_('Number of invitations to send.'))
@click.option('--debug',
              is_flag=True,
              required=False,
              help=_('Prints out debugging information at runtime.'))
def search(  # pylint: disable=invalid-name
    email: str, password: str, keyword: str, regions: list, connection_of: str,
    network_depths: list, network_depth: str, industries: list,
    current_company: str, profile_languages: list, schools: list,
    refresh_cookies: bool, limit: int, debug: bool) -> None:
  """Searches for the specific keyword given and sends invitation to them.

  Usage:

    ./inb/inb.py search --email "username" --password "password"
      --keyword "Software developer"

  inb supports cookie based authentication - use --refresh-cookies in case you
  encounter error LinkedInSessionExpiredException.

    ./inb/inb.py search --email "username" --password "password"
      --keyword "Software developer" --refersh-cookies

  Also, for security purpose you can omit the --pasword argument over the
  command-line and later on executing the tool you'll be prompted to enter your
  password which will be hidden even after pressing keystrokes.

    ./inb/inb.py search --email "username" --keyword "Software developer"
      --refersh-cookies
  """
  linkedin = linkedin_api.LinkedIn(email,
                                   password,
                                   authenticate=True,
                                   debug=debug,
                                   refresh_cookies=refresh_cookies)

  count = 0
  search_results = linkedin.search_people(keywords=keyword,
                                          regions=regions,
                                          connection_of=connection_of,
                                          network_depths=network_depths,
                                          network_depth=network_depth,
                                          industries=industries,
                                          current_company=current_company,
                                          profile_languages=profile_languages,
                                          schools=schools)
  start_time = time.time()
  for result in search_results:
    if limit is not None and count >= limit:
      break

    person = status.Person(
        name=result['name'],
        occupation=result['jobtitle'],
        location=result['location'],
        profileid=result['public_id'],
        profileurl=f'{client.Client.LINKEDIN_BASE_URL}/in/{result["public_id"]}'
    )
    invitation = status.Invitation()
    if linkedin.add_connection(profile_pub_id=result['public_id'],
                               message='',
                               profile_urn=result['urn_id']) is True:
      invitation.display_invitation_status_on_console(person=person,
                                                      status='sent',
                                                      start_time=start_time)
      count += 1
    else:
      invitation.display_invitation_status_on_console(person=person,
                                                      status='failed',
                                                      start_time=start_time)


Inb.add_command(search)

if __name__ == '__main__':
  Inb()

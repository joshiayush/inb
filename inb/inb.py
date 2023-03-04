#!/usr/bin/python3

# Copyright 2021, joshiayus Inc.
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are
# met:
#
#     * Redistributions of source code must retain the above copyright
# notice, this list of conditions and the following disclaimer.
#     * Redistributions in binary form must reproduce the above
# copyright notice, this list of conditions and the following disclaimer
# in the documentation and/or other materials provided with the
# distribution.
#     * Neither the name of joshiayus Inc. nor the names of its
# contributors may be used to endorse or promote products derived from
# this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
# "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
# LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR
# A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT
# OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
# SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT
# LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
# DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY
# THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
# (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
# OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

"""Command line interface for automation tool inb."""

import time
import click

from api import linkedin_api, client
from api.invitation import status

try:
  from gettext import gettext as _  # pylint: disable=unused-import
except ImportError:
  _ = lambda msg: msg  # pylint: disable=unnecessary-lambda-assignment


@click.group()
def Inb():
  """inb version 1.0.0

  Command line utility to automate the world of LinkedIn.

  Quick start:

    python3 inb/inb.py send --email "username" --password "password"
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
              type=list,
              required=False,
              help=_('Search people based on these regions.'))
@click.option('--connection-of',
              type=str,
              required=False,
              help=_('Profile id for mutual connection.'))
@click.option('--network_depths',
              type=list,
              required=False,
              help=_('Network depths to dig into.'))
@click.option('--network-depth',
              type=str,
              required=False,
              help=_('Network depth to dig into.'))
@click.option('--industries',
              type=list,
              required=False,
              help=_('Search people from these industries.'))
@click.option('--current-company',
              type=str,
              required=False,
              help=_('Search people working at this company.'))
@click.option('--profile-languages',
              type=list,
              required=False,
              help=_('Person profile languages.'))
@click.option('--schools',
              type=list,
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
    email: str, password: str, keyword: str, regions: str, connection_of: str,
    network_depths: list, network_depth: str, industries: list,
    current_company: str, profile_languages: list, schools: list,
    refresh_cookies: bool, limit: int, debug: bool) -> None:
  """Searches for the specific keyword given and sends invitation to them.

  Usage:

    python3 inb/inb.py search --email "username" --password "password"
        --keyword "Software developer"
  """
  linkedin = linkedin_api.LinkedIn(username=email,
                                   password=password,
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

    public_id = result['public_id']
    person = status.Person(
        name=result['name'],
        occupation=result['jobtitle'],
        location=result['location'],
        profileid=result['public_id'],
        profileurl=f'{client.Client.LINKEDIN_BASE_URL}/in/{public_id}')
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

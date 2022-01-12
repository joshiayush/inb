#!/usr/bin/python3

# pylint: disable=missing-module-docstring

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

from __future__ import annotations

import sys
import click

from linkedin import settings

try:
  from gettext import gettext as _  # pylint: disable=unused-import
except ImportError:
  _ = lambda msg: msg


def _SendAndSearchCommandCommonOptions(f: function) -> function:  # pylint: disable=undefined-variable
  """Decorator provides common command line flags for command `send` and
  `search`.

  Use this decorator to pass `--limit`, `--headless`, `--versbose` flags from
  command line.

  ```shell
  python3 inb/inb.py send --email "username" --password "password" --headless
    --maximized
  ```

  Args:
    func: Function to decorate.

  Returns:
    Function attached with common command line flags.
  """
  f = click.option(
      '--limit',
      type=int,
      default=20,
      help=_('Overrides the default limit of 20 by passing an explicit'
             ' limit number.'))(f)
  f = click.option('--headless',
                   is_flag=True,
                   help=_('Disables GPU support for Chromedriver.'))(f)
  f = click.option(
      '--maximized',
      is_flag=True,
      help=_(
          'Maximizes the Chrome window even if it is in headless mode.'))(f)
  f = click.option(
      '--debug',
      is_flag=True,
      help=_('Prints out debugging information at runtime.'))(f)
  return f


@click.group()
def Inb():
  """inb version 1.0.0

  Command line utility to automate the world of LinkedIn.

  Quick start:

    python3 inb/inb.py send --email "username" --password "password"
  """
  pass


@click.command()
@click.option('--email', type=str, required=True, help=_('LinkedIn username.'))
@click.password_option('--password',
                       type=str,
                       required=True,
                       help=_('LinkedIn password.'))
@_SendAndSearchCommandCommonOptions
def send(  # pylint: disable=invalid-name
    email: str, password: str, limit: int, headless: bool, maximized: bool,
    debug: bool) -> None:
  """Sends invitations on LinkedIn to people in your MyNetwork page.

  Usage:

    python3 inb/inb.py send --email "username" --password "password"

  If you want to open Chrome browser in its full size use\n
  '--maximized' over the command line.

    python3 inb/inb.py send --email "username" --password "password"
        --maximized

  If you want to send invitations without opening Chrome browser\n
  use '--headless' flag over the command line.

    python3 inb/inb.py send --email "username" --password "password"
        --headless

  Note: When running with '--headless' also provide '--maximized'\n
  to capture the complete view otherwise the bot will complain
  about 'No such element'.

    python3 inb/inb.py send --email "username" --password "password"
        --headless --maximized

  Controlling Invitation Limit:

  By default the bot will send invitations to 20 people on\n
  LinkedIn if you provide a plain command over the command
  line.

    python3 inb/inb.py send --email "username" --password "password"

  In order to override the default behaviour you need to pass the\n
  flag '--limit' to provide the number of invitations the bot
  should send.

    python3 inb/inb.py send --email "username" --password "password"
        --limit 40

  Note: The limit should not exceed by 80 and we recommend a limit\n
  of 40 every time you run this bot.
  """
  if debug:
    settings.TurnOnLoggingToStream()
  from linkedin import driver  # pylint: disable=import-outside-toplevel
  chromedriver_options = [
      driver.CHROMEDRIVER_OPTIONS['disable-infobars'],
      driver.CHROMEDRIVER_OPTIONS['enable-automation']
  ]
  if headless:
    chromedriver_options = [
        *chromedriver_options,
        driver.CHROMEDRIVER_OPTIONS['headless'] if sys.platform
        in ('linux', 'darwin') else driver.CHROMEDRIVER_OPTIONS['disable-gpu']
    ]
  if maximized:
    chromedriver_options = [
        *chromedriver_options, driver.CHROMEDRIVER_OPTIONS['start-maximized']
    ]
  try:
    driver.GChromeDriverInstance.initialize(settings.ChromeDriverAbsolutePath(),
                                            chromedriver_options)
    from linkedin import (login, connect)  # pylint: disable=import-outside-toplevel
    login.LinkedIn.login(email, password)
    linkedinconnect = connect.LinkedInConnect(max_connection_limit=limit)
    linkedinconnect.get_my_network_page()
    linkedinconnect.send_connection_requests()
  except Exception as exc:  # pylint: disable=broad-except
    if debug:
      raise exc
    click.echo(f'{type(exc).__name__}: {str(exc)}', None, False, True)
  finally:
    driver.DisableGlobalChromeDriverInstance()


@click.command()
@click.option('--email', type=str, required=True, help=_('LinkedIn username.'))
@click.password_option('--password',
                       type=str,
                       required=True,
                       help=_('LinkedIn password.'))
@click.option('--keyword',
              type=str,
              required=True,
              help=_('Keyword to search for.'))
@click.option('--location',
              type=list,
              required=False,
              help=_('Location to search for.'))
@_SendAndSearchCommandCommonOptions
def search(  # pylint: disable=invalid-name
    email: str, password: str, keyword: str, location: str, limit: int,
    headless: bool, maximized: bool, debug: bool) -> None:
  """Searches for the specific keyword given and sends invitation to them.

  Usage:

    python3 inb/inb.py search --email "username" --password "password"
        --keyword "Software developer"

  If you want to open Chrome browser in its full size use\n
  '--maximized' over the command line.

    python3 inb/inb.py search --email "username" --password "password"
        --keyword "Software developer" --maximized

  If you want to send invitations without opening Chrome browser\n
  use '--headless' flag over the command line.

    python3 inb/inb.py send --email "username" --password "password"
        --keyword "Software developer" --headless

  Note: When running with '--headless' also provide '--maximized'\n
  to capture the complete view otherwise the bot will complain
  about 'No such element'.

    python3 inb/inb.py send --email "username" --password "password"
        --keyword "Software developer" --headless --maximized

  Controlling Invitation Limit:

  By default the bot will send invitations to 20 people on\n
  LinkedIn if you provide a plain command over the command
  line.

    python3 inb/inb.py send --email "username" --password "password"
        --keyword "Software developer"

  In order to override the default behaviour you need to pass the\n
  flag '--limit' to provide the number of invitations the bot
  should send.

    python3 inb/inb.py send --email "username" --password "password"
        --keyword "Software developer" --limit 40

  Note: The limit should not exceed by 80 and we recommend a limit\n
  of 40 every time you run this bot.
  """
  if debug:
    settings.TurnOnLoggingToStream()
  from linkedin import driver  # pylint: disable=import-outside-toplevel
  chromedriver_options = [
      driver.CHROMEDRIVER_OPTIONS['disable-infobars'],
      driver.CHROMEDRIVER_OPTIONS['enable-automation']
  ]
  if headless:
    chromedriver_options = [
        *chromedriver_options,
        driver.CHROMEDRIVER_OPTIONS['headless'] if sys.platform
        in ('linux', 'darwin') else driver.CHROMEDRIVER_OPTIONS['disable-gpu']
    ]
  if maximized:
    chromedriver_options = [
        *chromedriver_options, driver.CHROMEDRIVER_OPTIONS['start-maximized']
    ]
  try:
    driver.GChromeDriverInstance.initialize(settings.ChromeDriverAbsolutePath(),
                                            chromedriver_options)
    from linkedin import (login, connect)  # pylint: disable=import-outside-toplevel
    login.LinkedIn.login(email, password)
    linkedinsearchconnect = connect.LinkedInSearchConnect(
        keyword=keyword,
        location=''.join(location).split(',') if location else None,
        industry=None,
        title=None,
        firstname=None,
        lastname=None,
        school=None,
        current_company=None,
        profile_language=None,
        max_connection_limit=limit)
    linkedinsearchconnect.get_search_results_page()
    linkedinsearchconnect.send_connection_requests()
  except Exception as exc:  # pylint: disable=broad-except
    if debug:
      raise exc
    click.echo(f'{type(exc).__name__}: {str(exc)}', None, False, True)
  finally:
    driver.DisableGlobalChromeDriverInstance()


Inb.add_command(send)
Inb.add_command(search)

if __name__ == '__main__':
  Inb()

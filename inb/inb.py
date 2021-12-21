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

import click

from linkedin import (login, settings, connect)


def send_and_search_common_options(func: function) -> function:  # pylint: disable=undefined-variable
  """Decorator provides common command line flags for command `send` and
  `search`.

  Use this decorator to pass `--limit`, `--headless`, `--versbose` flags from
  command line.

  Args:
    func: Function to decorate.

  Returns:
    Function attached with common command line flags.
  """
  func = click.option(
      '--limit',
      type=int,
      default=20,
      help=('Overrides the default limit of 20 by passing an explicit'
            ' limit number.'))(func)
  func = click.option('--headless',
                      is_flag=True,
                      help=('Disables GPU support for Chromedriver.'))(func)
  func = click.option(
      '--maximized',
      is_flag=True,
      help=(
          'Maximizes the Chrome window even if it is in headless mode.'))(func)
  func = click.option('--verbose',
                      is_flag=True,
                      help=('Prints out extra information at runtime.'))(func)
  return func


@click.group()
def inb():
  """inb version 1.0.0

  Command line utility to automate the world of LinkedIn.

  Quick start:

    python3 inb/inb.py send --email "username" --password "password"
  """
  pass


@click.command()
@click.option('--email', type=str, required=True, help='LinkedIn username.')
@click.password_option('--password',
                       type=str,
                       required=True,
                       help='LinkedIn password.')
@send_and_search_common_options
def send(email: str, password: str, limit: int, headless: bool, maximized: bool,
         verbose: bool) -> None:
  """Sends invitations on LinkedIn to people in your MyNetwork page.

  Usage:

    python3 inb/inb.py send --email "username" --password "password"

  If you want to open Chrome browser in its full size use '--maximized' over
  the command line.

    python3 inb/inb.py send --email "username" --password "password" \\
        --maximized

  If you want to send invitations without opening Chrome browser use
  '--headless' flag over the command line.

    python3 inb/inb.py send --email "username" --password "password" \\
        --headless

  Note: When running with '--headless' also provide '--maximized' to capture
  the complete view otherwise the bot will complain about 'No such element'.

    python3 inb/inb.py send --email "username" --password "password" \\
        --headless --maximized

  Controlling Invitation Limit:

  By default the bot will send invitations to 20 people onn LinkedIn if you
  provide a plain command over the command line.

    python3 inb/inb.py send --email "username" --password "password"

  In order to override the default behaviour you need to pass the flag '--limit'
  to provide the number of invitations the bot should send.

    python3 inb/inb.py send --email "username" --password "password" --limit 40

  Note: The limit should not exceed by 80 and we recommend a limit of 40 every
  time you run this bot.
  """
  if verbose:
    settings.TurnOnLoggingToStream()
  from linkedin import driver  # pylint: disable=import-outside-toplevel
  chromedriver_options = []
  if headless:
    chromedriver_options.append(driver.CHROMEDRIVER_OPTIONS['headless'])
  if maximized:
    chromedriver_options.append(driver.CHROMEDRIVER_OPTIONS['start-maximized'])
  driver.GChromeDriverInstance.initialize(settings.ChromeDriverAbsPath(),
                                          chromedriver_options)
  login.LinkedIn.login(email, password)
  connect.LinkedInConnect(limit).send_invitations()


@click.command()
@click.option('--email', type=str, required=True, help='LinkedIn username.')
@click.password_option('--password',
                       type=str,
                       required=True,
                       help='LinkedIn password.')
@click.option('--keyword',
              type=str,
              required=True,
              help='Keyword to search for.')
@click.option('--location',
              type=str,
              required=False,
              help='Location to search for.')
@send_and_search_common_options
def search(email: str, password: str, keyword: str, location: str, limit: int,
           headless: bool, maximized: bool, verbose: bool) -> None:
  """Searches for the specific keyword given and sends invitation to them.

  Usage:

    python3 inb/inb.py search --email "username" --password "password" \\
        --keyword "keyword"

  Note: When running with '--headless' also provide '--maximized' to capture
  the complete view.
  """
  if verbose:
    settings.TurnOnLoggingToStream()
  from linkedin import driver  # pylint: disable=import-outside-toplevel
  chromedriver_options = []
  if headless:
    chromedriver_options.append(driver.CHROMEDRIVER_OPTIONS['headless'])
  if maximized:
    chromedriver_options.append(driver.CHROMEDRIVER_OPTIONS['start-maximized'])
  driver.GChromeDriverInstance.initialize(settings.ChromeDriverAbsPath(),
                                          chromedriver_options)
  login.LinkedIn.login(email, password)


inb.add_command(send)
inb.add_command(search)

if __name__ == '__main__':
  inb()

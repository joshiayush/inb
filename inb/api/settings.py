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

"""A configuration file for all the directory paths and logging settings."""

import os
import pathlib

USER_HOME_DIR = pathlib.Path.home()
INB_USER_DIR = USER_HOME_DIR / '.inb/'
INB_COOKIE_DIR = INB_USER_DIR / 'cookies/'
INB_LOG_DIR = INB_USER_DIR / 'logs'

# Variable's value decides whether logging to stream is allowed in the entire
# project.
LOGGING_TO_STREAM_ENABLED = False

# We want to create the log directory if it does not exists otherwise the file
# handlers for loggers used in other modules will complain about its absence.
if not os.path.exists(INB_LOG_DIR):
  os.mkdir(INB_LOG_DIR)

LOG_FORMAT_STR = (
    '%(asctime)s:%(name)s:%(levelname)s:%(funcName)s\n%(message)s')

INB_VERSION = '1.0.0'

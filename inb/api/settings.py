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

"""A configuration file for all the directory paths and logging settings."""

import os
import pathlib

USER_HOME_DIR = pathlib.Path.home()
INB_USER_DIR = USER_HOME_DIR / '.inb/'
INB_COOKIE_DIR = INB_USER_DIR / 'cookies/'
INB_LOG_DIR = INB_USER_DIR / 'logs'

# Variable's value decides whether logging to stream is allowed
# in the entire project.
LOGGING_TO_STREAM_ENABLED = False

# Create the required directories for storing bot related data.
if not os.path.exists(INB_USER_DIR):
  os.makedirs(INB_USER_DIR)
if not os.path.exists(INB_COOKIE_DIR):
  os.makedirs(INB_COOKIE_DIR)

# We want to create the log directory if it does not exists
# otherwise the file handlers for loggers used in other modules
# will complain about its absence.
if not os.path.exists(INB_LOG_DIR):
  os.makedirs(INB_LOG_DIR)

LOG_FORMAT_STR = (
    '%(asctime)s:%(name)s:%(levelname)s:%(funcName)s\n%(message)s')

INB_VERSION = '1.0.0'

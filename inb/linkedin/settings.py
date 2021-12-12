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

import os
import pathlib

LOG_DIR_PATH = pathlib.Path(__file__).resolve().parent.parent.parent / 'logs'

# We want to create the log directory if it does not exists otherwise the
# file handlers for loggers used in other modules will complain about its
# absence.
if not os.path.exists(LOG_DIR_PATH):
  os.mkdir(LOG_DIR_PATH)

LOG_FORMAT_STR = '%(asctime)s:%(name)s:%(levelname)s:%(filename)s:%(funcName)s:%(message)s'  # pylint: disable=line-too-long

INB_VERSION = '1.0.0'


def _ChromeDriverAbsPath() -> str:
  dir_path = os.path.dirname(os.path.abspath(__file__))
  last_inb_indx = dir_path.rfind('inb')
  return os.path.join(dir_path[:last_inb_indx], 'driver/chromedriver')


CHROME_DRIVER_ABS_PATH = _ChromeDriverAbsPath()

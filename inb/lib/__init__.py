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

from .algo import levenshtein

from .parser import NARGS
from .parser import ArgumentParser
from .parser import OPT_ARGS_ACTION

from .utils import ping
from .utils import _type
from .utils import is_int
from .utils import is_str
from .utils import is_none
from .utils import is_empty
from .utils import is_present
from .utils import Terminal
from .utils import Validator
from .utils import disable_logging
from .utils import InbValidator
from .utils import CreateFigletString

__all__ = ["DRIVER_PATH"]


def chromedriver_abs_path() -> str:
    _dir_path = os.path.dirname(os.path.abspath(__file__))
    _last_inb_indx = _dir_path.rfind("inb")
    return os.path.join(_dir_path[:_last_inb_indx], "driver/chromedriver")


DRIVER_PATH = chromedriver_abs_path()
__project_name__ = "inb"
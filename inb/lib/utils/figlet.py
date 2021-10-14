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

import pyfiglet


def CreateFigletString(text: str, font: str = "standard", **kwargs) -> pyfiglet.FigletString:
  """Function CreateFigletString() takes ASCII text and returns it in ASCII art fonts. 
  figlet_format method convert ASCII text into ASCII art fonts.

  :Args:
      - text: ASCII text to convert to ASCII art fonts
      - font: font type { "standard", "slant", "3-d", "3x5", "5lineoblique", "alphabet", 
          "banner3-D", "doh", "isometric1", "letters", "alligator", "dotmatrix", "bubble", 
          "bulbhead", "digital" } for more fonts see http://www.figlet.org/fontdb.cgi
      - kwargs: keyword arguments

  :Returns:
      - ASCII art font
  """
  return pyfiglet.figlet_format(text=text, font=font, **kwargs)

"""
This module provides service to parse template messages given by the user.

SUPPORTED TEMPLATE FILES
~~~~~~~~~~~~~~~~~~~~~~~~

- .txt

SUPPORTED LANGUAGES
~~~~~~~~~~~~~~~~~~~

- English, United States

  :author: Ayush Joshi, ayush854032@gmail.com
  :proposer: Bruce Lewin, bruce.lewin@fourgroups.com
  :copyright: Copyright (c) 2019 Creative Commons
  :license: MIT License, see license for details
"""

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

# from __future__ imports must occur at the beginning of the file. DO NO CHANGE!
from __future__ import annotations

from typing import Dict

import os
import datetime
import language_tool_python

from errors import (
  TemplateFileNotSupportedException,
  TemplateMessageLengthExceededException,
)

NAMES = [
    '{{name}}', '{{first_name}}', '{{last_name}}', '{{my_name}}',
    '{{my_first_name}}', '{{my_last_name}}', '{{my_company_name}}',
    '{{current_company}}', ]

OTHERS = [
    '{{keyword}}', '{{location}}', '{{industry}}', '{{title}}',
    '{{school}}', '{{profile_language}}', '{{my_position}}',
    '{{position}}', '{{year}}', ]

SUPPORTED_TEMP_FILES = ['.txt', ]

DEFAULT_LANG = 'en-US'


class Template:
  def __init__(
          self: Template, data: Dict[str, str],
          message: str) -> None:
    if data:
      self.set_data(data)
    else:
      Exception("Argument 'data' cannot be a NoneType object!")
    if os.path.isfile(message):
      self._message = self.load_message(message)
    else:
      self._message = message
    self._language_tool = language_tool_python.LanguageTool(
        language=DEFAULT_LANG)

  def set_data(self: Template, data: Dict[str, str]) -> None:
    self.data = {}
    self.data = {**self.data, **{'{{name}}': data.pop('name', None)}}
    self.data = {
        **self.data, **
        {'{{first_name}}': data.pop('first_name', None)}}
    self.data = {
        **self.data, **
        {'{{last_name}}': data.pop('last_name', None)}}
    self.data = {**self.data, **
                 {'{{my_name}}': data.pop('my_name', None)}}
    self.data = {
        **self.data, **
        {'{{my_first_name}}': data.pop('my_first_name', None)}}
    self.data = {
        **self.data, **
        {'{{my_last_name}}': data.pop('my_last_name', None)}}
    self.data = {**self.data, **
                 {'{{keyword}}': data.pop('keyword', None)}}
    self.data = {
        **self.data, **
        {'{{location}}': data.pop('location', None)}}
    self.data = {
        **self.data, **
        {'{{industry}}': data.pop('industry', None)}}
    self.data = {**self.data, **
                 {'{{title}}': data.pop('title', None)}}
    self.data = {**self.data, **
                 {'{{school}}': data.pop('school', None)}}
    self.data = {
        **self.data, **
        {'{{current_company}}': data.pop('current_company', None)}}
    self.data = {
        **self.data, **
        {'{{profile_language}}': data.pop(
            'profile_language', None)}}
    self.data = {
        **self.data, **
        {'{{my_position}}': data.pop('my_position', None)}}
    self.data = {
        **self.data, **
        {'{{my_company_name}}': data.pop('my_company_name', None)}}
    self.data = {
        **self.data, **
        {'{{position}}': data.pop('position', None)}}
    self.data = {
        **self.data, **
        {'{{year}}': data.pop(
            'year', str(datetime.datetime.now().year))}}

  @staticmethod
  def load_message(path: str) -> str:
    for ext in SUPPORTED_TEMP_FILES:
      if not path.endswith(ext):
        raise TemplateFileNotSupportedException(
            'Template file %(file)s is not supported!' %
            {'file': path})
      else:
        break
    with open(path, 'r') as template_file:
      message = template_file.read()
    return message

  def parse(self: Template) -> str:
    for var in OTHERS:
      if self.data[var]:
        self._message = self._message.replace(var, self.data[var])
    self._message = self._language_tool.correct(self._message)
    for var in NAMES:
      if self.data[var]:
        self._message = self._message.replace(var, self.data[var])
    return self._message

  def read(self: Template) -> str:
    message = self.parse()
    if len(self._message) > 300:
      raise TemplateMessageLengthExceededException(
          'Personalized message length cannot exceed by 300, you gave %(characters)s characters'
          % {'characters': len(self._message)})
    return message

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
import json
import random
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
          self: Template, message_template: str,
          *, grammar_check: bool = True) -> None:
    if os.path.isfile(message_template):
      self._message_template = self.load_message(message_template)
    else:
      self._message_template = message_template
    self._enable_language_tool = grammar_check
    if self._enable_language_tool:
      self._language_tool = language_tool_python.LanguageTool(
          language=DEFAULT_LANG)

  def set_data(self: Template, data: Dict[str, str]) -> None:
    self._data = {}
    self._data = {**self._data, **{'{{name}}': data.pop('name', None)}}
    self._data = {**self._data, **{'{{first_name}}': data.pop('first_name', None)}}
    self._data = {**self._data, **{'{{last_name}}': data.pop('last_name', None)}}
    self._data = {**self._data, **{'{{my_name}}': data.pop('my_name', None)}}
    self._data = {**self._data, **{'{{my_first_name}}': data.pop('my_first_name', None)}}
    self._data = {**self._data, **{'{{my_last_name}}': data.pop('my_last_name', None)}}
    self._data = {**self._data, **{'{{keyword}}': data.pop('keyword', None)}}
    self._data = {**self._data, **{'{{location}}': data.pop('location', None)}}
    self._data = {**self._data, **{'{{industry}}': data.pop('industry', None)}}
    self._data = {**self._data, **{'{{title}}': data.pop('title', None)}}
    self._data = {**self._data, **{'{{school}}': data.pop('school', None)}}
    self._data = {**self._data, **{'{{current_company}}': data.pop('current_company', None)}}
    self._data = {**self._data, **{'{{profile_language}}': data.pop('profile_language', None)}}
    self._data = {**self._data, **{'{{my_position}}': data.pop('my_position', None)}}
    self._data = {**self._data, **{'{{my_company_name}}': data.pop('my_company_name', None)}}
    self._data = {**self._data, **{'{{position}}': data.pop('position', None)}}
    self._data = {**self._data, **{'{{year}}': data.pop('year', str(datetime.datetime.now().year))}}

  @staticmethod
  def load_message(path: str) -> str:
    unmatched_temp_files_count = 0
    for ext in SUPPORTED_TEMP_FILES:
      if not path.endswith(ext):
        unmatched_temp_files_count += 1
      else:
        break
    if unmatched_temp_files_count == len(SUPPORTED_TEMP_FILES):
      raise TemplateFileNotSupportedException(
          'Template file %(file)s is not supported!' %
          {'file': path})
    with open(path, 'r') as template_file:
      message = template_file.read()
    return message

  def parse(self: Template) -> str:
    def common_connection_request_random_choice() -> str:
      abspath_ = os.path.abspath(__file__)
      with open(os.path.join(abspath_[:abspath_.find(__file__):], 'templates.json')) as file:
        data = json.dump(file)
        message = random.choice(data['template_common_connection_request'])
      return message
    def check_if_templ_variable_missing(var: str) -> bool:
      nonlocal self
      return self._data[var] is None and self._message_template.find(var) > -1
    for var in OTHERS:
      if self._data[var]:
        self._message_template = self._message_template.replace(var, self._data[var])
      elif check_if_templ_variable_missing(var):
        self._message_template = common_connection_request_random_choice()
        return self.parse()
    if self._enable_language_tool:
      self._message_template = self._language_tool.correct(self._message_template)
    for var in NAMES:
      if self._data[var]:
        self._message_template = self._message_template.replace(var, self._data[var])
      elif check_if_templ_variable_missing(var):
        self._message_template = common_connection_request_random_choice()
        return self.parse()
    return self._message_template

  def read(self: Template) -> str:
    message = self.parse()
    if len(self._message_template) > 300:
      raise TemplateMessageLengthExceededException(
          'Personalized message length cannot exceed by 300, you gave %(characters)s characters'
          % {'characters': len(self._message_template)})
    return message

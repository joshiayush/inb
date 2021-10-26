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

from errors import (
  TemplateFileException,
  TemplateFileNotSupportedException,
  TemplateMessageLengthExceededException,
)

MY_NAMES = [
    '{{my_name}}', '{{my_first_name}}', '{{my_last_name}}', 
    '{{my_company_name}}', '{{my_position}}', ]

NAMES = [
    '{{name}}', '{{first_name}}', '{{last_name}}', 
    '{{current_company}}', *MY_NAMES, ]

OTHERS = [
    '{{keyword}}', '{{location}}', '{{industry}}', '{{title}}',
    '{{school}}', '{{profile_language}}', '{{my_position}}',
    '{{position}}', '{{year}}', ]

SUPPORTED_TEMP_FILES = ['.txt', ]

DEFAULT_LANG = 'en-US'

VAR_BEGN_BLK = 'VARIABLE BEGIN:'
VAR_END_BLK = 'VARIABLE END;'
TEMPL_BEGN_BLK = 'TEMPLATE BEGIN:'
TEMPL_END_BLK = 'TEMPLATE END;'

TEMPL_AVAIL = [
    'template_business', 'template_sales', 'template_real_estate', 
    'template_creative_industry', 'template_hr', 'template_include_industry',
    'template_ben_franklin', 'template_virtual_coffee', 
    'template_common_connection_request', ]

TEMPL_FILE_PATH = os.path.join(os.path.abspath(__file__)[0:os.path.abspath(__file__).find('template.py'):], 'templates.json')


class Template:
  def __init__(
          self: Template, message_template: str,
          *, var_template: str, grammar_check: bool = True,
          use_template: str = None) -> None:
    if message_template is None:
      if use_template is None:
        return
      else:
          self._message = self.get_template_by_name(use_template)
          if use_template == 'template_common_connection_request':
            self._message = random.choice(self._message)
    elif os.path.isfile(message_template):
      self._message = self.load_message(message_template)
    else:
      self._message = message_template
    self.var_template = var_template
    self._enable_language_tool = grammar_check
    if self._enable_language_tool:
      import language_tool_python
      self._language_tool = language_tool_python.LanguageTool(
          language=DEFAULT_LANG)

  @staticmethod
  def get_template_by_name(name: str) -> str:
    if not name in TEMPL_AVAIL:
      raise TemplateFileException(
        f"Invalid template! Use any of these {TEMPL_AVAIL}")
    else:
      with open(TEMPL_FILE_PATH, 'r') as templ_file:
        data = json.load(templ_file)
      return data[name]

  def set_data(self: Template, data: Dict[str, str]) -> None:
    self._data = {}
    self._data = {**self._data, **{'{{name}}': data.pop('name', None)}}
    self._data = {**self._data, **{'{{first_name}}': data.pop('first_name', None)}}
    self._data = {**self._data, **{'{{last_name}}': data.pop('last_name', None)}}
    self._data = {**self._data, **{'{{keyword}}': data.pop('keyword', None)}}
    self._data = {**self._data, **{'{{location}}': data.pop('location', None)}}
    self._data = {**self._data, **{'{{industry}}': data.pop('industry', None)}}
    self._data = {**self._data, **{'{{title}}': data.pop('title', None)}}
    self._data = {**self._data, **{'{{school}}': data.pop('school', None)}}
    self._data = {**self._data, **{'{{current_company}}': data.pop('current_company', None)}}
    self._data = {**self._data, **{'{{profile_language}}': data.pop('profile_language', None)}}
    self._data = {**self._data, **{'{{position}}': data.pop('position', None)}}
    self._data = {**self._data, **{'{{year}}': data.pop('year', str(datetime.datetime.now().year))}}

    if self.var_template is not None and os.path.isfile(self.var_template):
      self.load_variable(self.var_template)

  @staticmethod
  def check_if_file_is_supported(path: str) -> bool:
    unmatched_temp_files_count = 0
    for ext in SUPPORTED_TEMP_FILES:
      if not path.endswith(ext):
        unmatched_temp_files_count += 1
      else:
        break
    if unmatched_temp_files_count == len(SUPPORTED_TEMP_FILES):
      return False
    return True

  @staticmethod
  def load_message(path: str) -> str:
    if Template.check_if_file_is_supported(path) is False:
      raise TemplateFileNotSupportedException(
          'Template file %(file)s is not supported!' %
          {'file': path})
    with open(path, 'r') as templ_file:
      message = templ_file.read()
    return message[message.find(TEMPL_BEGN_BLK)+len(TEMPL_BEGN_BLK):message.find(TEMPL_END_BLK):]

  def load_variable(self: Template, path: str) -> str:
    if self.check_if_file_is_supported(path) is False:
      raise TemplateFileNotSupportedException(
          'Template file %(file)s is not supported!' %
          {'file': path})
    with open(path, 'r') as templ_file:
      variables = templ_file.read()
    variables = variables[variables.find(VAR_BEGN_BLK)+len(VAR_BEGN_BLK):variables.find(VAR_END_BLK):]
    variables = variables.split('\n')
    for var in variables:
      if var == '':
        continue
      var_, val = var.split('=')
      var_ = var_.strip()
      if var_ in MY_NAMES:
        self._data = {**self._data, **{var_: val.strip()}}
      else:
        raise TemplateFileException(
          f"Variables other than {MY_NAMES} are not currently supported, you gave {var_}!")

  def parse(self: Template) -> str:
    def common_connection_request_random_choice() -> str:
      with open(TEMPL_FILE_PATH, 'r') as file:
        data = json.load(file)
        message = random.choice(data['template_common_connection_request'])
      return message
    def check_if_templ_variable_missing(var: str) -> bool:
      nonlocal self
      return var in self._data and self._data[var] is None and self._message.find(var) > -1
    message = self._message
    for var in OTHERS:
      if var in self._data and self._data[var]:
        message = self._message.replace(var, self._data[var])
      elif check_if_templ_variable_missing(var):
        message = common_connection_request_random_choice()
        return self.parse()
    if self._enable_language_tool:
      message = self._language_tool.correct(message)
    for var in NAMES:
      if var in self._data and self._data[var]:
        message = self._message.replace(var, self._data[var])
      elif check_if_templ_variable_missing(var):
        message = common_connection_request_random_choice()
        return self.parse()
    return message

  def read(self: Template) -> str:
    message = self.parse()
    if len(message) > 300:
      raise TemplateMessageLengthExceededException(
          'Personalized message length cannot exceed by 300, you gave %(characters)s characters'
          % {'characters': len(message)})
    return message

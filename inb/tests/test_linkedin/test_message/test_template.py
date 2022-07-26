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

import os
import signal
import pathlib
import unittest

from linkedin.message import template

_ADMIRATION_MESSAGE_TEMPLATE = """
Hi Etienne,
I’ve been following the work you’ve been doing for Google in the last few months, and I’m very impressed with the results achieved in such a short time! I would love to chat more and learn how you got the opportunity to work on such a project.

Best,
Ayush
""".strip('\n')


class TestTemplateBaseClass(unittest.TestCase):  # pylint: disable=missing-class-docstring
  _TEST_MSG_TEMPLATE_F = pathlib.PurePath(
      __file__).parent / 'test-message-template-f.txt'

  def setUp(self) -> None:
    self.maxDiff = None  # pylint: disable=invalid-name
    signal.signal(signal.SIGINT, self.tearDown)

  def tearDown(self) -> None:
    if os.access(self._TEST_MSG_TEMPLATE_F, os.F_OK):
      os.remove(self._TEST_MSG_TEMPLATE_F)


class TestProtectedFunctionCheckIfTemplateFileIsSupported(  # pylint: disable=missing-class-docstring
    TestTemplateBaseClass):

  def test_function_with_unsupported_file_extensions(self) -> None:
    ill_extensions = ['.py', '.pyi', '.cc', '.c', '.h', '.hh']
    for ext in ill_extensions:
      self.assertFalse(
          template._CheckIfTemplateFileIsSupported(  # pylint: disable=protected-access
              os.fspath(self._TEST_MSG_TEMPLATE_F)[:-4] + ext))

  def test_function_with_supported_file_extensions(self) -> None:
    extensions = ['.txt']
    for ext in extensions:
      self.assertTrue(
          template._CheckIfTemplateFileIsSupported(  # pylint: disable=protected-access
              os.fspath(self._TEST_MSG_TEMPLATE_F)[:-4] + ext))


class TestProtectedFunctionLoadMessageTemplate(TestTemplateBaseClass):  # pylint: disable=missing-class-docstring

  def test_function_with_invalid_path(self) -> None:
    with self.assertRaises(FileNotFoundError):
      template._LoadMessageTemplate(os.fspath(self._TEST_MSG_TEMPLATE_F)[:-4])  # pylint: disable=protected-access

  def test_function_output_with_valid_path(self) -> None:
    with open(self._TEST_MSG_TEMPLATE_F, 'w+', encoding='utf-8') as t_file:
      t_file.write(f'{template._TEMPL_BEGIN_BLOCK}')  # pylint: disable=protected-access
      t_file.write('\n\n')
      t_file.write(f'{_ADMIRATION_MESSAGE_TEMPLATE}')
      t_file.write('\n\n')
      t_file.write(f'{template._TEMPL_END_BLOCK}')  # pylint: disable=protected-access

    self.assertEqual(
        template._LoadMessageTemplate(self._TEST_MSG_TEMPLATE_F).strip('\n'),  # pylint: disable=protected-access
        _ADMIRATION_MESSAGE_TEMPLATE)


class TestFunctionReadTemplate(TestTemplateBaseClass):  # pylint: disable=missing-class-docstring

  def test_function_output(self) -> None:
    with open(self._TEST_MSG_TEMPLATE_F, 'w+', encoding='utf-8') as t_file:
      t_file.write(f'{template._TEMPL_BEGIN_BLOCK}')  # pylint: disable=protected-access
      t_file.write('\n\n')
      t_file.write(f'{_ADMIRATION_MESSAGE_TEMPLATE}')
      t_file.write('\n\n')
      t_file.write(f'{template._TEMPL_END_BLOCK}')  # pylint: disable=protected-access

    self.assertEqual(template.ReadTemplate(self._TEST_MSG_TEMPLATE_F),
                     _ADMIRATION_MESSAGE_TEMPLATE)

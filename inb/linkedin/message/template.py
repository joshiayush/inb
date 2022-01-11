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

from typing import Union

import os

_SUPPORTED_TEMPLATE_FILES_EXT = [
    '.txt',
]

_TEMPL_BEGIN_BLOCK = 'LINKEDIN MESSAGE TEMPLATE BEGIN:'
_TEMPL_END_BLOCK = 'LINKEDIN MESSAGE TEMPLATE END;'


def _CheckIfTemplateFileIsSupported(
    path: Union[str, bytes, os.PathLike]) -> bool:
  path = os.fspath(path)
  ill_template_files = 0
  for ext in _SUPPORTED_TEMPLATE_FILES_EXT:
    if not path.endswith(ext):
      ill_template_files += 1
    else:
      break
  if ill_template_files == len(_SUPPORTED_TEMPLATE_FILES_EXT):
    return False
  return True


def _LoadMessageTemplate(path: Union[str, bytes, os.PathLike]) -> str:
  if _CheckIfTemplateFileIsSupported(path) is False:
    raise FileNotFoundError(
        f'Template file {path} is not supported.  '
        f'Provide files ending with {_SUPPORTED_TEMPLATE_FILES_EXT}.')
  with open(path, 'r', encoding='utf-8') as t_file:
    message = t_file.read()
  return message[message.find(_TEMPL_BEGIN_BLOCK) +
                 len(_TEMPL_BEGIN_BLOCK):message.find(_TEMPL_END_BLOCK):]


def ReadTemplate(template_file: Union[str, bytes, os.PathLike]) -> str:
  if template_file is None:
    raise FileNotFoundError("Expected 'str' type object received 'None'.")
  return _LoadMessageTemplate(template_file).strip('\n')

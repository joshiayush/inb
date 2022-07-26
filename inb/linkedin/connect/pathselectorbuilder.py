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

"""Path selector builder for document_object_module elements."""

from __future__ import annotations

from typing import Union


class PathSelectorBuilder:
  """Builds a path selector for a document_object_module element."""

  def __init__(self, path_label: str, path_selector: Union[PathSelectorBuilder,
                                                           str]):
    self.path_label = path_label
    if isinstance(path_selector, PathSelectorBuilder):
      self.path_selector = path_selector.path_selector
    elif isinstance(path_selector, str):
      self.path_selector = path_selector

  def __add__(self, other: Union[PathSelectorBuilder,
                                 str]) -> PathSelectorBuilder:
    if isinstance(other, PathSelectorBuilder):
      self.path_selector += other.path_selector
    elif isinstance(other, str):
      self.path_selector += other
    elif isinstance(other, int):
      self.path_selector += str(other)
    else:
      raise TypeError(f'Unsupported type {type(other)}')
    return self

  def __iadd__(self, other: Union[PathSelectorBuilder,
                                  str]) -> PathSelectorBuilder:
    return self + other

  def __str__(self) -> str:
    return self.path_selector

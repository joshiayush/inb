# pylint: disable=missing-module-docstring

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

from api.utils import utils


def test_get_id_from_urn():
  urn = 'urn:li:fs_miniProfile:1234567890abcdef'
  assert utils.get_id_from_urn(urn) == '1234567890abcdef'

  urn = 'urn:li:fs_miniProfile:abc1234567890def'
  assert utils.get_id_from_urn(urn) == 'abc1234567890def'

  urn = 'urn:li:fs_miniProfile:12:34:56:78:90'
  assert utils.get_id_from_urn(urn) == '12'


def test_generate_tracking_id():
  tracking_id = utils.generate_tracking_id()
  assert len(tracking_id) == 24
  assert isinstance(tracking_id, str)

  for char in tracking_id:
    assert char.isalnum() or char in ['+', '/', '=']

  assert tracking_id != utils.generate_tracking_id()

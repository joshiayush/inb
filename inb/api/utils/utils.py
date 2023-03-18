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

"""Utility module for the LinkedIn API package."""

import base64
import random


def get_id_from_urn(urn: str) -> str:
  """Returns the last element from the profile urn string."""
  return urn.split(':')[3]


def generate_tracking_id() -> str:
  """Generates a tracking id to attach to the payload being sent to the voyager
  endpoints.

  Returns:
    Tracking id for a payload.
  """
  return str(
      base64.b64encode(bytearray([random.randrange(256) for _ in range(16)
                                 ])))[2:-1]

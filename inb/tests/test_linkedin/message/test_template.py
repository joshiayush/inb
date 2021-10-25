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

# from __future__ imports must occur at the beginning of the file. DO NOT CHANGE!
from __future__ import annotations

import unittest

from errors import TemplateFileException
from linkedin.message import Template

Template_Business = """Hi {{name}},

I'm looking to expand my network with fellow business owners and professionals. I would love to learn about what you do and see
if there's any way we can support each other.

Cheers!"""

Template_Sales = """Hi {{name}},

I'm looking to connect with like-minded professionals specifically who are on the revenue generating side of things.

Let's connect!"""

Template_Real_Estate = """Hey {{name}},

Came across your profile and saw your work in real estate. I'm reaching out to connect with other like-minded people. Would be
happy to make your acquaintance.

Have a good day!"""

Template_Creative_Industry = """Hi {{name}},

LinkedIn showed me your profile multiple times now, so I checked what you do. I really like your work and as we are both in the
creative industy - I thought I'll reach out. It's always great to be connected with like-minded individuals, isn't it?

{{my_name}}"""

Template_Hr = """Hey {{name}},

I hope your week is off to a great start, I noticed we both work in the HR/Employee Experience field together.

I would love to connect with you."""

Template_Include_Industry = """Hi {{name}},

I hope you're doing great! I'm on a personal mission to grow my connections on LinkedIn, especially in the field of {{industry}}.
So even though we're practically strangers, I'd love to connect with you.

Have a great day!"""

Template_Ben_Franklin = """Hi {{name}},

The Ben Franklin effect - when we do a person a favor, we tend to like them more as a result. Anything I can do for you?

Best, {{my_name}}"""

Template_Virtual_Coffee = """Hi {{name}},

I hope you're doing well. I'm {{my_name}}, {{my_position}} of {{my_company_name}}. We're looking for {{position}} and it would be
great to connect over a 'virtual' coffee/chat and see what we can do together?"""

Template_Common_Connection_Request = [
  """Hey {{name}},

I notice we share a mutual connection or two & would love to add you to my network of professionals.

If you're open to that let's connect!""",
  """Hi {{name}},

I see we have some mutual connections. I always like networking with new people, and thought this would be an easy way for us to
introduce ourselves.""",
  """Hi {{name}},

Life is both long and short. We have quite a few mutual connections. I would like to invite you to join my network on LinkedIn
platform. Hopefully, our paths will cross professionally down the line. Until then, wishing you and yours an incredible {{year}}.

{{my_name}}""",
  """Hi {{name}},

I was looking at your profile and noticed we had a few shared connections. I thought it would be nice to reach out to connect with
you and share out networks.

Thank you and hope all is well!""",
  """Hey {{first_name}},

I saw you're based in {{location}} and work on {{keyword}}, I'd love to connect.

Thanks, {{my_name}}"""
]


class TestTemplateApi(unittest.TestCase):
  def test_static_method_get_template_by_name(
          self: TestTemplateApi) -> None:
    template = Template(
        None, var_template=None, grammar_check=False,
        use_template='template_ben_franklin')
    self.assertEqual(template.get_template_by_name(
      'template_ben_franklin'), Template_Ben_Franklin)
    self.assertEqual(template.get_template_by_name(
      'template_business'), Template_Business)
    self.assertEqual(template.get_template_by_name(
      'template_sales'), Template_Sales)
    self.assertEqual(template.get_template_by_name(
      'template_real_estate'), Template_Real_Estate)
    self.assertEqual(template.get_template_by_name(
        'template_creative_industry'),
        Template_Creative_Industry)
    self.assertEqual(
        template.get_template_by_name('template_hr'),
        Template_Hr)
    self.assertEqual(template.get_template_by_name(
        'template_include_industry'),
        Template_Include_Industry)
    self.assertEqual(template.get_template_by_name(
      'template_virtual_coffee'), Template_Virtual_Coffee)
    for i in range(5):
      self.assertEqual(
          template.get_template_by_name(
              'template_common_connection_request')[i],
          Template_Common_Connection_Request[i])
    with self.assertRaises(TemplateFileException):
      template.get_template_by_name('any_unknown_template')

  def test_method_parse_with_template_business(
          self: TestTemplateApi) -> None:
    template = Template(None, var_template=None,
                        use_template='template_business',
                        grammar_check=False)
    template.set_data({
      'name': 'Ayush',
    })
    template_business = Template_Business.replace(
        '{{name}}', 'Ayush')
    self.assertEqual(template.parse(), template_business)

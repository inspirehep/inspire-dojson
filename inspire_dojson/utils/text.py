# -*- coding: utf-8 -*-
#
# This file is part of INSPIRE.
# Copyright (C) 2014-2017 CERN.
#
# INSPIRE is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# INSPIRE is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with INSPIRE. If not, see <http://www.gnu.org/licenses/>.
#
# In applying this license, CERN does not waive the privileges and immunities
# granted to it by virtue of its status as an Intergovernmental Organization
# or submit itself to any jurisdiction.

from __future__ import absolute_import, division, print_function

import re

import six


try:
    six.unichr(0x100000)
    RE_ALLOWED_XML_1_0_CHARS = re.compile(
        u'[^\U00000009\U0000000A\U0000000D\U00000020-'
        u'\U0000D7FF\U0000E000-\U0000FFFD\U00010000-\U0010FFFF]')
    RE_ALLOWED_XML_1_1_CHARS = re.compile(
        u'[^\U00000001-\U0000D7FF\U0000E000-\U0000FFFD\U00010000-\U0010FFFF]')
except ValueError:
    # oops, we are running on a narrow UTF/UCS Python build,
    # so we have to limit the UTF/UCS char range:
    RE_ALLOWED_XML_1_0_CHARS = re.compile(
        u'[^\U00000009\U0000000A\U0000000D\U00000020-'
        u'\U0000D7FF\U0000E000-\U0000FFFD]')
    RE_ALLOWED_XML_1_1_CHARS = re.compile(
        u'[^\U00000001-\U0000D7FF\U0000E000-\U0000FFFD]')


def encode_for_xml(text, wash=False, xml_version='1.0', quote=False):
    """Encode special characters in a text so that it would be XML-compliant.

    :param text: text to encode
    :return: an encoded text
    """
    if not isinstance(text, six.text_type):
        text = six.text_type(text)

    text = text.replace('&', '&amp;')
    text = text.replace('<', '&lt;')
    if quote:
        text = text.replace('"', '&quot;')
    if wash:
        text = wash_for_xml(text, xml_version=xml_version)
    return text


def wash_for_xml(text, xml_version='1.0'):
    """Remove any character which isn't a allowed characters for XML.

    The allowed characters depends on the version
    of XML.
        - XML 1.0:
            <http://www.w3.org/TR/REC-xml/#charsets>
        - XML 1.1:
            <http://www.w3.org/TR/xml11/#charsets>

    :param text: input string to wash.
    :param xml_version: version of the XML for which we wash the
        input. Value for this parameter can be '1.0' or '1.1'
    """
    if xml_version == '1.0':
        return RE_ALLOWED_XML_1_0_CHARS.sub('', text)
    else:
        return RE_ALLOWED_XML_1_1_CHARS.sub('', text)

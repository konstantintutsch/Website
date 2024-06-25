# manifest_html_parser.py
#
# Copyright 2024 Satvik Patwardhan
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
# SPDX-License-Identifier: GPL-3.0-or-later

from html.parser import HTMLParser

class ManifestHTMLParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.manifest_url = None
        self.title = None
        self.favicon = None
        self.starttag = ''

    def handle_starttag(self, tag, attrs):
        self.starttag = tag
        if tag == 'link' and ('rel', 'manifest') in attrs:
            manifest_url = ''
            for attr in attrs:
                if attr[0] == 'href':
                    manifest_url = attr[1]
            self.manifest_url = manifest_url
        if tag == 'link' and (('rel', 'icon') in attrs or ('rel', 'shortcut icon') in attrs):
            for attr in attrs:
                if attr[0] == 'href':
                    self.favicon = attr[1]

    def handle_endtag(self, tag):
        pass

    def handle_data(self, data):
        if data.strip() != "":
            if self.starttag == "title":
                self.title = data
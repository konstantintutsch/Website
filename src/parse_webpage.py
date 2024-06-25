# parse_webpage.py
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


import os
import requests

from urllib import parse

from .manifest_html_parser import ManifestHTMLParser

def get_website_data_from_webpage(url):
    """ Get the favicon and name from the given url by data gathered by the webview. """
    if not url.startswith('http'):
        url = 'https://' + url
    if not url.endswith('/'):
        url += '/'

    name = None
    favicon = None

    try:
        html = requests.get(url, timeout=10).text
        parser = ManifestHTMLParser()
        parser.feed(html)

        name = parser.title
        favicon = parser.favicon
    except Exception as e:
        print(_("Error accessing URL:"), e)
        
    if favicon and not favicon.startswith("http"):
        favicon = favicon.strip('/')
        favicon = url + favicon

    if favicon:
        try:
            request = requests.get(parser.favicon)
            icon = request.content

            with open('/tmp/webapps_icon.png', 'wb') as f:
                f.write(icon)

            return ['/tmp/webapps_icon.png', name] if name else ['/tmp/webapps_icon.png', None]
        except:
            pass
        
    # If code reached here it means favicon still isn't there

    domain_name = parse.urlparse(url).netloc
    try:
        # SECRET google api. Do not trust.
        print(_("Google API for favicons being used... if correct favicon is not visible please file a bug report!"))
        request = requests.get('https://www.google.com/s2/favicons?sz=256&domain_url=' + domain_name)
        if request.headers['content-type'] == "image/png":
            icon = request.content
            with open('/tmp/webapps_icon.png', 'wb') as f:
                f.write(icon)

            return ['/tmp/webapps_icon.png', name] if name else ['/tmp/webapps_icon.png', None]

        if icon == b'\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00\x10\x00\x00\x00\x10\x08\x06\x00\x00\x00\x1f\xf3\xffa\x00\x00\x00\tpHYs\x00\x00\x0b\x12\x00\x00\x0b\x12\x01\xd2\xdd~\xfc\x00\x00\x02\x88IDAT8\x11\xa5S\xcdO\x13Q\x10\x9f\xda\xd2nK\xbbP\xb6T[\xe9B\x81"D0\x91\x14R\x139\x10\x83!\x1c\xeaY\x0e*\x07\x0e\xa6\x1e\xfcc\xe0\xa0\x8dx\xc3\xb3h\xb8\xe0U\xd8\xf4\x03\x13\x95\x04T\x10\xb6Z\xa5Yh\xbb-\xdd\xeeB\xadoFk\xd0\xc4\x8bN\xf2\xf6\xcd\xbe\xf9x\xbf7\xf3\x1bS\xbd^\x87\xff\x11\x0b\x06\x9bL&\x88\xde\\\xb0\x97\xca\x86\xe7\xca\x888b\x1c\xd7b\xf9\x82\x16.\xaaU\'\xday\x17Wv\xb7\xdaSV\xaby^J\xcaI\x97\xd3\xaa\xdc\xbf;\xa6\x8d\x8f\xf5\x82\t\x11\xdc\x98~l\xd7\xf5\x9a\xbf/\xd4>[.\xeb\xd1\xde\xa0\xe0\x15\xbb\xdb\x04\x96\x08\xacMf\x08\x8a\x02\xac\xacl\x1e\xec\xca\xf9\x1c\xef\xb2-\xbd\xfb\xa0\xc4m6s\xf6\xe9\xe2\x8cF\x08\xf0\xe6\xc1\x81s\xb3\x95\xca\xf1\xf4\xe0%_ \xd8)@\xb3\xc3\n\xc3C\x1dpT1\xa0\xd3\xcfC\xb7\xe8\x11\xdelf\x85\xc5\'ig\xa8\xc7\x03\x1b\x9b\xfb\xf3\x0c\\\xe6\x0cB\x8c0\xd8j\xb9\x1a\x9d\xb9=J\xc1x\x86\xb7K\xeb{\xa8\x92x\x05\x07414wn\x8d\x06\xd0\x17c\xd0@\t\x0c\xa3\x16\xeb\n\xb8\xbd\x91\xcb\xe2\x0fo\xf6=f\tp\xb9[\x1ctv\xa4\x9d@\xa1\xa8\xb1\x7f;\x88\xe7\xdd^]?\x89\xa1\x81\x12`\xc1&&\xfa\x05t:-\xd7\xae\xf6\x01\xdfL\xaf\x84f\xbb\x05.\xf4xaG>\x84\xc9\xc9\x01\xe10\xaf\x85\xd1\x97\xacEUs\x9e\xf5\xf0\xe4\x8co\xef\xf0\xb5\xd2j\x04\xa3\xa3\x99]\xb5\xaf\x94P\x05\xf4UY\x0c\xea\x84\x00\x15\x0cD\x89\x0cw\xc1\xa7/\x05V\x83\xdf\xd1\x90\x91}\xb0\x0e(\r\xf6\x10\x02\xec\xf3\x8e\xac\xf0\xbev\x91P\\g\xfd}\x99\x96a\x8b\\\x01;\x00\xbev\x07\x8cG\x82\xa0\x14\xaa\xb0\xb5\x9d#n\xa0\x99\x10\xb4\xb9\x1d\xa9\x17\xac\xcf?\xfdi\x1b\xea\xf7CN)\xd3\x92\xd6w!\xf1:K\xe7\x9eV\x0e\x9e=\x7f{\x801x@\t\x18\xc3\xe6>2\x92\xe0\xad\x7f\x93\xcf\xecY\xb5o@\xc8\xb2_\xd5\x1cg\xb3\xcc\xfdJ\xc0\xe8\x99B\x86\xc5\x17\xd62\x8d$X@D\xd1\x10\xd4\xa5W2<\x88\xaffZ\\\xdc\x92\x94\x92\t\x01\xd5\x00\xb9\x8d\xf4\x0c\xf5z\xe0\xe1\xa3\xd5\xe8\xf2\xf2\x86wj\xea\xa2\x80<\xc8\x17+\xc0x\x02\xa9\x84t\x90\xc9\x16r-<\xb7\xf4~[\x89c\x0c&\xa7Y8=L\x91\xb0\x18\xd6\x8d\x93{\xd8g\xb5Tu\xe2\xac`\x91\x856G\xd2\xce5\xcd\xad%\xf6\xd2\xce?\x87\xa9\x01\xf3_\xf6\xefX!\x1b^\xe5\xfa\xb3\xd3\x00\x00\x00\x00IEND\xaeB`\x82':
            # the default favicon served by the API
            return [None, name] if name else [None, None]

    except Exception as e:
        return [None, name] if name else [None, None]
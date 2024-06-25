# parse_manifest.py
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

import requests
import json
from urllib import parse

from .manifest_html_parser import ManifestHTMLParser

def get_manifest_json(url):
    if not url.startswith('http'):
        url = 'https://' + url
    if not url.endswith('/'):
        url += '/'

    try:
        request = requests.get(url, timeout=5)
        html = request.text
    except:
        return None

    parser = ManifestHTMLParser()
    parser.feed(html)
    manifest_url = parser.manifest_url
    
    if manifest_url:
        if not (manifest_url.startswith('http') or manifest_url.startswith('data:application/json')):
            # this is a relative path
            domain_name = parse.urlparse(url).netloc
            manifest_prefix = manifest_url.rpartition('/')[0] + '/' if manifest_url.rpartition('/')[0] != '' else ''
            # sometimes manifest urls are in form of images/manifest.json etc
            manifest_url = 'https://' + domain_name + '/' + manifest_url.lstrip('/')
        else:
            manifest_prefix = ''

        try:
            manifest = requests.get(manifest_url, timeout=5).text # This is a json file
        except:
            manifest = ""

        if manifest != '':
            try:
                manifest = json.loads(manifest)
            except:
                return None
            return [manifest, manifest_prefix]
        else:
            return None
    
    else:
        return None


def get_favicon_from_manifest(manifest, manifest_prefix, domain_name):
    if 'icons' in manifest:
        max_size = [0, '']
        for i in manifest['icons']:
            if 'purpose' in i and i['purpose'] == 'monochrome':
                continue
            size = int(i['sizes'].split('x')[0])
            if size > max_size[0] and size <= 512:
                max_size = [size, i['src']]
            if i['type'] == 'image/svg' or i['type'] == 'image/svg+xml':
                max_size = [512, i['src']]
        
        if max_size[1] == '': # We only want icons upto 512x512 in size otherwise the dynamic launcher breaks.
            return None

        if not max_size[1].startswith('http'):
            max_size[1] = 'https://' + domain_name + '/' + manifest_prefix + max_size[1].lstrip('/')
        
        try:
            icon = requests.get(max_size[1], timeout=2).content
        except:
            return None
        
        if icon:
            with open('/tmp/webapps_icon.png', 'wb') as f:
                f.write(icon)

            return '/tmp/webapps_icon.png'

        else:
            return None

    else:
        return None

def get_website_data_from_manifest(url):
    """ Get the favicon and name from the given url. If manifest is not found, return None """
    manifest_data = get_manifest_json(url)
    if manifest_data is None:
        return [None, None]
    
    manifest = manifest_data[0]
    manifest_prefix = manifest_data[1]
    domain_name = parse.urlparse(url).netloc

    favicon = get_favicon_from_manifest(manifest, manifest_prefix, domain_name)
    name = manifest['name']

    return [favicon, name]
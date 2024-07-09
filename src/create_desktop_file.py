# create_desktop_file.py
#
# Copyright 2023 Satvik Patwardhan
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

import threading
import time
import os
import shutil
import sys
import gi
import json
import stat

from gi.repository import Gtk, GLib, Gio

global app
global parentwindow

def desktop_filer(parent, app_id, name):
    global parentwindow
    parentwindow = parent

    icon_path = os.path.expanduser('~/.var/app/net.codelogistics.webapps/icons/192x192/net.codelogistics.webapps.' + app_id + '.png')
    write_desktop_file(app_id, name, icon_path)

def write_desktop_file(app_id, name, icon_path):
    global app
    app = app_id
    
    desktop_file = '[Desktop Entry]\nName={}\nIcon={}\nExec = flatpak run net.codelogistics.webapps {}\nTerminal=false\nType=Application\nCategories=Network;\nTryExec=/var/lib/flatpak/exports/bin/net.codelogistics.webapps'.format(name, icon_path, app_id)

    with open(os.path.expanduser('~/.local/share/applications/net.codelogistics.webapps.{}.desktop'.format(app_id)), 'w') as f:
        f.write(desktop_file)

    os.chmod(os.path.expanduser('~/.local/share/applications/net.codelogistics.webapps.{}.desktop'.format(app_id)), mode=0o755)
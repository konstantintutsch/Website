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
gi.require_version("WebKit", "6.0")

from gi.repository import Gtk, GLib, Gio, WebKit, Xdp

global app
global parentwindow

def desktop_filer(parent, name, url, icon):
    global parentwindow
    parentwindow = parent
    if icon == _("Default Favicon"):
        if os.path.exists('.var/app/net.codelogistics.webapps/icons/192x192/net.codelogistics.webapps.' + name.replace(' ', '-') + '.png'):
            # in case url is being changed
            os.remove('.var/app/net.codelogistics.webapps/icons/192x192/net.codelogistics.webapps.' + name.replace(' ', '-') + '.png')
        window = Gtk.Window()
        webview = WebKit.WebView()
        network_session = webview.get_network_session()
        data_manager = network_session.get_website_data_manager()
        data_manager.set_favicons_enabled(True)

        window.set_child(webview)
        webview.load_uri(url)
        webview.connect("notify::favicon", favicon_loaded, name)
        end_time = time.time() + 10
        check_if_favicon_thread = threading.Thread(target = check_if_favicon, args = (end_time, name,))
        check_if_favicon_thread.start()

    else:
        icon_path = '.var/app/net.codelogistics.webapps/icons/192x192/net.codelogistics.webapps.' + name.replace(' ', '-') + '.png'
        write_desktop_file(name, icon_path)

def favicon_loaded(webview, favicon, name):
    favicon = webview.get_favicon()
    if favicon:
        icon_path = '.var/app/net.codelogistics.webapps/icons/192x192/net.codelogistics.webapps.' + name.replace(' ', '-') + '.png'
        with open(icon_path, 'wb') as f:
            f.write(favicon.save_to_png_bytes().get_data())
    else:
        favicon = '/app/share/icons/hicolor/96x96/apps/net.codelogistics.webapps.png'
        icon_path = '.var/app/net.codelogistics.webapps/icons/192x192/net.codelogistics.webapps.' + name.replace(' ', '-') + '.png'
        shutil.copyfile(favicon, icon_path)

def check_if_favicon(end_time, name):
    while time.time() < end_time:
        if os.path.exists('.var/app/net.codelogistics.webapps/icons/192x192/net.codelogistics.webapps.' + name.replace(' ', '-') + '.png'):
            icon_path = '.var/app/net.codelogistics.webapps/icons/192x192/net.codelogistics.webapps.' + name.replace(' ', '-') + '.png'
            while os.path.getsize(icon_path) < 1:
                pass
            write_desktop_file(name, icon_path)
            break
    else:
        favicon = '/app/share/icons/hicolor/96x96/apps/net.codelogistics.webapps.png'
        icon_path = '.var/app/net.codelogistics.webapps/icons/192x192/net.codelogistics.webapps.' + name.replace(' ', '-') + '.png'
        shutil.copyfile(favicon, icon_path)
        write_desktop_file(name, icon_path)

def write_desktop_file(name, icon_path):
    global app
    app = name
    portal = Xdp.Portal()
    with open(icon_path, 'rb') as f:
        icon = Gio.BytesIcon.new(GLib.Bytes.new(f.read())).serialize()
    portal.dynamic_launcher_prepare_install(None, name, icon, Xdp.LauncherType.APPLICATION, None, False, False, None, finish_install)

def finish_install(portal, result):
    global app
    global parentwindow
    try:
        variant = portal.dynamic_launcher_prepare_install_finish(result)
    except Exception as e:
        if os.path.exists('.var/app/net.codelogistics.webapps/webapps/' + app + '.json'):
            os.remove('.var/app/net.codelogistics.webapps/webapps/' + app + '.json')
        if os.path.exists('.var/app/net.codelogistics.webapps/webapps/' + app + '.window'):
            os.remove('.var/app/net.codelogistics.webapps/webapps/' + app + '.window')
        if os.path.exists('.var/app/net.codelogistics.webapps/webapps/' + app + '.cookies.txt'):
            os.remove('.var/app/net.codelogistics.webapps/webapps/' + app + '.cookies.txt')
        if os.path.exists('.var/app/net.codelogistics.webapps/icons/192x192/net.codelogistics.webapps.' + app + '.png'):
            os.remove('.var/app/net.codelogistics.webapps/icons/192x192/net.codelogistics.webapps.' + app + '.png')
        parentwindow.refresh_rows()
        # Translators: Do not translate portal
        print(_('Portal Error:'), e, file=sys.stderr)
        return
    app = variant['name'].replace(' ', '-')
    notCancelled = portal.dynamic_launcher_install(variant['token'],"net.codelogistics.webapps." + app + ".desktop", '[Desktop Entry]\nExec = webapps ' + variant['name'].replace(' ', '-') + '\nTerminal=false\nType=Application\nCategories=Network;')

    with open('.var/app/net.codelogistics.webapps/webapps/' + app + '.json', 'r') as f:
        state = json.load(f)
    state['icon'] = '.var/app/net.codelogistics.webapps/icons/192x192/net.codelogistics.webapps.' + app.replace(' ', '-') + '.png'
    with open('.var/app/net.codelogistics.webapps/webapps/' + app + '.json', 'w') as f:
        json.dump(state, f)
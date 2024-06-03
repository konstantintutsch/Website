# main.py
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

import os
import sys
import gi
import json
from pathlib import Path

gi.require_version('Gtk', '4.0')
gi.require_version("Adw", '1')
gi.require_version('GIRepository', '2.0')
gi.require_version('Xdp', '1.0')

from gi.repository import Gtk, GModule, GObject, GIRepository, Gio, GLib, Adw
from .window import WebAppsWindow
from .web_app_window import WebAppWindow

class WebappsApplication(Adw.Application):
    """The main application singleton class."""

    def __init__(self, args):
        if len(args) > 1 and args[1] + '.json' in os.listdir('.var/app/net.codelogistics.webapps/webapps/'):
            super().__init__(application_id='net.codelogistics.webapps.' + args[1],
                         flags=Gio.ApplicationFlags.DEFAULT_FLAGS)
        else:
            super().__init__(application_id='net.codelogistics.webapps.Webapps',
                             flags=Gio.ApplicationFlags.DEFAULT_FLAGS)
        self.create_action('quit', lambda *_: self.quit(), ['<primary>q'])
        self.create_action('about', self.on_about_action)
        self.args = args

    def do_activate(self):
        """Called when the application is activated.

        We raise the application's main window, creating it if
        necessary.
        """
        if len(self.args) > 1 and self.args[1] + '.json' in os.listdir('.var/app/net.codelogistics.webapps/webapps'):
            with open('.var/app/net.codelogistics.webapps/webapps/' + self.args[1] + '.json', 'r') as f:                
                state = json.load(f)
            win = WebAppWindow(application=self, state = state)
            win.present()
        else:
            win = WebAppsWindow(application=self)
            win.present()

    def on_about_action(self, widget, _):
        """Callback for the app.about action."""
        about = Adw.AboutDialog()
        about.set_application_name("Web Apps")
        about.set_comments("Install websites as apps")
        about.set_developer_name("Satvik Patwardhan")
        about.set_application_icon('net.codelogistics.webapps')
        about.set_version('0.4.4')
        about.set_license_type(Gtk.License.GPL_3_0)
        about.set_developers(['Satvik Patwardhan'])
        about.set_copyright('© 2024 Satvik Patwardhan')
        about.set_website("https://codelogistics.net/")
        about.set_issue_url("https://codeberg.org/eyekay/webapps/issues")

        about.present(self.get_active_window())

    def create_action(self, name, callback, shortcuts=None):
        """Add an application action.

        Args:
            name: the name of the action
            callback: the function to be called when the action is
              activated
            shortcuts: an optional list of accelerators
        """
        action = Gio.SimpleAction.new(name, None)
        action.connect("activate", callback)
        self.add_action(action)
        if shortcuts:
            self.set_accels_for_action(f"app.{name}", shortcuts)


def main(version):
    """The application's entry point."""

    Path(".var/app/net.codelogistics.webapps/webapps/").mkdir(parents=True, exist_ok=True)
    Path(".var/app/net.codelogistics.webapps/icons/192x192/").mkdir(parents=True, exist_ok=True)

    app = WebappsApplication(args = sys.argv)
    return app.run()


